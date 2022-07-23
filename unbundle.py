#!/usr/bin/python

import argparse
import os
import sys
argparser = argparse.ArgumentParser()
argparser.add_argument('input', help='input file name')
argparser.add_argument('-o', '--output', help='output file name; omitting will print to stdout')
argparser.add_argument('-v', '--verbose', help='print verbose output', action='store_true')
argparser.add_argument('-e', '--executable', help='retrieve executable instead of swf', action='store_true')
args = argparser.parse_args()

def main():
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
        
        if args.executable:
            # seek to the start of the file
            file_in.seek(0, 0)

            # read the executable
            data = file_in.read(os.path.getsize(args.input) - swf_length - 8)
            file_in.close()
        else:
            # seek backwards by the number of bytes indicated by the SWF length, back to the start of the SWF
            file_in.seek(-8 - swf_length, 2)

            # read the SWF
            data = file_in.read(swf_length)
            file_in.close()

        # output
        output_data(data)
    else:
        print('ERROR: No SWF file detected.', file=sys.stderr)

def output_data(data):
    if args.output == None:
        print(data) # stdout print
    else:
        file_out = open(args.output, 'wb') # save to output file
        file_out.write(data)
        file_out.close()
        print('Successfully unbundled to file %s! Make sure to check the output file.' % args.output)

main()