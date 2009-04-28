# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Parser.py: Parses HTML documents and counts tag transitions

import glob, pickle, pprint, re, os, fnmatch
from BeautifulSoup import BeautifulSoup, Comment, NavigableString, Tag

textSymbol  = 'TEXT'            # Special symbol for document text
transFile   = 'transitions.dat' # File name for the tag transition counts

# Initialize the tag transition map
transitions = {}

'''Brorrowed from the ActiveState recepies, recursive glob'''
def rglob(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
       supplied root directory.'''
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
    # transitions are saved outside of here

def parseFile(filename, transitions={}, debug=False):
    '''Parse HTML code from the given file and put the transition counts in the given dictionary'''
    print 'Parsing HTML code from input file:', filename
    # Open the HTML file and create a soup from it
    infile = open(filename, 'r')
    soup = BeautifulSoup(infile)
    infile.close()
    if debug:
        print separator('before removing junk')
        print soup.prettify()
    # Remove HTML junk from the soup
    removeJunk(soup, debug)
    if debug:
        print separator('after removing junk')
        print soup.prettify()
    # Count the tag transitions starting from the HTML root tag
    countTagTrans(soup.html, transitions, debug)

def countTagTrans(node, trans, debug=False):
    '''Count the HTML tag transitions starting from the given node'''
    # Check if the given node is a tag or string
    if isinstance(node, Tag):
        tag = node
        tagname = str(tag.name.upper())
##        if debug:
##            print 'tag name:', tag.name
##            print 'tag contents:', tag.contents
        rule = []
        # Loop over each child of the tag
        for child in tag.contents:
            # Append the child tag name and recursively count the tag transitions
            if isinstance(child, Tag):
                rule.append(str(child.name.upper()))
                countTagTrans(child, trans, debug)
            # Append the child string as a text symbol if it is not whitespace
            elif isinstance(child, NavigableString):
                if not re.match(r'^\s+$', child):
                    rule.append(textSymbol)
            else:
                print '!!! unknown child type:', child
        # Check if the tag is in the transition map
        if tagname not in trans:
            trans[tagname] = {}
        # Increment the tag -> rule transition count
        trans[tagname][tuple(rule)] = trans[tagname].get(tuple(rule), 0) + 1
        if debug: print 'trans['+tagname+']['+liststr(rule)+']:', trans[tagname][tuple(rule)]
    elif debug: print '!!! non-Tag node given to countTagTrans:', node

def removeJunk(soup, debug=False):
    '''Remove junk HTML tags from the given BeautifulSoup'''
    if debug: print separator('removing junk')
    # Remove all unsupported elements
    junkTags = ['applet', 'embed', 'object', 'script', 'meta', 'link', 'style', 'img', 'a']
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

def saveTransitions(datafilename = None):
    '''Save the given transition counts to the given data file'''
    if datafilename is None:
        datafilename = transFile
    print 'Saving transition counts to data file:', datafilename
    # Open the data file and dump the n-gram counts into it
    datafile = open(datafilename, 'wb')
    pickle.dump(transitions, datafile)
    if not transitions:
        print "!!! null transition table written"
    datafile.close()

def loadTransitions(datafilename):
    '''Load the transition counts from the given data file'''
    print 'Loading transition counts from data file:', datafilename
    # Open the data file and load the n-gram counts from it
    datafile = open(datafilename, 'rb')
    transitions = pickle.load(datafile)
    if not transitions:
        print "!!! null transition table loaded"
    datafile.close()
    return transitions
