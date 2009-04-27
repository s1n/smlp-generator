# Statistical NLP Project - 4/26/09
# Alan Davis, Jason Switzer, Ryan Garabedian
# Generate.py: Generates text by sampling Markov chain transitions

import sys
from Generator import *

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
    print 'Generating a test file in directory:', dirname
    generateTextFromDir(dirname, dirname + 'test.html', debug)

# Print a help prompt to the user
if len(dirnames) == 0:
    print 'Usage:   Generate.py dirname1, dirname2, ... [-debug]'

# Change the directory or filename here to test
test = False
if test:
    # Generate text in a test directory or file
    dirname = '../corpus/' + 'test/'##'MrX/'
    filename = dirname + 'example.html'##'bagels.htm'
    debug = True
    # Test the generate text function
    generateTextFromDir(dirname, dirname + 'test.html', debug=True)
