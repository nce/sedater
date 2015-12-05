# ./sedater/txtvalidation.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Tue, 10.11.2015 - 12:22:28 
# Modified: Sat, 05.12.2015 - 16:59:13

import csv
import re

class TxtConverter(object):
    """
    """
    def __init__(self, filesToConvert):
        self.filesToConvert = filesToConvert
    def processTxtFiles(self):
        for txtPair in self.filesToConvert:
            for i in range(len(txtPair)):
                # skip all non '.txt' files
                if '.txt' != os.path.splitext(rawPair[i].filename)[1]: continue
                self.parseTxtFile(rawPair[i])

    def parseTxtFile(self, sourcefile):
        """
        Parses ``.txt`` sensor files.

        The validation-text files provide some metainformation, as well as the
        validation-data. In the example below, line 1-3 provide meta information 
        in the  ``<property>,<value>`` schema (often with trailing ``,``).

        line 4 is the header line for the following contents, starting in line 5.
        This content is referred to as validation-data

        .. code-block:: none
            :linenos:

            Meta1,Foo,,,,
            Meta2,Bar,,,,
            Meta3,Baz,,,,
            Start,End
            1,2
            3,4
            5,6

        *Note: most of the sensor-validation files i aquired had an invalid\
            csv syntax. So we don't solely rely on the csv reading capabilites.*

        :param sourcefile: path to the validation-text file
        :type sourcefile: :class:`Sourcefile <sedater.lib.shared.Sourcefile>`
        :return: the meta information and validation-data
        :rtype: tuple of ``list`` of ``list`` (storing metainformation) and 
            ``list`` of ``dictionary`` (storing validation-data)
        """
        with open(sourcefile.path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            i          = 0
            s          = 0
            attributes = []
            content    = []
            for row in reader:
                if re.match('^[0-9]+', row[0]): break
                i = i+1
                attributes.append(row)

            i = i - 1               # set the line indicator two lines up
            csvfile.seek(0)         # scroll back filedescriptor position
            attributes.pop()        # remove said last two elements

            # reread the whole file
            while s < i:
                csvfile.readline()
                s = s + 1
            # scroll file until previously determined start of content
            # now parse all the content into a tmp dictionary
            d = csv.DictReader(csvfile)
            for row in d:
                content.append(row)

            return (attributes, content)
