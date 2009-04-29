# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Parser.py: Parses HTML documents and counts tag transitions

import glob, pickle, pprint, re, os, fnmatch
from BeautifulSoup import BeautifulSoup, Comment, NavigableString, Tag

textSymbol  = 'TEXT'            # Special symbol for document text
transFile   = 'transitions.dat' # File name for the tag transition counts

# Initialize the tag transition map
transitions, attributes = {}, {}

def rglob(pattern, root=os.curdir):
    '''Recursively locate files matching the given pattern in the given directory'''
    # Borrowed from the ActiveState recipes, recursive glob
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

def parseFilesInDir(directory, debug=False):
    '''Parse all HTML files inside the given directory'''
    if not directory.endswith('/'):
        directory += '/'
    # Find the file names of all HTML files
    filenames = rglob("*htm*", directory)
    # Loop over all file names in sorted order
    for filename in sorted(filenames):
        # Parse the HTML file
        parseFile(filename, transitions, debug)
    if debug:
        print 'Transitions Map:'
        pprint.pprint(transitions)
        print 'Attributes Map:'
        pprint.pprint(attributes)

def parseFile(filename, transitions={}, debug=False):
    '''Parse HTML code from the given file and put the transition counts in the given dictionary'''
    print 'Parsing HTML code from input file:', filename
    # Open the HTML file and create a soup from it
    infile = open(filename, 'r')
    soup = BeautifulSoup(infile)
    infile.close()
##    if debug:
##        print separator('before removing junk')
##        print soup.prettify()
    # Remove HTML junk from the soup
    removeJunk(soup, debug)
##    if debug:
##        print separator('after removing junk')
##        print soup.prettify()
    # Count the tag transitions starting from the HTML root tag
    countTagTrans(soup.html, transitions, attributes, debug)

def countTagTrans(tag, trans, attrs, debug=False):
    '''Count the HTML tag transitions starting from the given tag'''
    # Check if the given tag is indeed a tag
    if isinstance(tag, Tag):
        tagname = str(tag.name.upper())
##        if debug:
##            print 'tag name:', tag.name
##            print 'tag contents:', tag.contents
        rule = []
        # Loop over each child of the tag
        for child in tag.contents:
            # Append the child tag name to the rule, count the attribute
            #   transitions, and recursively count the tag transitions
            if isinstance(child, Tag):
                rule.append(str(child.name.upper()))
                countAttrTrans(child, attrs, debug)
                countTagTrans(child, trans, attrs, debug)
            # Append the child string as a text symbol if it is not whitespace
            elif isinstance(child, NavigableString):
                if not re.match(r'^\s+$', child):
                    rule.append(textSymbol)
            else:
                print '!!! unknown child type:', child
        # Check if the tag is in the transition map
        if tagname not in trans:
            trans[tagname] = {}
        # Increment the tag transition count for this rule
        trans[tagname][tuple(rule)] = trans[tagname].get(tuple(rule), 0) + 1
        if debug: print 'trans['+tagname+']['+liststr(rule)+']:', trans[tagname][tuple(rule)]
    elif debug: print '!!! non-Tag given to countTagTrans:', tag

def countAttrTrans(tag, attrs, debug=False):
    '''Count the HTML tag attribute transitions for the given tag'''
    # Check if the given tag is indeed a tag
    if isinstance(tag, Tag):
        tagname = str(tag.name.upper())
        if debug: print 'tag attributes:', dict(tag.attrs)
        rule = []
        # Loop over each attribute name-value pair of the tag
        for name, value in tag.attrs:
            name, value = str(name), str(value)
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
        if debug: print 'attrs['+tagname+']['+liststr(rule)+']:', attrs[tagname][tuple(rule)]
    elif debug: print '!!! non-Tag given to countAttrTrans:', tag

def removeJunk(soup, debug=False):
    '''Remove junk HTML tags from the given BeautifulSoup'''
    if debug: print separator('removing junk')
    # Remove all unsupported elements
    junkTags = ['applet', 'embed', 'object', 'script', 'meta', 'link', 'style', 'onload', 'onunload']
    for junkTag in junkTags:
        for junk in soup.findAll(name=junkTag):
            junk.extract()
            if debug: print 'junk:', junk
    # Remove all comments
    for comment in soup.findAll(text=isComment):
        comment.extract()
        if debug: print 'comment:', comment.strip()

def isComment(text):
    '''Return true if the given text is an instance of Comment'''
    return isinstance(text, Comment)

def liststr(alist):
    '''Return a string representation of the given list or tuple'''
    if isinstance(alist, list) or isinstance(alist, tuple):
        return ','.join(alist)
    else:
        return ''

def separator(title):
    '''Return a string separator with the given title'''
    return '\n---------- ' + title + ' ----------'

def saveTransitions(datafilename=None):
    '''Save the given transition counts to the given data file'''
    # Use the default data file name if none is given
    if datafilename is None:
        datafilename = transFile
    print 'Saving transition counts to data file:', datafilename
    # Open the data file and dump the transition counts into it
    datafile = open(datafilename, 'wb')
    pickle.dump((transitions, attributes), datafile)
    if not transitions:
        print "!!! empty transition map saved"
    datafile.close()

def loadTransitions(datafilename=None):
    '''Load the transition counts from the given data file'''
    # Use the default data file name if none is given
    if datafilename is None:
        datafilename = transFile
    print 'Loading transition counts from data file:', datafilename
    # Open the data file and load the transition counts from it
    datafile = open(datafilename, 'rb')
    transitions, attributes = pickle.load(datafile)
    if not transitions:
        print "!!! empty transition map loaded"
    datafile.close()
    return transitions, attributes
