# ./sedater/export.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 08.11.2015 - 22:21:45 
# Modified: Tue, 08.12.2015 - 22:41:41

import csv
import os
from xml.etree import ElementTree as et

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

# # TODO: move to validation; this should not be the in an exporter
#     def getOrientation(self, validationProperties):
#         orientationIndex = validationProperties.index('Orientation')
#         # get the next element in list
#         orientation = validationProperties[orientationIndex + 1]
#         # check if orientation is a sring, and is a valid 'Orientation'
#         if isinstance(orientation, str) and \
#                 orientation in [e.name for e in shared.Orientation]:
#             return orientation
#         else:
#             # TODO: get current file
#             raise AttributeError("The ValidationTxtFile '{}' does not contain"
#                     " a valid Orientation. This is not recoverable, as we"
#                     " don't know where to store the export".format("Unknown"))

#     def getValidationType(self, validationProperties):
#         validationIndex = validationProperties.index('Validation')
#         # get element 'right of' Validation
#         validation = validationProperties[validationIndex + 1]
#         if isinstance(validation, str):
#             return validation
#         else:
#             raise AttributeError("The ValidationTxtFile '{}' does not contain"
#                     " a valid ValidationType. This is recoverable, but might"
#                     " mishandle the export".format("Unknown"))

class XMLExporter(Exporter):
    def __init__(self, exportLocation):
        """
        Exports the given validation to a specific file in XML notation

        :param str exportLocation: Path to the export directory
        """

        self.exportLocation = exportLocation
        self.annotationFile = 'annotation.xml'
    def export(self, validation):
        """
        :param validation: The parsed 
            :class:`Textfile <sedater.txtvalidation.TxtConverter.parseTxtFile>`
        :param type validation: 
            :class:`Validationfile <sedater.lib.shared.Validationfile>`
        """

        filename = 'annotation.xml'
        # extract parameters from txtvalidation

        self._exportMetaInformationToXML(validation.sourcefile.session, 
                validation.sourcefile.exercise, filename)

        # check if file already exists (from a previous run or the other sensors)
        if os.path.isfile(self.exportLocation + filename):
            document = et.ElementTree()
            document.parse(self.exportLocation + filename)

            overwrite = document.find('.//Sensor [@Orientation="'+
                    validation.sourcefile.orientation.name +'"]/..\
                    [@Type="'+validation.type+'"]')
            if overwrite:
                document.getroot().remove(overwrite)
        else:
            head = et.Element('Data')
            document = et.ElementTree(head)

        document = document.getroot()
        if validation.type:
            validationXML = et.SubElement(document, 'Validation')
            validationXML.set('Type', validation.type)
        else:
            validationXML = document

        orientationXML = et.SubElement(validationXML, 'Sensor')
        orientationXML.set('Orientation', validation.sourcefile.orientation.name)

        meta = et.SubElement(orientationXML, 'Meta')
        #print(validation.properties, file=sys.stderr)
        for prop in validation.properties:
            tmp = et.SubElement(meta, prop[0])
            tmp.text = prop[1]

        content = et.SubElement(orientationXML, 'Content')
        steps = 1
        for prop in validation.content:
            counter = et.SubElement(content, 'No' + str(steps))
            for key, value in prop.items():
                tmp = et.SubElement(counter, key)
                tmp.text = value
            steps = steps + 1

        export = et.ElementTree(document)
        shared.indentXML(document)
        export.write(self.exportLocation + filename, encoding='utf-8',
                xml_declaration=True)
        return True



    def _exportMetaInformationToXML(self, session, exercise, annotationFile):
        """
        Creates a XML file containing the session details. Specifying the 
        ``Session``, ``Exercise`` and the fll path to the ``Annotationfile`` 
        containing all Validationdata.

        :param str session: Name of the current session
        :param str exercise: Name of the current exercise
        :param str annotationFile: Full path to the annotation file
        """
        filename = 'metainformation.xml'

        # Build XML structure
        documentXML = et.Element('Meta')

        sessionXML = et.SubElement(documentXML, 'Session')
        sessionXML.text = session

        exerciseXML = et.SubElement(documentXML, 'Exercise')
        exerciseXML.text = exercise

        annotationXML = et.SubElement(documentXML, 'Annotationfile')
        annotationXML.text = annotationFile

        exportXML = et.ElementTree(documentXML)
        shared.indentXML(documentXML)
        exportXML.write(self.exportLocation + filename, encoding='utf-8', 
                xml_declaration=True)
        return True


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
