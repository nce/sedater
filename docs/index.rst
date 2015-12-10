=============================
A Sensor-Validation Converter
=============================
:Author: Ulli Goschler
:Contact: ulligoschler@gmail.com
:version: 1.0.0
:copyright: https://github.com/nce/sedater/blob/master/LICENSE

A Python Tool to convert Sensor-Validation Data to a more machine-
processable format.

It includes two utilities:
    - The parser, processor and exporter of Sensor-Validation files, see: :ref:`sedater`
    - A plotter for SVG-graphics, see: :ref:`plotter`

The sources are available on: `Github/sedater <https://github.com/nce/sedater>`_

-----------------
Table of Contents
-----------------

.. contents:: Content
    :depth: 3
.. section-numbering::

=============
Documentation
=============

.. _sedater:

------------------
sedater - The Tool
------------------
sedater imports files or directories which were exported by a Vicon or
Shimmer (Foot) Sensor.

These files are hardly processable which this tool tries to solve.

Sensors usually export two kinds of files:
    - RawValidation Data
    - TextValidation Data


**RawValidation Data**:
RawValidation files are binary files storing a sensors' recorded movement.

**TextValidation Data:**
Provide a textual representation of Metadata as well as Validationdata
in some kind of CSV notation.

Command Line Options
--------------------

.. automodule:: sedater.options
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:

Data Import
-----------
The ``filesystem``-module is responsible for the finding and indexing
of all files found under or in a directory.

After all files are indexed and paired together, the data conversion is
handled by two different submodules:

    - Rawdata (``.dat``) (binary) is handled by the :ref:`rawDataConversion`
    - Textdata (``.txt``) is handled by the :ref:`textDataConversion`


.. automodule:: sedater.filesystem
    :members:
    :private-members:
    :undoc-members:
    :show-inheritance:

.. _rawDataConversion:

Raw Data Conversion and Normalization
-------------------------------------
The indexed Sourcefiles are now processed. The binary RawValidation files
(``.dat``) are segmented in atomic movement recordings called Sensorsegment.
These values need to be normalized with an unique ``Calibrationfile``
specific for each Sensor (provided by command line).

After the normalization of each Sensorsegment, they are ready for
export, back to the filesytem. See :ref:`dataExport` for further details.

.. automodule:: sedater.rawvalidation
    :members:
    :private-members:
    :undoc-members:
    :show-inheritance:

.. _textDataConversion:

Text Data Conversion
--------------------
The indexed Sourcefiles are now processed. All matching ``.txt`` files
are analyzed for valid TextValidation content. Files,  like the one
mentioned in
:class:`TxtConverter.parseTxtFile <txtvalidation.TxtConverter.parseTxtFile>`,
are imported and all data is converted in
:class:`Validationfile <lib.shared.Validationfile>` specific objects.

These objects are ready for export, back to the filesystem. See
:ref:`dataExport` for further details

.. automodule:: sedater.txtvalidation
    :members:
    :private-members:
    :undoc-members:
    :show-inheritance:

.. _dataExport:

Data Export
---------------------

Both - the Raw and the Text - data can be exported to the filesystem. 
Due to
the nature of the RawValidation files they are always exported 
as CSV files to the 
respective ``session`` directory. The Textfiles (technically) allow 
multiple export schemes like ``json`` or ``xml``. Currently only ``xml``
is implemented and understood by the :ref:`plotter`

.. automodule:: sedater.export
    :members:
    :private-members:
    :undoc-members:
    :show-inheritance:

Library Files
-------------------------
The library files are used throughout the whole application.

.. automodule:: sedater.lib.shared
    :members:
    :undoc-members:
    :show-inheritance:


------------


.. _plotter:

--------------------------
plotter - Graphing utility
--------------------------
Plotting is the second part of this tool. It offers the ability to
create SVG image files of the normalized RawValidation data.

With information about the Gold Standard parameters in the 
``annotation.xml`` file, it is possible to draw these parameters as an
overlay over the regular plot.

Refer to the Enduser documentation on:
`Github/sedater <https://github.com/nce/sedater>`_ for sample images.


Command Line Options
--------------------

.. automodule:: sedater.plotter.options
    :members:
    :undoc-members:
    :show-inheritance:

Plotting
--------------------

.. automodule:: sedater.plotter.plotter
    :members:
    :private-members:
    :undoc-members:
    :show-inheritance:

