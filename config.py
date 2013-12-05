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

#Define mass of the isotopic labels
C12=12.00000 # Carbon 12 
C13=13.003355 # Carbon 13
C13Shift = C13-C12 # Difference in Carbon Mass

N14=14.003074 # Nitrogen 14
N15=15.000109 # Nitrogen 15
N15Shift=N15-N14 # Difference in Nitrongen Mass

label_default=6*C13Shift + 2*N15Shift # Default Label 13C6 15N2 = +8Da

H=1.007825 # Hydrogen Mass
Elec=0.00054858 # Electron Mass
proton=H-Elec # Proton Mass

#Default parameters        
DEFAULTTOL = 0.01 # Mass accuracy
DEFAULTTHRESHOLD = 100000  # Signal rejection Threshold
SCANWINDOW = 0.5 # Sliding time window
STARTSCAN = 0 # Start Scan
ENDSCAN = 1000000 # End Scan
STARTMASS = 350 # Minimum mass
ENDMASS = 2000  # Maximum mass
MAXISO = 4      # Maximum number of isotopes
MAXCHARGE = 4   # Maximum number of charges
NORMCHARGE = [3] # Normalization charge
