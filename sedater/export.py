# ./sedater/export.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 08.11.2015 - 22:21:45 
# Modified: Sat, 05.12.2015 - 18:05:42

import csv

import sys

from sedater.lib import shared

class Exporter(object):
    """
    Exports the compiled data.

    The data collected by either binary or text files (and ready for 
    exportation), will be written to the filesystem.
    """

    def __init__(self):
        pass

class XMLExporter(Exporter):
    def __init__(self, session, exercise, exportLocation):
        """
        Exports the given validation to a specific file in XML notation

        :param str session: The releated session
        :param str exercise: The related exercise
        :param str exportLocation: Path to the export directory
        """

        self.session  = session
        self.exercise = exercise
        self.exportLocation = exportLocation
        self.annotationFile = 'annotation.xml'
    def export(self, validationdata):
        """
        :param validationdata: The parsed :class:`Textfile <sedater.txtvalidation.TxtConverter.parseTxtFile>`
        :param type validationdata: tuple of ``list`` of ``list`` and ``list`` of ``dictionary``
        """

        filename = 'annotation.xml'
        self._exportMetaInformationToXml(filename)

    def _exportMetaInformationToXML(self, annotationFile):
        """
        Exports the metainformation to a seperate XML file

        :param str annotationFile: Full path to the annotation file
        """
        filename = 'metainformation.xml'

        # Build XML structure
        document = et.Element('meta')

        session = et.SubElement(document, 'Session')
        session.text = self.session

        exercise = et.SubElement(document, 'Exercise')
        exercise.text = self.exercise

        annotation = et.SubElement(document, 'Annotationfile')
        annotation.text = annotationFile

        export = et.ElementTree(document)
        shared.indentXML(document)
        export.write(self.exportLocation + filename, encoding='utf-8', 
                xml_declaration=True)


class CSVExporter(Exporter):

    def export(self, segments, exportLocation, withHeader=False, withIndices=True):
        """
        Exports the given segments to a specific file in CSV notation

        :param segments: A list (array) of segments which should be exported to
                the same file
        :type segments: list of 
                :class:`Sensorsegment <sedater.lib.shared.Sensorsegment>`
        :param str exportLocation: export path location (incl. filename)
        :param Boolean withHeader: Print a header line in the csv file, 
                indicating the row attributes
        :param Boolean withIndices: Print an Indexnumber in the first column
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
                        header = ['Index']
                        header.extend(shared.Sensorsegment._fields)
                        exp.writerow(header)
                    else:
                        # header without indices
                        header = shared.Sensorsegment._fields
                        exp.writerow(header)
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
