# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Generator.py: Generates text by sampling Markov chain transitions

import random, re
from Parser import *

def generateText(transfile, filename = None, debug = False):
    '''Generates a single output document using the n-gram Markov model given a transition matrix'''
    transitions, attributes = loadTransitions(transfile)
    document = []
    generateTagTrans('HTML', transitions, attributes, document, debug)
    soup = BeautifulSoup('\n'.join(document))
    docstring = soup.prettify()
    if debug:
        print 'document length:', len(document)
        print separator('Generated HTML'), docstring
    if filename:
        print 'Writing generated HTML document to file: ', filename
        file = open(filename, 'w')
        file.write(docstring)
        file.close()

def generateTagTrans(tagname, trans, attrs, document, debug=False):
    '''Generate an HTML tag transition starting from the given tag'''
    if debug: print 'tag name:', tagname
    # Check if the tag is in the transition map
    if tagname in trans:
        # Initialize an empty tag transition rule
        transrule = ()
        # If there is only one rule, choose it as the next transition
        if len(trans[tagname]) == 1:
            transrule = trans[tagname].keys()[0]
        else:
            # Count the total number of tag transitions
            tagTransCount = sum(trans[tagname].values())
            # Generate a random integer between one and the tag transition count
            x = random.randint(1, tagTransCount)
            if debug: print 'random x:', x, 'range: 1 to', tagTransCount
            partsum = 0
            # Loop over each rule in the tag transitions
            for rule, count in trans[tagname].iteritems():
                # Calculate the rule's partial sum of transition counts
                partsum += count
                # Choose the rule with the smallest partial sum greater than x
                if x <= partsum:
                    transrule = rule
                    if debug: print 'part.sum:', partsum, 'rule:', liststr(rule)
                    break
        # Generate the tag attributes list
        attributes = generateAttrString(tagname, attrs, debug)
        # Check if the tag has no children
        if len(trans[tagname]) == 1 and '' in trans[tagname]:
            # Append a self-closing tag to the document
            document.append('<' + tagname.lower() + attributes + ' />')
        else:
            # Append an opening tag to the document
            document.append('<' + tagname.lower() + attributes + '>')
            # Loop over each symbol in the tag transition rule
            for symbol in transrule:
                # Recursively generate a tag transition for a known symbol
                if symbol in trans:
                    generateTagTrans(symbol, trans, attrs, document, debug)
                # Append the special text symbol
                elif symbol == textSymbol:
                    document.append(symbol)
                else:
                    print '!!! unknown symbol type:', symbol
            # Append a closing tag to the document
            document.append('</' + tagname.lower() + '>')
    else: print '!!! tag not in transition map:', tagname

def generateAttrString(tagname, attrs, debug=False):
    '''Generate an HTML tag attributes string for the given tag'''
    if debug: print 'tag name:', tagname
    # Check if the tag is in the attributes map
    if tagname in attrs:
        # Initialize an empty attribute list
        attrlist = ()
        # If there is only one rule, choose it as the attribute list
        if len(attrs[tagname]) == 1:
            attrlist = attrs[tagname].keys()[0]
        else:
            # Count the total number of attribute transitions
            attrTransCount = sum(attrs[tagname].values())
            # Generate a random integer between one and the attribute transition count
            x = random.randint(1, attrTransCount)
            if debug: print 'random x:', x, 'range: 1 to', attrTransCount
            partsum = 0
            # Loop over each rule in the attribute transitions
            for rule, count in attrs[tagname].iteritems():
                # Calculate the rule's partial sum of transition counts
                partsum += count
                # Choose the attribute list with the smallest partial sum greater than x
                if x <= partsum:
                    attrlist = rule
                    if debug: print 'part.sum:', partsum, 'rule:', liststr(rule)
                    break
        # Initializ an empty attribute string
        attributes = ''
        # Loop over each attribute in the attribute rule
        for attr in attrlist:
            # Initialize an empty string as attribute value
            attrvalue = ''
            # If there is only one value, choose it as the attribute value
            if len(attrs[attr]) == 1:
                attrlist = attrs[attr].keys()[0]
            else:
                # Count the total number of attribute values
                attrValueCount = sum(attrs[attr].values())
                # Generate a random integer between one and the attribute value count
                x = random.randint(1, attrValueCount)
                if debug: print 'random x:', x, 'range: 1 to', attrValueCount
                partsum = 0
                # Loop over each value in the attribute value list
                for value, count in attrs[attr].iteritems():
                    # Calculate the value's partial sum of attribute value counts
                    partsum += count
                    # Choose the value with the smallest partial sum greater than x
                    if x <= partsum:
                        attrvalue = value
                        if debug: print 'part.sum:', partsum, 'value:', liststr(value)
                        break
            # Append the attribute name and value to the attributes string
            attributes += ' ' + attr + '="' + attrvalue + '"'
        return attributes
    # If there is no rule, return an empty string
    else: return ''

def liststr(alist):
    '''Return a string representation of the given list or tuple'''
    if isinstance(alist, list) or isinstance(alist, tuple):
        return ','.join(alist)
    else:
        return ''
