# ./sedater/lib/filesystem.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Thu, 10.12.2015 - 23:16:02

import os, sys
import re
from collections import namedtuple

from sedater.lib.shared import Sourcefile
from sedater.lib.shared import Orientation

class Crawler(object):
    """
    The Crawler operates on a filesystem level. It locates all processable
    files  and groups them in individual sessions together.

    In the crawling process all files under the given path (usually
    provided on command line) are examined and disassembled by certain 
    criteria based on the filename.

    Session Data (required) is usually prefixed by (case sensitive):
        * GAstd
        * GA
        * P
        * Pat

    Exercise Data (optional) by:
        - E

    Orientation data (required) by (case insensitive):
        - left
        - right

    In the following pairing process, individual sensor data files are paired 
    together based on the session (and if available: exercise) ID.
    So each session should contain a left and right sensor file.
    """

    def __init__(self):
        self.existingFiles = []
        self.pairedFiles   = []

    def crawl(self, source):
        """
        Crawls all directories under the supplied path and stores files 
        matching a certain filename criteria for further processing

        :param str source: Path which should be crawled
        :return: Indicator if the crawling of the source was successfull
        :rtype: bool
        """
        sourceIsDir  = True if os.path.isdir(source) else False
        sourceIsFile = True if os.path.isfile(source) else False
        if not sourceIsFile and not sourceIsDir:
            raise AttributeError("'{}' is neither a file nor a directory,"
                    " attempting to skip this input source".format(source))
            return False

        if sourceIsFile:
            try:
                validFile = self._parseFileName(source)
            except PermissionError:
                # TODO: log it
                pass
            if validFile:
                self.existingFiles.append(validFile)
        else:
            # scan for files lying under current node and restart parsing
            for paths, dirnames, files in os.walk(source):
                for name in files:
                    self.crawl(os.path.join(paths,name))

        if not self.existingFiles:
            raise ValueError("No processable files found in '{}'".format(source))
            return False

    def _parseFileName(self, f):
        """
        Apply a RegEx on a filename to extract the sensor's orientation and
        session ID (aka patient ID); if an exercise ID is available,
        match that too.

        See the source code for available orientation parameters.

        :param str f: Path of the file
        :raises PermissionError: Indicating that no read access is provided
        :return: Parsed sourcfile information
        :rtype: :class:`Sourcefile <lib.shared.Sourcefile>`
        """
        if not os.access(f, os.R_OK):
            try:
                raise PermissionError("No read access granted on '{}', "
                    " skipping file")
            except Exception:
                return False

        attr = [''] * 5                     # create list for file attributes
        attr[0], attr[1] = os.path.split(f) # 0: fullpath 1:filename

        # list of regexes we run the filename against
        ## orientation is either left or right 
        ## exercise is prefixed by 'E' and sometimes followed by the orientation
        ## session is either prefixed by 'P', 'GA', 'GAstd' or 'Pat'
        orientation = re.compile("(left|right)", re.IGNORECASE|re.M)
        exercise    = re.compile("E([A-Za-z0-9]+)(?:left|right)?", re.M)
        session     = re.compile("P([0-9]+)E?|GA([0-9]+)|GAstd([0-9a-z]+)(?:left|right)|Pat([0-9a-z]+)(?:left|right)", re.IGNORECASE|re.M)

        orientationMatch = orientation.search(attr[1])
        exerciseMatch    = exercise.search(attr[1])
        sessionMatch     = session.search(attr[1])

        # extract the matches
        if orientationMatch:
            m = orientationMatch.group(1).lower()
            if m == 'left':
                attr[4] = Orientation.left
            elif m == 'right':
                attr[4] = Orientation.right
        if exerciseMatch:
            attr[3] = exerciseMatch.group(1)
        if sessionMatch:
            for i in range(1, len(sessionMatch.groups()) + 1):
                if sessionMatch.group(i):
                    attr[2] = sessionMatch.group(i)
                    break
        return Sourcefile._make(attr)

    def pair(self):
        """
        Pair files together based on the filename.

        *This should only happen after the ``crawl()`` function found 
        and indexed files*

        Each Session (Patient) has usually more sensors (e.g. left &
        right foot).

        :raises ValueError: Pairing of mentioned files failed
        :return: Indicator of successful paring
        :rtype: bool
        """
        if not self.existingFiles:
            raise ValueError("Can't attempt pairing if no datasets are "
                    "available. Either the Inputsource didn't provide "
                    "any matching files or the detection process failed")

        # delete all datasets without session and orientation data
        # TODO: log deleted files
        self.existingFiles = [x for x in self.existingFiles 
                if x.session and x.orientation]

        for single in self.existingFiles[:]:
            # always find a matching 'right' sensor
            if not single.orientation.name == 'left': continue
            # match same session, exercise and file extension
            match = [x for x in self.existingFiles 
                    if single.session == x.session
                    and single.exercise == x.exercise
                    and os.path.splitext(single.filename)[1]
                        == os.path.splitext(x.filename)[1]]
            if len(match) == 2:
                self.existingFiles.remove(match[0])
                self.existingFiles.remove(match[1])
                self.pairedFiles.append((match[0], match[1]))

        # TODO: better way to handle files without partner?
        if self.existingFiles:
            for i in self.existingFiles:
                self.pairedFiles.append((i, i))
                print("Found file without a matching partner "
                        "'{}/{}', pairing with itself to continue."
                        .format(i.path, i.filename), file=sys.stderr)

        return True

