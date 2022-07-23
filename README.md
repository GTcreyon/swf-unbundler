# SWF Unbundler
A python tool to extract SWF files from Flash projector executable bundles.

## Dependencies
- [Python](https://www.python.org/downloads)

## Usage
1. Download unbundle.py
2. Open a command line (CMD, PowerShell, Bash, Terminal, etc.) in the directory containing unbundle.py
3. Run `python unbundle.py <path to input file>` (might be `python3` instead of `python`)

## Additional Arguments
- \-o, \--output
	+ Specifies the path of the output file
	+ Omitting this will print to stdout
- \-v, \--verbose
	+ Displays verbose output
- \-e, \--executable
	+ Retrieves the executable instead of the SWF

## Credit
http://www.nullsecurity.org/article/extracting_swf_from_flash_projector
