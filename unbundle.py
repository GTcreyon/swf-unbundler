#!/usr/bin/python

import argparse
import os
import sys
argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='input file name; omitting will read from stdin')
argparser.add_argument('-o', '--output', help='output file name; omitting will print to stdout')
argparser.add_argument('-v', '--verbose', help='print verbose output; do NOT use when printing to stdout', action='store_true')
argparser.add_argument('-e', '--executable', help='retrieve executable instead of swf', action='store_true')
argparser.add_argument('-b', '--bundlewith', help='bundle swf with this executable instead of extracting')
args = argparser.parse_args()


def main():
    if args.input == None:
        # temporarily save pipe to a file in order to ensure seeking works
        # there might be a better way of doing this
        if args.verbose:
            print('Reading from stdin')
        stdin_data = sys.stdin.buffer.read()
        if os.path.exists('.unbundle_temp'):
            os.remove('.unbundle_temp')
            if args.verbose:
                print('Removed leftover temp file')
        file_temp = open('.unbundle_temp', 'wb')
        file_temp.write(stdin_data)
        file_temp.close()
        if args.verbose:
            print('Created temporary file')
        file_in = open('.unbundle_temp', 'rb')
        if args.verbose:
            print('File opened successfully')
        input_path = '.unbundle_temp'
    else:
        # open input file
        file_in = open(args.input, 'rb')
        if args.verbose:
            print('File opened successfully')
        input_path = args.input

    if args.bundlewith == None:
        if args.verbose:
            print('Attempting to unbundle')
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
                data = file_in.read(os.path.getsize(input_path) - swf_length - 8)
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
    else:
        if args.verbose:
            print('Attempting to bundle')
            if args.executable:
                print('Ignoring executable flag')

        if args.verbose:
            print('Reading executable')
        file_sa = open(args.bundlewith, 'rb')
        sa_data = file_sa.read()
        file_sa.close()
        if args.verbose:
            print('Read executable')

        if args.verbose:
            print('Reading SWF')
        swf_length = os.path.getsize(input_path)
        swf_data = file_in.read()
        file_in.close()
        if args.verbose:
            print('Read SWF')

        if args.verbose:
            print('Creating bundle')
        data = sa_data + swf_data + int.to_bytes(0xFA123456, 4, 'little') + int.to_bytes(swf_length, 4, 'little')
        if args.verbose:
            print('Created bundle')
            
        output_data(data)
    
    if os.path.exists('.unbundle_temp'):
        os.remove('.unbundle_temp')
        if args.verbose:
            print('Removed temp file')



def output_data(data):
    if args.output == None:
        sys.stdout.buffer.write(data) # stdout print
    else:
        file_out = open(args.output, 'wb') # save to output file
        file_out.write(data)
        file_out.close()
        print('Successfully exported to file %s! Make sure to check the output file.' % args.output)


main()