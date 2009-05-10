# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Parser.py: Parses HTML documents and counts tag transitions

import glob, pickle, pprint, re, os, fnmatch
import sys
from BeautifulSoup import BeautifulSoup, Comment, NavigableString, Tag

class Parser:

    def __init__(self, objfile, progressive = False, debug = False):
        # Initialize the tag transition map
        self.transitions, self.attributes = {}, {}
        self.TEXTelems = []
        self.indebug = False
        self.logs = []
        self.progr = None
        self.objFile = 'model.mem'
        self.textSymbol = 'TEXT'            # Special symbol for document text


        self.indebug = debug
        # progressive means we load the previous run, save as we can
        if progressive is None:
            self.progr = False
        else:
            self.progr = progressive
        print "progr: ", self.progr
        if objfile is None:
            self.objFile = 'model.mem'
        else:
            self.objFile = objfile
        if self.progr is True:
            if os.path.exists(self.objFile):
                self.thaw();

    def parseFilesInDir(self, directory):
        '''Parse all HTML files inside the given directory'''

        if not directory.endswith('/'):
            directory += '/'
        # Find the file names of all HTML files
        filenames = self.rglob("*.html", directory)
        # Loop over all file names in sorted order
        i = 0
        for filename in sorted(filenames):
            if filename in self.logs:
                print "Skipping ", filename
                continue
            # Parse the HTML file
            print 'Parsing file (' + str(i) + '):', filename
            self.parseFile(filename)
            self.logs.append(filename)
            self.store('texts.dat', 'a', self.TEXTelems)
            self.TEXTelems = []
            # in the event that something failed before, we can at least kinda recover
            if self.progr is True:
                self.freeze()

                if self.indebug:
                    print 'Transitions Map:'
                    pprint.pprint(self.transitions)
                    print 'Attributes Map:'
                    pprint.pprint(self.attributes)
            sys.stdout.flush()
            i += 1

    def parseFile(self, filename):
        '''Parse HTML code from the given file and put the transition counts in the given dictionary'''
        # Open the HTML file and create a soup from it
        infile = open(filename, 'r')
        soup = BeautifulSoup(infile)
        infile.close()
        # Remove HTML junk from the soup
        self.removeJunk(soup)
        # Count the tag transitions starting from the HTML root tag
        self.countTagTrans(soup.html, self.transitions, self.attributes)

    def countTagTrans(self, tag, trans, attrs):
        '''Count the HTML tag transitions starting from the given tag'''
        # Check if the given tag is indeed a tag
        if isinstance(tag, Tag):
            tagname = self.safe_str(tag.name.upper())
##        if debug:
##            print 'tag name:', tag.name
##            print 'tag contents:', tag.contents
            rule = []
            # Loop over each child of the tag
            for child in tag.contents:
                # Append the child tag name to the rule, count the attribute
                #   transitions, and recursively count the tag transitions
                if isinstance(child, Tag):
                    rule.append(self.safe_str(child.name.upper()))
                    self.countAttrTrans(child, attrs)
                    self.countTagTrans(child, trans, attrs)
                # Append the child string as a text symbol if it is not whitespace
                elif isinstance(child, NavigableString):
                    if not re.match(r'^\s+$', child):
                        rule.append(self.textSymbol)
                        self.TEXTelems.append(self.safe_str(child.string))
                else:
                    print '!!! unknown child type:', child
            # Check if the tag is in the transition map
            if tagname not in trans:
                trans[tagname] = {}
            # Increment the tag transition count for this rule
            trans[tagname][tuple(rule)] = trans[tagname].get(tuple(rule), 0) + 1
            self.dprint('trans[', tagname, '][', self.liststr(rule), ']: ', trans[tagname][tuple(rule)])
        self.dprint('!!! non-Tag given to countTagTrans:', tag)

    def countAttrTrans(self, tag, attrs):
        '''Count the HTML tag attribute transitions for the given tag'''
        # Check if the given tag is indeed a tag
        if isinstance(tag, Tag):
            tagname = self.safe_str(tag.name.upper())
            self.dprint('tag attributes: ', dict(tag.attrs))
            rule = []
            # Loop over each attribute name-value pair of the tag
            for name, value in tag.attrs:
                name, value = self.safe_str(name), self.safe_str(value)
                # Append the attribute name to the rule
                rule.append(name)
                # Check if the attribute is in the transition map
                if name not in attrs:
                    attrs[name] = {}
                # Increment the attribute transition count for this name-value pair
                attrs[name][value] = attrs[name].get(value, 0) + 1
            # Check if the tag is in the attribute transition map
            if tagname not in attrs:
                attrs[tagname] = {}
            # Increment the tag transition count for this rule
            attrs[tagname][tuple(rule)] = attrs[tagname].get(tuple(rule), 0) + 1
            self.dprint('attrs[', tagname, '][', self.liststr(rule), ']: ', attrs[tagname][tuple(rule)])
        self.dprint('!!! non-Tag given to countAttrTrans: ', tag)

    def removeJunk(self, soup):
        '''Remove junk HTML tags from the given BeautifulSoup'''
        self.dprint(self.separator('removing junk'))
        # Remove all unsupported elements
        junkTags = ['applet', 'embed', 'object', 'script', 'meta', 'link', 'style', 'onload', 'onunload']
        for junkTag in junkTags:
            for junk in soup.findAll(name=junkTag):
                junk.extract()
                self.dprint('junk: ', junk)
        # Remove all comments
        for comment in soup.findAll(text = self.isComment):
            comment.extract()
            self.dprint('comment: ', comment.strip())

    def isComment(self, text):
        '''Return true if the given text is an instance of Comment'''
        return isinstance(text, Comment)

    def liststr(self, alist):
        '''Return a string representation of the given list or tuple'''
        if isinstance(alist, list) or isinstance(alist, tuple):
            return ','.join(alist)
        else:
            return ''

    def separator(self, title):
        '''Return a string separator with the given title'''
        return '\n---------- ' + title + ' ----------'

    def thaw(self):
        #print "Thawing file:", self.objFile
        file = open(self.objFile, 'rb')
        obj = pickle.load(file)
        self.transitions = obj.transitions
        self.attributes = obj.attributes
        self.TEXTelems = obj.TEXTelems
        self.logs = obj.logs
        file.close()

    def store(self, file, mode, object):
        #print 'Freezing file:', file
        fd = open(file, mode)
        pickle.dump(object, fd)
        fd.close
        return True

    def load(self, file, mode):
        #print 'Freezing file:', file
        fd = open(file, mode)
        objects = []
        objects = pickle.load(fd)
        fd.close
        return objects

    def freeze(self):
        #print 'Freezing file:', self.objFile 
        file = open(self.objFile, 'wb')
        pickle.dump(self, file)
        file.close()
        return True

    def rglob(self, pattern, root = os.curdir):
        '''Recursively locate files matching the given pattern in the given directory'''
        # Borrowed from the ActiveState recipes, recursive glob
        for path, dirs, files in os.walk(os.path.abspath(root)):
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(path, filename)


    def safe_str(self, obj):
        """ return the byte string representation of obj """
        try:
            return str(obj)
        except UnicodeEncodeError:
            # obj is unicode
            return unicode(obj).encode('unicode_escape')

    def dprint(self, *what):
        if self.indebug:
            print what

