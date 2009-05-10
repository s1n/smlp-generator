# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Generate.py: Generates text by sampling Markov chain transitions

import sys, optparse
from Generator import *
from optparse import OptionParser

# Read command line arguments
opts = OptionParser()
opts.add_option('--objfile', '-o', help='transition file')
opts.add_option('--textfile', '-t', help='TEXT elements file')
opts.add_option('--result', '-r', help='generated HTML file')
opts.add_option('--debug', '-v', help='debugging output', action='store_true')
options, arguments = opts.parse_args()

# Generate an HTML document using the specified transition file
g = Generator(options.objfile, options.textfile, options.result, options.debug)
g.generateText()
