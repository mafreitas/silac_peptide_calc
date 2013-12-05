# -------------------------------------------------------------------------
#     SILAC Peptide Ratio Calculator  
#     Copyright (C) 2012-2013 iaoyan Guan and Michael A. Freitas
#
#     This program is free software; you can redistribute it and/or modify
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

# Python imports
import sys
import re

# Define median         
def listmed(X, Y):
    """
    Summary
        Returns median ratio
    """
    if len(X) > 0 and len(Y) > 0 and len(X) == len(Y):
        ratio = []
        for i in range(0, len(X)):
            ratio.append ( float(Y[i]/X[i]))
        ratio.sort()
        medratio =ratio[len(ratio)/2]
        return medratio
       
    else:
        return -1

def getRetTime(rettime):
    pattern = re.compile(r'PT(\d*.\d*)S')
    time = pattern.search(rettime).groups()
    return float(time[0])

def updateStdOut(string):
    sys.stdout.write("%s\r" % (string,))
    sys.stdout.flush()
