# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Generate.py: Generates text by sampling Markov chain transitions

import sys, optparse
from Generator import *
from optparse import OptionParser

# Read command line arguments
opts = OptionParser()
opts.add_option('--transfile', '-t', help='transition file')
opts.add_option('--output', '-o', help='generated HTML file')
opts.add_option('--debug', '-v', help='debugging output', action='store_true')
options, arguments = opts.parse_args()

# Generate an HTML document using the specified transition file
generateText(options.transfile, options.output, options.debug)
