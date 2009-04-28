# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Generate.py: Generates text by sampling Markov chain transitions

import sys, optparse
from Generator import *
from optparse import OptionParser

# Create an empty list of directory names
transfile = 'transitions.dat'
output = 'test.html'
debug = False

# Read command line arguments
opts = OptionParser()
opts.add_option("--transfile", "-t", help="transition file")
opts.add_option("--output", "-o", help="markov generated output file")
opts.add_option("--debug", "-v", action="store_true", help="debugging output")
options, arguments = opts.parse_args()

generateText(options.transfile, options.output, options.debug)
