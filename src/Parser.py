# Alan Davis - Statistical NLP Project - 4/26/09
# Parser.py: Parses HTML documents and counts tag transitions

import glob, re, pprint, pickle
from BeautifulSoup import BeautifulSoup, Comment, NavigableString, Tag

dataExt   = '.dat'          # File name extension for data files
transFile = 'transitions'   # File name for transition counts

def parseFilesInDir(directory, debug=False):
    '''Parse all HTML files inside the given directory'''
    if not directory.endswith('/'):
        directory += '/'
    # Find the file names of all HTML files
    filenames = glob.glob(directory + '*htm*')
    # Initialize the tag transition map
    transitions = {}
    # Loop over all file names in sorted order
    for filename in sorted(filenames):
        # Parse the HTML file
        parseFile(filename, transitions, debug)
    if debug:
        print 'Transitions Map:'
        pprint.pprint(transitions)
    # Save the transition counts, n-gram counts, and statistics to the data files
    saveTransitions(transitions, directory + transFile + dataExt)

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
    '''Count the HTML tag tranitions starting from the given node'''
    # Check if the given node is a tag or string
    if isinstance(node, Tag):
        tag = node
        tagname = str(tag.name.upper())
##        if debug:
##            print 'tag name:', tag.name
##            print 'tag contents:', tag.contents
        rule = []
        for child in tag.contents:
            if isinstance(child, Tag):
                rule.append(str(child.name.upper()))
                countTagTrans(child, trans, debug)
            elif isinstance(child, NavigableString):
                if not re.match(r'^\s+$', child):
                    rule.append('TEXT')
            else:
                print '!!! unknown child type:', child
        if tagname not in trans:
            trans[tagname] = {}
        trans[tagname][tuple(rule)] = trans[tagname].get(tuple(rule), 0) + 1
        if debug: print 'trans['+tagname+']['+liststr(rule)+']:', trans[tagname][tuple(rule)]
    elif debug: print '!!! non-Tag node given to countTagTrans:', node

def liststr(alist):
    '''Return a string representation of the given list'''
    if isinstance(alist, tuple) or isinstance(alist, list):
        return ','.join(alist)
    else:
        return ''

def removeJunk(soup, debug=False):
    '''Remove junk HTML tags from the given BeautifulSoup'''
    if debug:
        print separator('removing junk')
    # Remove all script, style, meta, link, object, embed, applet, and img elements
    junkTags = ['script', 'style', 'meta', 'link', 'object', 'embed', 'applet', 'img']
    junkElements = []
    for junkTag in junkTags:
        junkElements += soup.findAll(junkTag)
    for junkElement in junkElements:
        junkElement.extract()
        if debug: print 'junk:', junkElement
    # Remove all comments
    for comment in soup.findAll(text=isComment):
        comment.extract()
        if debug: print 'comment:', comment.strip()

def isComment(text):
    '''Return true if the given text is an instance of Comment'''
    # Return true if text is a comment
    return isinstance(text, Comment)

def separator(title):
    return '\n---------- ' + title + ' ----------'

def saveTransitions(transitions, datafilename):
    '''Save the given transition counts to the given data file'''
    print 'Saving transition counts to data file:', datafilename
    # Open the data file and dump the n-gram counts into it
    datafile = open(datafilename, 'wb')
    pickle.dump(transitions, datafile)
    datafile.close()

def loadTransitions(datafilename):
    '''Load the transition counts from the given data file'''
    print 'Loading transition counts from data file:', datafilename
    # Open the data file and load the n-gram counts from it
    datafile = open(datafilename, 'rb')
    transitions = pickle.load(datafile)
    datafile.close()
    return transitions
