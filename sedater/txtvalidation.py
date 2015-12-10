# ./sedater/txtvalidation.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Tue, 10.11.2015 - 12:22:28 
# Modified: Thu, 10.12.2015 - 17:16:13

import csv, re, os

from sedater.lib import shared as lib

class TxtConverter(object):
    """
    Imports and processes TextValidation files.

    The processed TextValidation files are stored in:
    :class:`self.validationData` as 
    ``list(``:class:`Validationfile <lib.shared.Validationfile>` ``)``

    :param filesToConvert: Files which might contain valid Validationinformation
    :type filesToConvert: list(:class:`Sourcefile <lib.shared.Sourcefile>`)
    """
    def __init__(self, filesToConvert):
        self.filesToConvert = filesToConvert
        self.validationData = []
    def processTxtFiles(self):
        for txtPair in self.filesToConvert:
            for i in range(len(txtPair)):
                # skip all non '.txt' files
                if '.txt' != os.path.splitext(txtPair[i].filename)[1]: continue
                self.validationData.append(self.parseTxtFile(txtPair[i]))

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
        :type sourcefile: :class:`Sourcefile <lib.shared.Sourcefile>`
        :return: the meta information and validation-data
        :rtype: :class:`Validationfile <lib.shared.Validationfile>`
        """
        validationType = ''

        with open(sourcefile.path + '/' + sourcefile.filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            i          = 0
            s          = 0
            attributes = []
            content    = []
            for row in reader:
                if re.match('^[0-9]+', row[0]): break
                if row[0] == 'ValidationType': validationType = row[1].strip()
                i = i+1
                attributes.append(list(map(str.strip, row)))

            # set the line indicator one lines up
            i = i - 1
            # reread the whole file
            csvfile.seek(0)
            # remove last element (which are the headers for the content)
            attributes.pop()

            # scroll file until previously determined start of content
            while s < i:
                csvfile.readline()
                s = s + 1

            # sometime the header have trailing spaces, remove them
            header = [h.strip() for h in csvfile.readline().split(',')]
            # now parse all the content into a tmp dictionary
            d = csv.DictReader(csvfile, fieldnames=header)
            for row in d:
                content.append(row)

        return lib.Validationfile._make([
              sourcefile
            , validationType
            , attributes
            , content
            ])
