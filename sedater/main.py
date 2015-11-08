# ./sedater/sedater/main.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Fri, 02.10.2015 - 14:45:02 
# Modified: Sat, 07.11.2015 - 17:30:28

from sedater.options import CLIParser

import sys


if __name__ == "__main__":
    cli = CLIParser()
    if not cli.parseForSedater(sys.argv[1:]):
        sys.exit(2)

