# ./sedater/export.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 08.11.2015 - 22:21:45 
# Modified: Sun, 08.11.2015 - 23:08:56

class Exporter(object):
    """
    Exports the compiled data.

    The data collected by either binary or text files (and ready for 
    exportation), will be written to the filesystem.
    """

    def __init__(self):
        pass

class CSVExporter(Exporter):

    def export(self, segments, exportLocation):
        """
        Exports the given segments to a specific file in CSV notation

        :param segments: A list (array) of segments which should be exported to 
        the same file
        :type segments: list of :class:`sedater.lib.shared.Sensorsegment`
        :param exportLocation: export path location (incl. filename)
        :type exportLocation: str
        :return: Indication whether the export succeeded
        :rtype: Boolean
        """

        try:
            with open(exportLocation, 'w') as exportFile:
                # TODO: with headers, with indices
                exp = csv.writer(exportFile)
                exp.writerows([(value.accelX, value.accelY, value.accelZ,
                        value.gyroX, value.gyroY, value.gyroZ) for value in segments])
        except Exception as e:
            # TODO: handle common exceptions
            raise e

        return True
