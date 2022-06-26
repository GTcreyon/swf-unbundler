#!/usr/bin/python

import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('input', help='input file name')
argparser.add_argument('-o', '--output', help='output file name')
argparser.add_argument('-v', '--verbose', help='print verbose output', action='store_true')
args = argparser.parse_args()

# give output file name a default suffix if none is specified
if args.output == None:
    file_name_out = str(args.input) + '_unbundled.swf'
    if args.verbose:
        print('No output specified, defaulting to', file_name_out)
else:
    file_name_out = str(args.output)
    if args.verbose:
        print('Output file:', file_name_out)

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
    file_out = open(file_name_out, 'wb')
    file_out.write(file_in.read(swf_length))
    file_out.close()
    print('Successfully unbundled SWF to output file %s! Make sure to check the output file.' % file_name_out)
else:
    print('ERROR: No SWF file detected.')

file_in.close()