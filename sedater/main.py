# ./sedater/sedater/main.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Fri, 02.10.2015 - 14:45:02 
# Modified: Mon, 05.10.2015 - 12:58:42

from lib import options

import sys

if __name__ == "__main__":
	cli = options.CLIParser()
	if not cli.parseForSedater(sys.argv[1:]):
		sys.exit(2)

