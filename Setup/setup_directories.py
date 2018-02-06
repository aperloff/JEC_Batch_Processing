#!/bin/python

import os, sys, argparse, subprocess, itertools
from textwrap import dedent

levels_library = ["","L1","L2L3","L1L2L3","L1L2L3L5","_NoPU","L2L3_NoPU"]
directories_library = ["closure", "correction", "resolution"]

'''
From http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text
and https://bitbucket.org/ruamel/std.argparse
'''
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

def main(args):
    if not args.base_path.endswith('/'): 
        args.base_path+='/'
    if not args.head_dir.endswith('/'):
        args.head_dir+='/'

    list_of_dir = [str(args.base_path+args.head_dir)]
    for dir in args.append:
        list_of_dir.append(dir)
    for dir in args.directories:
        for cor in args.levels:
            if args.strip_nopu and "NoPU" in cor:
                continue
            if dir+cor in args.ignore:
                continue
            else:
                list_of_dir.append(str(args.base_path+args.head_dir+dir+cor))

    for dir in list_of_dir:
        if args.verbose:
            print "Checking for the existence of",dir,"..."
        if not os.path.exists(dir):
            if args.verbose:
                print "\tMaking directory",dir
            os.makedirs(dir)

    print "Final directory structure:"
    os.system("tree -a "+args.base_path+args.head_dir)

if __name__ == '__main__':
    #program name available through the %(prog)s command
    #can use prog="" in the ArgumentParser constructor
    #can use the type=int option to make the parameters integers
    #can use the action='append' option to make a list of options
    parser = argparse.ArgumentParser(description="Setup the directory structure of the folder used to create a given JEC era.",
                                     epilog="And those are the options available. Deal with it.",
                                     formatter_class=SmartFormatter)
    parser.add_argument("-a", "--append", help="Folders to create that don't fit an easily defined pattern.",
                        nargs='+', default=[], metavar='')
    parser.add_argument("-b", "--base_path", help="The base path to the folder that stores all JEC eras (i.e. the folder containing the hear directory.",
                        default=os.environ['PWD'])
    parser.add_argument("-d", "--directories", help="Space separated list of directory names to be created. Allowed directory names are "+", ".join(directories_library),
                        nargs='+', choices=directories_library, default=["closure","correction"], metavar='')
    parser.add_argument("--debug", help="Shows some extra information in order to debug this program",
                        action="store_true")
    parser.add_argument("head_dir", help="The head directory of the JEC era (i.e. the folder containing the directory structure to be created).)")
    parser.add_argument("-i","--ignore", help="Patterns of folders to ignore",
                        nargs='+', type=str, default=[], metavar='')
    parser.add_argument("-l", "--levels", help="Space separated list of JEC levels to append to each directory name. Allowed levels are "+", ".join("(None)" if x=="" else x for x in levels_library),
                        nargs='+', choices=levels_library, default=["","L1","L1L2L3"], metavar='')
    parser.add_argument("-s", "--strip_nopu", help="Removes directories with \"NoPU\" in the name.",
                        action="store_true", default=True)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.",
                        action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s 1.1', help=dedent("""\
                         R|Prints the current version of the code.
                         V1.0 Created the folders from a static list
                         V1.1 Implemented the argparser. A more command line based set of options.
                         """))
    args = parser.parse_args()

    if(args.debug):
        print 'Number of arguments:', len(sys.argv), 'arguments.'
        print 'Argument List:', str(sys.argv)
        print "Argument ", args

    main(args)
