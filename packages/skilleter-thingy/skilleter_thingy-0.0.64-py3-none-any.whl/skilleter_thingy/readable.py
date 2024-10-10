#! /usr/bin/env python3

################################################################################
""" Pipe for converting colour combinations to make them readable

    Defaults to making things readable on a light background but has the
    option to make things readable on a dark background or for removing
    colours altogether
"""

# TODO: Not sure it works properly as a pipe
# TODO: Error handling in file I/O

################################################################################

import sys
import argparse
import tempfile
import os
import re
import filecmp
import shutil
import logging

from thingy import tidy
from thingy import files

################################################################################

TF_IGNORE_MSG = 'Unless you have made equivalent changes to your configuration, or ignored the relevant attributes using ignore_changes, the following plan may include actions to undo or respond to these changes.'

TF_REFRESHING_AND_READING = re.compile(r'.*: (?:Refreshing state\.\.\.|Reading\.\.\.|Still reading\.\.\.|Read complete after |Preparing import\.\.\.).*')
TF_FINDING_AND_INSTALLING = re.compile(r'- (?:Finding .*[.]{3}|Installing .*[.]{3}|Installed .*)')
TF_FETCHING_AND_INSTALLING = re.compile(r'(Fetching|Installing|Using) [-a-z0-9_]+ [0-9.]+')

TF_UNCHANGED_HIDDEN = re.compile(r' +# \(\d+ unchanged (?:attribute|block|element)s? hidden\)')

TF_HAS_CHANGED = re.compile(r'  # .* has changed')
TF_HAS_CHANGED_END = re.compile(r'    [}]')

TF_READ_DURING_APPLY = re.compile(r' +# [-a-z_.0-9\[\]]+ will be read during apply')
TF_READ_DURING_APPLY_END = re.compile(r'    [}]')

TF_TAG_CHANGE_BLOCK_START = re.compile(r'^ +~ +tags(_all)? += +\{$')
TF_TAG_ENTRY_IGNORE = re.compile(r'^ +".*" += +".*"')
TF_TAG_CHANGE_BLOCK_END = re.compile(r'^ +}$')

TF_MISC_REGEX = \
[
    { 'regex': re.compile(r'(Read complete after) (\d+s|\d+m\d+s)'), 'replace': r'\1 {ELAPSED}'},
    { 'regex': re.compile(r'"(.*:.*)"( = ".*")'), 'replace': r'\1\2'},
    { 'regex': re.compile(r'"(.*:.*)"( = \[$)'), 'replace': r'\1\2'},
    { 'regex': re.compile(r'^last "terraform apply":$'), 'replace':r'last "terraform apply" which may have affected this plan:'},
]

TF_IGNORE_LIST = [
    {'start': TF_HAS_CHANGED, 'end': TF_HAS_CHANGED_END},
    {'start': TF_READ_DURING_APPLY, 'end': TF_READ_DURING_APPLY_END},
    {'start': re.compile(r'(Releasing|Acquiring) state lock. This may take a few moments\.+')},
    {'start': re.compile(r'.*: Still reading\.{3} \[.* elapsed\]')},
]

################################################################################

def parse_command_line():
    """ Parse, check and sanitise the command line arguments """

    parser = argparse.ArgumentParser(description='Read from standard input and write to standard output modifying ANSI colour codes en-route.')

    parser.add_argument('-l', '--light', action='store_true', help='Modify colours for a light background (the default)')
    parser.add_argument('-d', '--dark', action='store_true', help='Modify colours for a dark background')
    parser.add_argument('-n', '--none', action='store_true', help='Remove all colour codes')
    parser.add_argument('-t', '--tidy', action='store_true',
                        help='Remove colour codes and stuff that typically occurs in log files causing diffs, but is of no particular interest (e.g. SHA1 values, times, dates)')
    parser.add_argument('-s', '--strip-blank', action='store_true', help='Strip all blank lines')
    parser.add_argument('-D', '--debug', action='store_true', help='Replace colours with debug information')
    parser.add_argument('-o', '--out', action='store_true', help='Output to standard output rather than overwriting input files')
    parser.add_argument('-O', '--dir', action='store', default=None, help='Store output files in the specified directory (creating it if it doesn\'t exist)')
    parser.add_argument('-a', '--aws', action='store_true', help='Remove AWS resource IDs')
    parser.add_argument('-T', '--terraform', action='store_true', help='Clean Terraform plan/apply log files')
    parser.add_argument('-R', '--replace', action='append', default=None, help='Additional regex replacements in the form "REGEX=REPLACEMENT"')
    parser.add_argument('-v', '--verbose', action='store_true', help='Output verbose status')
    parser.add_argument('files', nargs='*', default=None, help='The files to convert (use stdin/stout if no input files are specified)')

    args = parser.parse_args()

    # Enable logging, if requested

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info('Logging enabled')

    # Can't do more than one transformation

    if args.light + args.dark + args.none + args.debug > 1:
        print('ERROR: Only one colour conversion option can be specified')
        sys.exit(1)

    if args.tidy and (args.light or args.dark or args.debug):
        print('ERROR: The tidy and colour conversion options cannot be specified together')
        sys.exit(1)

    # Default to doing cleanup - removing colour codes, times & Terraform cleanup

    if not args.light and not args.dark and not args.tidy and not args.strip_blank and not args.terraform:
        args.strip_blank = args.none = args.tidy = args.terraform = True
        logging.info('No options specified - defaulting to stripping blanks, removing colour codes, tidying and cleaning Terraform data')

    # Terraform option also removes ANSI, etc.

    if args.terraform:
        args.strip_blank = args.tidy = args.none = True

    # Create the output directory, if required

    if args.dir and not os.path.isdir(args.dir):
        logging.info('Creating output directory %s', args.dir)

        os.mkdir(args.dir)

    # Handle additional regex replacements

    if args.replace:
        args.regex_replace = []
        for entry in args.replace:
            regex, replace = entry.split('=')
            try:
                args.regex_replace.append({'regex': re.compile(regex), 'replace':replace})
            except re.error as exc:
                print(f'ERROR in regular expression {regex}: {exc}')
                sys.exit(1)

    return args

################################################################################

def cleanfile(args, infile, outfile):
    """ Clean infile, writing to outfile.
        Returns True if any changes were made. """

    # Keep the previous line so that we can skip multiple blank lines

    prev_line = None

    # Set if we are ignoring a block - contains a regex for the end-of-ignore marker

    ignore_until = None

    # Collects data that we are going to output in alphabetical order

    collection = []

    # True if we are processing a tag block

    in_tag_block = False

    # Read, process and write stdin to stdout, converting appropriately

    for data in infile:
        # Remove the trailing newline

        if data[-1] == '\n':
            data = data[:-1]

        # Strip trailing whitespace

        data = data.rstrip()

        # Do colour code conversion

        if args.debug:
            clean = tidy.debug_format(data)
        elif args.light:
            clean = tidy.convert_ansi(data, True)
        elif args.dark:
            clean = tidy.convert_ansi(data, False)
        elif args.none:
            clean = tidy.remove_ansi(data)
        else:
            clean = data

        # Do tidying

        if args.tidy:
            clean = tidy.remove_sha256(clean)
            clean = tidy.remove_sha1(clean)
            clean = tidy.remove_times(clean)
            clean = tidy.remove_speeds(clean)

            if not args.light and not args.dark:
                clean = tidy.remove_ansi(clean)

        # Remove AWS ID values

        if args.aws:
            clean = tidy.remove_aws_ids(clean)

        # Additional custom regex replacements

        if args.replace:
            for entry in args.regex_replace:
                clean = entry['regex'].sub(entry['replace'], clean)

        # Do things with Terraform log data

        if args.terraform:
            clean = tidy.regex_replace(clean, TF_MISC_REGEX)

            for ignore in TF_IGNORE_LIST:
                if ignore['start'].fullmatch(clean):
                    if 'end' in ignore:
                        ignore_until = ignore['end']

                        logging.info('Found ignore start marker: "%s"', clean)
                        logging.info('Skipping until end marker: "%s"', ignore_until.pattern)
                    else:
                        clean = None

                    break
            else:
                if TF_TAG_CHANGE_BLOCK_START.fullmatch(clean):
                    in_tag_block = True

                elif TF_TAG_CHANGE_BLOCK_END.fullmatch(clean):
                    in_tag_block = False

                elif TF_UNCHANGED_HIDDEN.fullmatch(clean):
                    clean = None

                elif clean == TF_IGNORE_MSG:
                    clean = None

                elif TF_REFRESHING_AND_READING.match(clean) or TF_FINDING_AND_INSTALLING.fullmatch(clean) or TF_FETCHING_AND_INSTALLING.fullmatch(clean):
                    # Collect a block of non-deterministically-ordered data

                    collection.append(clean)
                    clean = None

                elif collection:
                    # If we collected a block, write it out in sorted order

                    logging.info('Outputting collection of %d lines of sorted text', len(collection))

                    collection.sort()
                    for entry in collection:
                        outfile.write(entry)
                        outfile.write('\n')

                    collection = []

            if in_tag_block and clean and TF_TAG_ENTRY_IGNORE.fullmatch(clean):
                clean = None

        # Write normal output, skipping >1 blank lines

        if clean is not None and not ignore_until:
            if clean != '' or prev_line != '':
                outfile.write(clean)
                outfile.write('\n')

            prev_line = clean

        # Clear the ignore flag if we've hid the end marker of the block

        if ignore_until and clean and ignore_until.fullmatch(clean):
            ignore_until = None
            logging.info('Hit end of ignore section')

    # If we've hit the end and are still ignoring stuff, something's up!

    if ignore_until:
        print(f'INTERNAL ERROR: Code never found end of ignore-block marker "{ignore_until.pattern}" - either the Terraform output format has changed, or the log file is incomplete!')
        sys.exit(2)

    if in_tag_block:
        print('INTERNAL ERROR: Code never found end of tag block marker - either the Terraform output format has changed, or the log file is incomplete!')
        sys.exit(2)

################################################################################

def main():
    """ Main code """

    # Process command line options

    args = parse_command_line()

    # We are either processing 1 or more files, or just piping stdin to stdout

    if args.files:
        try:
            for filename in args.files:
                with open(filename, 'rt') as infile:

                    # Either write to stdout or to a temporary file

                    if args.out:
                        outfile = sys.stdout
                        outfile_name = None
                    else:
                        outfile = tempfile.NamedTemporaryFile(mode='wt+', delete=False)
                        outfile_name = outfile.name

                    cleanfile(args, infile, outfile)

                    if outfile_name:
                        outfile.close()

                # If we wrote to an output file then do something

                if outfile_name:
                    if args.dir:
                        # Writing to a directory - just move the output file there unconditionally

                        shutil.move(outfile_name, os.path.join(args.dir, os.path.basename(filename)))

                    elif not filecmp.cmp(outfile_name, filename, shallow=False):
                        # Only backup and write the source file if changes have been made (original is
                        # left in place without a backup if nothing's changed)

                        files.backup(filename)

                        shutil.move(outfile_name, filename)

                    else:
                        # Output file hasn't been used, so just delete it

                        os.unlink(outfile_name)

        except FileNotFoundError as exc:
            print(exc)
            sys.exit(1)

    else:
        cleanfile(args, sys.stdin, sys.stdout)

################################################################################

def readable():
    """Entry point"""

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(2)

################################################################################

if __name__ == '__main__':
    readable()
