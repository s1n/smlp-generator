# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Parse.py: Parses files in a corpus given at the command line

import sys, optparse
from Parser import *
from optparse import OptionParser

# Create an empty list of directory names
dirnames = []

# Read command line arguments
opts = OptionParser()
opts.add_option("--transfile", "-t", help="transition file")
opts.add_option("--debug", "-v", help="debugging output", action="store_true", default = True)
options, arguments = opts.parse_args()

# Parse files in each directory
for dir in arguments:
    print 'Parsing files in directory:', dir
    parseFilesInDir(dir, options.debug)

saveTransitions(options.transfile)
