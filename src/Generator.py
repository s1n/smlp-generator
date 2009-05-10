# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Generator.py: Generates text by sampling Markov chain transitions

import random, re, sys, traceback
from Parser import *

p = None

class Generator:

    def __init__(self, objfile, textfile, resultfile, indebug = False):
        global p
        self.result = resultfile
        self.debug = indebug
        p = Parser(objfile, True, True)
        #p.TEXTelems = p.load(textfile, 'rb')
        #sys.setrecursionlimit(sys.getrecursionlimit() * 10)

    def generateText(self):
        '''Generates a single output document using the n-gram Markov model given a transition matrix'''
        global p
        document = []
        self.generateTagTrans('HTML', document)
        soup = BeautifulSoup('\n'.join(document))
        docstring = soup.prettify()
        p.dprint('document length:', len(document))
        p.dprint(p.separator('Generated HTML'), docstring)
        if self.result:
            print 'Writing generated HTML document to file: ', self.result
            file = open(self.result, 'w')
            file.write(docstring)
            file.close()

    def generateTagTrans(self, tagname, document):
        '''Generate an HTML tag transition starting from the given tag'''
        global p
        #p.dprint('tag name:', tagname)
        # Check if the tag is in the transition map
        if tagname in p.transitions:
            # Initialize an empty tag transition rule
            transrule = ()
            # If there is only one rule, choose it as the next transition
            if len(p.transitions[tagname]) == 1:
                transrule = p.transitions[tagname].keys()[0]
            else:
                # Count the total number of tag transitions
                tagTransCount = sum(p.transitions[tagname].values())
                # Generate a random integer between one and the tag transition count
                x = random.randint(1, tagTransCount)
                p.dprint('random x:', x, 'range: 1 to', tagTransCount)
                partsum = 0
                # Loop over each rule in the tag transitions
                for rule, count in p.transitions[tagname].iteritems():
                    # Calculate the rule's partial sum of transition counts
                    partsum += count
                    # Choose the rule with the smallest partial sum greater than x
                    if x <= partsum:
                        transrule = rule
                        p.dprint('part.sum:', partsum, 'rule:', self.liststr(rule))
                        break
            print "tag:", tagname.lower()
            # Generate the tag attributes list
            attributes = self.generateAttrString(tagname)
            # Check if the tag has no children
            if len(p.transitions[tagname]) == 1 and '' in p.transitions[tagname]:
                # Append a self-closing tag to the document
                document.append('<' + tagname.lower() + attributes + ' />')
            else:
                # Append an opening tag to the document
                document.append('<' + tagname.lower() + attributes + '>')
                # Loop over each symbol in the tag transition rule
                for symbol in transrule:
                    # Append the special text symbol
                    if symbol == p.textSymbol:
                        document.append(symbol)
                    # Recursively generate a tag transition for a known symbol
                    elif symbol in p.transitions:
                        self.generateTagTrans(symbol, document)
                        #document.append(p.TEXTelems[random.randint(0, len(p.TEXTelems) - 1)])
                    else:
                        print '!!! unknown symbol type:', symbol
                # Append a closing tag to the document
                document.append('</' + tagname.lower() + '>')
        else:
            print '!!! tag not in transition map:', tagname

    def generateAttrString(self, tagname):
        '''Generate an HTML tag attributes string for the given tag'''
        global p
        #p.dprint('tag name:', tagname)
        # Check if the tag is in the attributes map
        if tagname in p.attributes:
            # Initialize an empty attribute list
            attrlist = ()
            # If there is only one rule, choose it as the attribute list
            if len(p.attributes[tagname]) == 1:
                attrlist = p.attributes[tagname].keys()[0]
            else:
                # Count the total number of attribute transitions
                attrTransCount = sum(p.attributes[tagname].values())
                # Generate a random integer between one and the attribute transition count
                x = random.randint(1, attrTransCount)
                p.dprint('random x:', x, 'range: 1 to', attrTransCount)
                partsum = 0
                # Loop over each rule in the attribute transitions
                for rule, count in p.attributes[tagname].iteritems():
                    # Calculate the rule's partial sum of transition counts
                    partsum += count
                    # Choose the attribute list with the smallest partial sum greater than x
                    if x <= partsum:
                        attrlist = rule
                        p.dprint('part.sum:', partsum, 'rule:', self.liststr(rule))
                        break
            # Initializ an empty attribute string
            attributes = ''
            # Loop over each attribute in the attribute rule
            for attr in attrlist:
                # Initialize an empty string as attribute value
                attrvalue = ''
                # If there is only one value, choose it as the attribute value
                if len(p.attributes[attr]) == 1:
                    attrlist = p.attributes[attr].keys()[0]
                else:
                    # Count the total number of attribute values
                    attrValueCount = sum(p.attributes[attr].values())
                    # Generate a random integer between one and the attribute value count
                    x = random.randint(1, attrValueCount)
                    p.dprint('random x:', x, 'range: 1 to', attrValueCount)
                    partsum = 0
                    # Loop over each value in the attribute value list
                    for value, count in p.attributes[attr].iteritems():
                        # Calculate the value's partial sum of attribute value counts
                        partsum += count
                        # Choose the value with the smallest partial sum greater than x
                        if x <= partsum:
                            attrvalue = value
                            p.dprint('part.sum:', partsum, 'value:', self.liststr(value))
                            break
                # Append the attribute name and value to the attributes string
                attributes += ' ' + attr + '="' + attrvalue + '"'
            return attributes
        # If there is no rule, return an empty string
        else:
            #traceback.print_stack()
            #print "tag name:", tagname
            return ''

    def liststr(self, alist):
        '''Return a string representation of the given list or tuple'''
        if isinstance(alist, list) or isinstance(alist, tuple):
            return ','.join(alist)
        else:
            return ''
