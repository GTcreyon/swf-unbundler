#!/usr/bin/python

import sys
import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('input', help='input file name')
argparser.add_argument('-o', '--output', help='output file name; omitting will print to stdout')
argparser.add_argument('-v', '--verbose', help='print verbose output', action='store_true')
args = argparser.parse_args()

# open input file
file_in = open(args.input, 'rb')
if args.verbose:
    print('File opened successfully')

# a 32-bit integer 0xFA123456 marks this as a SWF bundle
# the next 32-bit integer stores the SWF length in bytes
file_in.seek(-8, 2)
if int.from_bytes(file_in.read(4), 'little') == 0xFA123456:
    if args.verbose:
        print('SWF marker found, this is probably a SWF bundle')
    
    # get the SWF length in bytes
    swf_length = int.from_bytes(file_in.read(4), 'little')
    if args.verbose:
        print('SWF length:', swf_length)
    
    # seek backwards by that number of bytes, back to the start of the SWF
    file_in.seek(-8 - swf_length, 2)

    # read the SWF and save it to the output file
    if args.output == None:
        if args.verbose:
            print('Printing to stdout')
        print(file_in.read(swf_length))
    else:
        file_out = open(args.output, 'wb')
        if args.verbose:
            print('Output file:', args.output)
        file_out.write(file_in.read(swf_length))
        print('Successfully unbundled SWF to output file %s! Make sure to check the output file.' % args.output)
        file_out.close()
else:
    print('ERROR: No SWF file detected.', file=sys.stderr)

file_in.close()
