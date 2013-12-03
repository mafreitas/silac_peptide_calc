# -------------------------------------------------------------------------
#     The following file is a modified version of parser_mzxml.py 
#     distrubuted with the MMass application <www.mmass.org>.
#
#     Modifications Copyright (C) 2012-2013 Michael A. Freitas 
#     Original code Copyright (C) 2005-2013 Martin Strohalm 
#
#     This file is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.
#
#     Complete text of GNU GPL can be found in the file LICENSE.TXT in the
#     main directory of the program.
# -------------------------------------------------------------------------

import os.path
from lxml import etree as ET
import base64
import struct

from itertools import chain, izip

class mzXMLDoc:

    def __init__(self, ):

        self.data = {
                    'docType':'mzXML',
                    'scanID':'',
                    'peaklist':[],
                    'spectrum':[]
                    }
                    
        self.scan_basePeakMz = []
        self.scan_basePeakIntensity = []
        self.scan_scanID =[]
        self.scan_num = []
        self.scan_retentionTime  = []
        
        # This parser does not automatically remove namespace.  Namespace
        # must be set in the code as shown below.
        
        self.ns = "{http://sashimi.sourceforge.net/schema_revision/mzXML_3.0}"
#       self.namespace = "http://sashimi.sourceforge.net/schema_revision/mzXML_2.1"
        self.namespace = "http://sashimi.sourceforge.net/schema_revision/mzXML_3.0"
        
    def getDocument(self, path):
 
        # parse XML
        self.doc = ET.parse(path)       
        self.root = self.doc.getroot()
        
        # get spectrum
        self.scans = self.root.findall(".//" + self.ns + "scan")


    def getSpectrum(self, scan):
        """ Read and parse selected elements' data from document. """

        status = self.handleSpectrum(scan)         
        return self.data


    def getPeaks(self, spectrum):
        """ Get spectrum data from <spectrum> element. """

        # get data element
        self.peaks = spectrum.find('./'+self.ns+'peaks')
        
        # get endian or use default(!)
        
        try:
            
            if self.peaks.get('byteOrder') == 'network':
                endian = '!'
            elif self.peaks.get('byteOrder') == 'little':
                endian = '<'
            elif self.peaks.get('byteOrder') == 'big':
                endian = '>'
            else:
                endian = '!'
       
            # get text
            data = self.peaks.text

            # decode data
            try:
                data = base64.b64decode(data)
            except:
                return False

        # convert from binary format
            try:
                pointsCount = len(data)/struct.calcsize(endian+'f')
                start, end = 0, len(data)
                data = struct.unpack(endian+'f'*pointsCount, data[start:end])
            except:
                return False
            
            # split data to m/z and intensity
            mzData = data[::2]
            intData = data[1::2]
            
            # check data
            if not mzData or not intData or (len(mzData) != len(intData)):
                return False
    
            # "zip" mzData and intData
            formatedData = zip(mzData, intData)
            self.data['peaklist'] = self.convertSpectrumToPeaklist(formatedData)
            return self.data['peaklist']
    
        except:
            print "Could not read Peaks!"
            return False
    

    def getScans(self, spectra):
        """ Get basic info about all the ms scans. """

        # get list of scans
        scans = []
        for x, scan in enumerate(spectra):

            # get scan info
            scanInfo = self.getScanInfo(scan)

            # ID, time, range, MS level, prec.mass, pre.charge, spec. type
            scans.append(['---', '---', '---', '---', '---', '---', '---', '---'])
            scans[x][0] = scanInfo['id']
            scans[x][1] = scanInfo['time']
            scans[x][2] = scanInfo['range']
            scans[x][3] = scanInfo['points']
            scans[x][4] = scanInfo['level']
            scans[x][5] = scanInfo['mz']
            scans[x][6] = scanInfo['charge']
            scans[x][7] = scanInfo['type']

        return scans


    def getScanInfo(self, scan):
        """ Get basic info about selected scan. """

        scanInfo = {}
        scanInfo['type'] = '---'
        scanInfo['level'] = '---'
        scanInfo['range'] = '---'
        scanInfo['points'] = '---'
        scanInfo['polarity'] = '---'
        scanInfo['time'] = '---'
        scanInfo['mz'] = '---'
        scanInfo['charge'] = '---'
        scanInfo['method'] = '---'

        # get ID
        scanInfo['id'] = scan.get('num')

        # get msLevel
        scanInfo['level'] = scan.get('msLevel')

        # get number of points
        scanInfo['points'] = scan.get('peaksCount')

        # get polarity
        scanInfo['polarity'] = scan.get('polarity')

        # get retention time
        scanInfo['time'] = scan.get('retentionTime')

        # get range
        lowMz = scan.get('lowMz')
        highMz = scan.get('highMz')
        try:
            scanInfo['range'] = '%d - %d' % (float(lowMz), float(highMz))
        except:
            scanInfo['range'] = '%s - %s' % (lowMz, highMz)

        # find precursor params
        if scanInfo['level'] and scanInfo['level'] != '1':
            precursorMz = scan.findall('precursorMz')
            if precursorMz:

                # get m/z
                scanInfo['mz'] = self.getText(precursorMz[0].childNodes)

                # get charge
                scanInfo['charge'] = precursorMz[0].get('retentionTime')

        return scanInfo


    def getText(self, nodelist):
        """ Get text from node list. """

        # get text
        buff = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                buff += node.data

        return buff


    def convertSpectrumToPeaklist(self, spectrum):
        """ Convert spectrum to peaklist. """

        peaklist = []
        for point in spectrum:
            peaklist.append([point[0], point[1]])

        return peaklist


    def basePeakPlot(self):
        return list(chain(*izip(self.scan_num, self.scan_basePeakIntensity)))


if __name__ == "__main__":
    test = mzXMLDoc()
    
    print test.getDocument(path='./test.mzxml')
