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
import matplotlib.pyplot
import matplotlib

def saveplot_ratios(X, Y, filename):
    """
    Create plots for light and heavy abundances of all peptides
    """    
    # creates pyplot figure object
    matplotlib.pyplot.figure()
    
    #plot data
    matplotlib.pyplot.scatter(X, Y, s=4,color="black",lw = 0, label="L vs H abund")

    #add in labels and title
    matplotlib.pyplot.xlabel("Light Abundance")
    matplotlib.pyplot.ylabel("Heavy Abundance")
    matplotlib.pyplot.suptitle(filename)

    #save figure to png
    matplotlib.pyplot.savefig(str(filename) + ".pdf")
    matplotlib.pyplot.clf()


def saveplot_ratios_w_regs(X, Y, filename, slope1, intercept1, slope2, intercept2, mnr = -1, mnrwa = -1, size = 4 ):
    """
    Summary  
        Create scatter plots for the light and heavy abundance of peptide peaks with regression lines
    Usage
        saveplot_ratios_w_regs(X, Y, filename, slope1, intercept1, slope2, intercept2, mnr = -1, mnrwa = -1, size = 4 ):
    Returns a scatter plot for light:heavy abundance of all peptides with normalization factors or light:heavy abundance of
    a single peptide with peptide ratio
    """
  
    # creates pyplot figure object    
    matplotlib.pyplot.figure()
    
    #plot data
    matplotlib.pyplot.scatter(X, Y, s=size,color="black",lw = 0, label="L vs H abund")

    #set axes limits and save figure to png
    txmin,txmax = matplotlib.pyplot.xlim()
    tymin,tymax = matplotlib.pyplot.ylim()

    if txmax > tymax:
        tymax = txmax
    else:
        txmax = tymax

    matplotlib.pyplot.xlim(0.0,txmax)
    matplotlib.pyplot.ylim(0.0,tymax)

    Xreg = [0.0,txmax]

    #Set the location of the regression lines
    miny1=float(intercept1)
    maxy1=float(txmax) * float(slope1) + float(intercept1)
    Yreg1 = [miny1,maxy1]

    miny2=float(intercept2)
    maxy2=float(txmax) * float(slope2) + float(intercept2)
    Yreg2 = [miny2,maxy2]
    
    #Draw the robust linear regression and linear regression lines
    matplotlib.pyplot.plot(Xreg, Yreg1,label="RLR regression="+ str("%.2f" % slope1), color="black", ls="solid")
    matplotlib.pyplot.plot(Xreg, Yreg2,label="LR regression="+ str("%.2f" % slope2), color="black", ls="dashed")

    # Draw the regression lines by the median and abundance weighted median ratio if applicable
    if mnr != -1:
        miny3 = 0.0
        maxy3= float(txmax) * float(mnr)
        Yreg3 = [miny3,maxy3]     
        matplotlib.pyplot.plot(Xreg, Yreg3,label="Median ratio="+ str("%.2f" % mnr), color="black", ls="dashdot")
    if mnrwa != -1:
        miny4 = 0.0
        maxy4= float(txmax) * float(mnrwa)
        Yreg4 = [miny4,maxy4]     
        matplotlib.pyplot.plot(Xreg, Yreg4,label="Weighted Median ratio="+ str("%.2f" % mnrwa), color="black", ls="dotted")
      
    #add in legend, labels and title
    matplotlib.pyplot.xlabel("Light Abundance")
    matplotlib.pyplot.ylabel("Heavy Abundance")
    matplotlib.pyplot.suptitle(filename)
    matplotlib.pyplot.legend()
 
    #Draw the line y=x as a reference for a unity ratio
    matplotlib.pyplot.plot((0,txmax), (0,tymax), color="red", ls="dotted")

    #Save plot in pdf    
    matplotlib.pyplot.savefig(str(filename) + ".pdf")
    matplotlib.pyplot.clf()


def saveplot_norm_ratios(X, Y, Z, filename):
    """
    Summary
        Create a heatmap of the SILAC ratios 
    """  
    # creates pyplot figure object
    matplotlib.pyplot.figure()

    for i in range(0,len(Z)):
        Z[i] = math.log(Z[i],2)   
    #plot data
    matplotlib.pyplot.scatter(X, Y, c=Z, s=4, lw = 0, label="log2 ratio", cmap=matplotlib.cm.RdYlGn_r)
    cb = matplotlib.pyplot.colorbar()
    cb.set_label('log2 ratio')
    matplotlib.pyplot.legend()
        
    #add in labels and title
    matplotlib.pyplot.xlabel("Retention Time")
    matplotlib.pyplot.ylabel("Light Mass")
    matplotlib.pyplot.suptitle(filename)
    # save plot in pdf
    matplotlib.pyplot.savefig(str(filename) + ".pdf")
    matplotlib.pyplot.clf()

