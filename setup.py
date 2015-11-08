#!/usr/bin/env python3

from distutils.core import setup
import os

setup(
        name='Sedater',
        version='0.0.1',
        description='Python Tool to convert SensorValidation Data to '
        'a more machine-processable format',
        author='Ulli Goschler',
        author_email='ulligoschler@gmail.com',
        license = "MIT",
        url='https://github.com/nce/sedater',
        packages=['sedater', 'sedater.lib', 'sedater.test'],
        #long_description=read('README.md'), TODO:working
     )
