# ./sedater/export.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 08.11.2015 - 22:21:45 
# Modified: Fri, 11.12.2015 - 01:14:26

import csv
import os
from xml.etree import ElementTree as et

from sedater.lib import shared

class Exporter(object):
    """
    Exports the compiled data.

    The data collected by either binary or text files (and ready for 
    exportation), will be written to the filesystem.
    """

    def __init__(self):
        pass

    def prepareOutputDir(self, dirPrefix, session, exercise=False):
        """
        Creates all necessary directories for the exporting process.

        Each individual ``session`` gets an own directory under the ``ouputDir``
        provided by command line.

        :param str dirPrefix: Path under which all directories will be created
        :param str session: Session identifier
        :param str exercise: (optional) Exercise identifier
        :return: Path to existing directory
        :rtype: str
        """
        ePrefix = "_E"+exercise if exercise else ''
        sPrefix = "session"+session

        output = dirPrefix + '/' + sPrefix + ePrefix + '/'

        if not os.path.exists(output):
            os.makedirs(output)

        return output

class XMLExporter(Exporter):
    """
    Exports TextValidation files to a single file in XML notation

    :param str exportLocation: Path to the export directory
    """

    def __init__(self, exportLocation):
        self.exportLocation = exportLocation
        self.annotationFile = 'annotation.xml'

    def export(self, validation):
        """
        :param validation: The parsed 
            :class:`Textfile <txtvalidation.TxtConverter.parseTxtFile>`
        :type validation:
            :class:`Validationfile <lib.shared.Validationfile>`
        """

        filename = 'annotation.xml'

        self._exportMetaInformationToXML(validation.sourcefile.session, 
                validation.sourcefile.exercise, filename)
        output = self._getExportLocation(validation.sourcefile.session,
                validation.sourcefile.exercise)

        # check if file already exists (from a previous run or the other sensors)
        if os.path.isfile(output + filename):
            document = et.ElementTree()
            document.parse(output + filename)

            overwrite = document.find('.//Sensor[@Orientation="'+
                    validation.sourcefile.orientation.name.lower() +'"]/..[@Type="'+validation.type+'"]')
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
        export.write(output + filename, encoding='utf-8',
                xml_declaration=True)
        return True


    def _getExportLocation(self, session, exercise):
        """
        Returns a dynamic export location.

        :param str session: Session
        :param str exercise: Exercise
        :return: Current export location
        :rtype: str
        """
        ePrefix = "_E"+exercise if exercise else ''
        sPrefix = "session"+session

        output = self.exportLocation + '/' + sPrefix + ePrefix + '/'

        return output

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
        output = self._getExportLocation(session, exercise)

        # Build XML structure
        documentXML = et.Element('Meta')

        sessionXML = et.SubElement(documentXML, 'Session')
        sessionXML.text = session

        exerciseXML = et.SubElement(documentXML, 'Exercise')
        exerciseXML.text = exercise

        annotationXML = et.SubElement(documentXML, 'Annotationfile')
        annotationXML.text = output + annotationFile

        exportXML = et.ElementTree(documentXML)
        shared.indentXML(documentXML)
        exportXML.write(output + filename, encoding='utf-8', 
                xml_declaration=True)
        return True


class CSVExporter(Exporter):
    """
    This Exporter handles the export of the RawValidation files to CSV files.

    After the :class:`Sensorsegments <lib.shared.Sensorsegment>` are
    normalized they can be exported back to the filesystem as CSV files.
    """

    def export(self, segments, exportLocation
            , withHeader=False
            , withIndices=True):
        """
        Exports the given segments to a specific file in CSV notation

        :param segments: A list (array) of segments which should be exported to
                the same file
        :type segments: list of 
                :class:`Sensorsegment <lib.shared.Sensorsegment>`
        :param str exportLocation: export path location (incl. filename)
        :param Boolean withHeader: Print a header line in the csv file, 
                indicating the row attributes
        :param Boolean withIndices: Print an Indexnumber in the first column
        :return: Indication whether the export succeeded
        :rtype: Boolean
        """

        try:
            with open(exportLocation, 'w') as exportFile:
                # TODO: indices are currently always placed in the first 
                # column,
                # as they are needed for the plotting. But this might not
                # be wanted by the user. So maybe deactivate them by
                # commandline switch
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
                    exp.writerows([(
                        index+1
                        , value.accelX
                        , value.accelY
                        , value.accelZ
                        , value.gyroX
                        , value.gyroY
                        , value.gyroZ
                        ) for index,value in enumerate(segments)])
                else:
                    # column without indices
                    exp.writerows([(
                        value.accelX
                        , value.accelY
                        , value.accelZ
                        , value.gyroX
                        , value.gyroY
                        , value.gyroZ
                        ) for value in segments])

        except Exception as e:
            # TODO: handle common exceptions;
            # but not sure what could happen here besides filesystem 
            # failures
            raise e

        return True
