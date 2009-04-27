# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Parse.py: Parses files in a corpus given at the command line

import sys
from Parser import *

# Create an empty list of directory names
dirnames = []
debug = False

# Read command line arguments
for arg in sys.argv[1:]:
    # Read the directory names
    if not arg.startswith('-'):
        dirnames.append(arg)
    # Turn debugging mode on
    elif arg == '-debug':
        print '--- debugging mode on ---'
        debug = True

# Parse files in each directory
for dirname in dirnames:
    print 'Parsing files in directory:', dirname
    parseFilesInDir(dirname, debug)

# Print a help prompt to the user
if len(dirnames) == 0:
    print 'Usage:   Parse.py dirname1, dirname2, ... [-debug]'

# Change the directory or filename here to test
test = False
if test:
    # Parse text in a test directory or file
    dirname = '../corpus/' + 'test/'##'MrX/'
    filename = dirname + 'example.html'##'bagels.htm'##
    debug = True##False##
    parseFilesInDir(dirname, debug)
##    parseFile(filename, debug=debug)
