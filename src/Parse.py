# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Parse.py: Parses files in a corpus given at the command line

import sys, optparse
from Parser import *
from optparse import OptionParser

# Read command line arguments
opts = OptionParser()
opts.add_option('--debug', '-v', help = 'enable debugging output', action='store_true')
opts.add_option('--progressive', '-p', help = 'continues the previous parsing', action='store_true')
opts.add_option('--objfile', '-o', help = 'object output file')
options, arguments = opts.parse_args()

# Parse files in each directory
p = Parser(options.objfile, options.progressive, options.debug)
for dir in arguments:
    print 'Parsing files in directory:', dir
    p.parseFilesInDir(dir)

# Save the transitions map
if arguments and not options.progressive:
    p.freeze()
