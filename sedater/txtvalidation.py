# ./sedater/txtvalidation.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Tue, 10.11.2015 - 12:22:28 
# Modified: Tue, 10.11.2015 - 20:20:47

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
        :param sourcefile: path to the validation-text file
        :type sourcefile: :class:`Sourcefile <sedater.lib.shared.Sourcefile`
        """
        with open(sourcefile.path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            i          = 0
            s          = 0
            attributes = []
            content    = []
            for row in reader:
                i = i+1
                attributes.append(row)

                if re.match('^[0-9]+', row[0]): break
            i = i - 2               # set the line indicator two lines up
            csvfile.seek(0)         # scroll back filedescriptor position
            attributes.pop() * 2    # remove said last two elements

            # reread the whole file
            while s < i:
                csvfile.readline()
                s = s + 1
            # until previously determined start of content
            # now parse all the content into a tmp dictionary
            d = csv.DictReader(csvfile)
            for row in d:
                content.append(row)

            return attributes
