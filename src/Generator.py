# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Generator.py: Generates text by sampling Markov chain transitions

import random, re
from Parser import *

def generateTextFromDir(directory, filename=None, debug=False):
    '''Generate text using the n-gram Markov model in the given directory'''
    if not directory.endswith('/'):
        directory += '/'
    # Load the transition counts from the data files
    trans = loadTransitions(directory + transFile)
    # Initialize the statistics
##    tagCount = 0
    # Initialize a document with the HTML tag
    document = []
    generateTagTrans('HTML', trans, document, debug)
    # Print the statistics
##    print 'Tag Count: ', tagCount
    # Print a pretty version of the document
    soup = BeautifulSoup('\n'.join(document))
    docstring = soup.prettify()
    if debug:
        print 'document length:', len(document)
        print separator('Generated HTML'), docstring
    # Write the generated document to the file
    if filename:
        print 'Writing generated HTML document to file:', filename
        file = open(filename, 'w')
        file.write(docstring)
        file.close()

def generateTagTrans(tagname, trans, document, debug=False):
    '''Generate an HTML tag transition starting from the given tag'''
    tagname = str(tagname.upper())
    if debug: print 'tag name:', tagname
    # Check if the tag is in the transition map
    if tagname in trans:
        transrule = ()
        # If there is only one rule, choose it as the next transition
        if len(trans[tagname]) is 1:
            transrule = trans[tagname].keys()[0]
        else:
            # Count the total number of tag transitions
            tagTransCount = sum(trans[tagname].values())
            # Generate a random integer between one and the tag transition count
            x = random.randint(1, tagTransCount)
            if debug: print 'random x:', x, 'range: 1 to', tagTransCount
            partsum = 0
            # Loop over each rule in the tags transitions
            for rule, count in trans[tagname].iteritems():
                # Calculate the rule's partial sum of transition counts
                partsum += count
                # Choose the rule with the smallest partial sum greater than x
                if x <= partsum:
                    transrule = rule
                    if debug: print 'part.sum:', partsum, 'rule:', liststr(rule)
                    break
        # Append the opening tag to the document
        document.append('<' + tagname.lower() + '>')
        # Loop over each symbol in the tag transition rule
        for symbol in transrule:
            # Recursively generate a tag transition for a known symbol
            if symbol in trans:
                generateTagTrans(symbol, trans, document, debug)
            # Append the special text symbol
            elif symbol == textSymbol:
                document.append(symbol)
            else:
                print '!!! unknown symbol type:', symbol
        # Append the closing tag to the document
        document.append('</' + tagname.lower() + '>')
    elif debug: print '!!! tag not in transition map:', tag

def liststr(alist):
    '''Return a string representation of the given list or tuple'''
    if isinstance(alist, list) or isinstance(alist, tuple):
        return ','.join(alist)
    else:
        return ''
