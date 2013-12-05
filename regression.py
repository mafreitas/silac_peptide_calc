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
import math

# Define linear regression	
def linreg(X, Y):
    """
    Summary
        Linear regression of y = ax + b
    Usage
        real, real, real = linreg(list, list)
    Returns coefficients to the regression line "y=ax+b" from x[] and y[], and R^2 Value
    """
    
    if len(X) != len(Y):  raise ValueError, 'unequal length'
   
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
   
    for x, y in map(None, X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
       
    det = Sxx * N - Sx * Sx
    
    a, b = (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
   
    meanerror = residual = 0.0
    
    for x, y in map(None, X, Y):
        meanerror = meanerror + (y - Sy/N)**2
        residual = residual + (y - a * x - b)**2
        
    RR = 1 - residual/meanerror
    ss = residual / (N-2)
    StdDev_a, StdDev_b = math.sqrt(ss * N / det), math.sqrt(ss * Sxx / det)

    return a, b, RR, ss, StdDev_a, StdDev_b, N


# Define robust linear regression	
def ktrreg(X, Y):
    """
    Summary
        Kendall Thiel, Robust Linear regression of y = ax + b
    Usage
        real, real, list = ktrreg(list, list)     
    Returns coefficients to the regression line "y=ax+b" from x[] and y[], and median ratios
    """
   
    if len(X) > 0 and len(Y) > 0 and len(X) == len(Y):

        # Create lists
        cratios = []
        iratios = []
        results = []

        # Calculate the slope using the complete version of the Kendall Theil
        if len(X) < 10000:
           for i in range(0, len(X)):
                for j in range(i+1, len(X)):
                    if X[j] == X[i] or Y[j] == Y[i]:
                        continue
                    else: 
                        cratios.append(math.fabs(float(Y[j]-Y[i])/float(X[j]-X[i])))

        # Calculate the slope using the incomplete version of the Kendall Theil, Thiel's Method
        halflen = len(X)/2
        for i in range(0,halflen):
            if X[halflen+i] == X[i] or Y[halflen+i] == Y[i]:
                continue
            else:
                iratios.append(math.fabs(float(Y[halflen+i]-Y[i])/float(X[halflen+i]-X[i])))
       
        # Sort lists
        cratios.sort()
        iratios.sort()
        
        X.sort()
        Y.sort()
       
        # Calculate slope by the Thiel's method and its corresponding intercept
        ti_slope = iratios[len(iratios)/2]
        
        Xmed = X[len(X)/2]
        Ymed = Y[len(Y)/2]

        ti_intercept = Ymed - ti_slope * Xmed

        # Calculate standard deviation of the slope and intercept
        N = len(X)
        Sx = Sy = Sxx = Syy = Sxy = 0.0
        for x, y in map(None, X, Y):
            Sx = Sx + x
            Sy = Sy + y
            Sxx = Sxx + x*x
            Syy = Syy + y*y
            Sxy = Sxy + x*y
        det = Sxx * N - Sx * Sx
        a, b = ti_slope, ti_intercept
        meanerror = residual = 0.0
        for x, y in map(None, X, Y):
            meanerror = meanerror + (y - Sy/N)**2
            residual = residual + (y - a * x - b)**2

        RR = 1 - residual/meanerror
        ss = residual / (N-2)
        StdDev_a, StdDev_b = math.sqrt(ss * N / det), math.sqrt(ss * Sxx / det)

        # Append results to lists
        results.append(ti_slope)
        results.append(ti_intercept)
        results.append(iratios)
        results.append(StdDev_a)
        results.append(StdDev_b)
        return results
    
    else:
        return -1


