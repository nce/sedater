# ./sedater/options.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Thu, 10.12.2015 - 19:04:12

import argparse

class CLIParser(object):
    """
    Parses the commandline arguments.

    Refer to the source code for available commandline options.
    """

    def parseForSedater(self, arguments):
        """
        :param list arguments: List of commandline arguments
        :return: Indicator of the successful cli parsing
        :rtype: bool
        """
        parser = argparse.ArgumentParser(
                description='A Sensor-Validation Converter Tool'
                "\n"
                "\nDocumentation available at:  "
                "http://sedater.readthedocs.org"
                "\nLatest Version available at: "
                "https://github.com/nce/sedater"
                "\n"
                "\nThis tool converts Sensor-Validation data to a more machine"
                " processable format."
                , formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-c', '--csv-headers'
                , action='store_true'
                , help='Toggle if the exported RawValidation files '
                    'should contain a header line (default: False)')
        parser.add_argument('-l', '--left-calibration'
                , help='Path to the calibration file for the left sensor.'
                    ' The file is necessary for a normalization of the sensors'
                    ' RawValidation data')
        parser.add_argument('-r', '--right-calibration'
                , help='Path to the calibration file for the right sensor'
                    ' The file is necessary for a normalization of the sensors'
                    ' RawValidation data')
        parser.add_argument('-o', '--output-dir'
                , help='Directory where the exported data will be stored')
        parser.add_argument('inputSource'
                , nargs='+'
                , help='Directory or file which should be crawled for'
                    ' Validationfiles')

        self.args = parser.parse_args(arguments)

        return True
