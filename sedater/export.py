# ./sedater/export.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 08.11.2015 - 22:21:45 
# Modified: Mon, 09.11.2015 - 12:12:20

import csv

from sedater.lib import shared

class Exporter(object):
    """
    Exports the compiled data.

    The data collected by either binary or text files (and ready for 
    exportation), will be written to the filesystem.
    """

    def __init__(self):
        pass

class CSVExporter(Exporter):

    def export(self, segments, exportLocation, withHeader=False, withIndices=True):
        """
        Exports the given segments to a specific file in CSV notation

        :param segments: A list (array) of segments which should be exported to \
                the same file
        :type segments: list of :class:`sedater.lib.shared.Sensorsegment`
        :param exportLocation: export path location (incl. filename)
        :type exportLocation: str
        :param withHeader: Print a header line in the csv file, indicating the \
                row attribute
        :type withHeader: Boolean
        :param withIndices: Print an Index in the first column
        :type withIndices: Boolean
        :return: Indication whether the export succeeded
        :rtype: Boolean
        """

        try:
            with open(exportLocation, 'w') as exportFile:
                # TODO: with headers, with indices
                exp = csv.writer(exportFile)
                if withHeader:
                    if withIndices:
                        # Header with indices
                        exp.writerow(['Index', *shared.Sensorsegment._fields] )
                    else:
                        # header without indices
                        exp.writerow([*shared.Sensorsegment._fields] )
                if withIndices:
                    # column with indices
                    exp.writerows([(index+1, value.accelX, value.accelY, value.accelZ,
                        value.gyroX, value.gyroY, value.gyroZ) for index,value in enumerate(segments)])
                else:
                    # column without indices
                    exp.writerows([(value.accelX, value.accelY, value.accelZ,
                        value.gyroX, value.gyroY, value.gyroZ) for value in segments])

        except Exception as e:
            # TODO: handle common exceptions
            raise e

        return True
