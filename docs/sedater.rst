sedater package
===============

Components
----------

Data Import
-----------

.. automodule:: sedater.filesystem
    :members:
    :undoc-members:
    :show-inheritance:

sedater.main module
-------------------

.. automodule:: sedater.main
    :members:
    :undoc-members:
    :show-inheritance:

Command Line Options
--------------------

.. automodule:: sedater.options
    :members:
    :undoc-members:
    :show-inheritance:

Raw Data Conversion and Normalization
-------------------------------------

.. automodule:: sedater.rawvalidation
    :members:
    :private-members:
    :undoc-members:
    :show-inheritance:

Text Data Conversion
--------------------

.. automodule:: sedater.txtvalidation
    :members:
    :undoc-members:
    :show-inheritance:

Data Export
---------------------

Both - the Raw and the Text - data is exported to the filesystem. Due to
the nature of the Rawfiles they are always exported as CSV files to the 
respective ``session`` directory. The Textfiles allow multiple export 
schemes like ``json`` or ``xml``, which are currently implemented.

.. automodule:: sedater.export
    :members:
    :undoc-members:
    :show-inheritance:

Library Files
-------------------------

.. automodule:: sedater.lib.shared
    :members:
    :undoc-members:
    :show-inheritance:

Module contents
---------------

.. automodule:: sedater
    :members:
    :undoc-members:
    :show-inheritance:
