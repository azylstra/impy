# Calculate yields, Ti
# A. Zylstra 2013/04/13

from Implosion import *
from Resources.IO import *
from Resources import Fusion
from numpy import arange
from numpy import zeros
import math
import csv
import os

# cutoffs in Ti for calculations
Ti_Min = 0.5
Ti_Max = 50

# reactions
reactions = []
# syntax: [ name , A1, Z1, A2, Z2, reactivity fn ]
reactions.append( [ "DD" , 2, 1, 2, 1, Fusion.DD ] )
#reactions.append( [ "DT" , 2, 1, 3, 1, Fusion.DT ] )
#reactions.append( [ "TT" , 3, 1, 3, 1, Fusion.TT ] )
reactions.append( [ "D3He" , 2, 1, 3, 2, Fusion.D3He ] )
#reactions.append( [ "3He3He" , 3, 2, 3, 2, Fusion.HeHe ] )
#reactions.append( [ "HD", 1, 1, 2, 1, Fusion.HD ] )
#reactions.append( [ "p11B", 11, 5, 1, 1, Fusion.p11B ] )
#reactions.append( [ "p15N", 1, 1, 15, 7, Fusion.p15N ] )

# global implosion
impl = 0
    
# ------------------------------------
# Burn rate calculators
# ------------------------------------
def rate(rxn, it):
    """Calculate the rate for a specified reaction rxn at time index t."""
    # fuel info
    A1 = rxn[1]
    Z1 = rxn[2]
    A2 = rxn[3]
    Z2 = rxn[4]
    dblcount = 1
    if (A1 == A2) and (Z1 == Z2):
        dblcount = 2 #account for factor of 2 if reactants are identical
    #fuel fractions
    f1 = 0
    f2 = 0
    # return values
    ret = 0
    ret2 = 0 #Ti 'rate'
    
    # iterate over all radii:
    for ir in range( impl.ir_min() , impl.ir_fuel() ):
        vol = impl.vol(ir,it)
        Ti = impl.Ti(ir,it)
        # crop Ti:
        Ti = min(Ti,Ti_Max)

        # get fuel fractions:
        f1 = impl.f(ir,it,A1,Z1)
        f2 = impl.f(ir,it,A2,Z2)

        # burn rate for this zone:
        temp = rxn[5](Ti)*pow(impl.ni(ir,it),2)*(f1*f2/dblcount)*vol

        # append to return:
        ret += temp
        ret2 += temp*Ti

    return [ret , ret2]
 
# ------------------------------------
# Main method
# ------------------------------------
def run(i):
    """Calculate total yield."""
    # input sanity check:
    if not isinstance(i,Implosion):
        print("WARNING: invalid input.")
        return
    global impl
    impl = i # global implosion variable for this module
        
    # Yields
    Y = zeros( len(reactions) )
    # ion temps (burn-averaged)
    Ti = zeros( len(reactions) )
    # Bang (peak emission) times
    BT = zeros( len(reactions) )
    PeakRate = zeros( len(reactions) )
    
    # output files
    rateFile = csv.writer(open(os.path.join(OutputDir,'BurnRate.csv'),'w'))
    yieldFile = csv.writer(open(os.path.join(OutputDir,'Yield.csv'),'w'))
    TiFile = csv.writer(open(os.path.join(OutputDir,'Ti.csv'),'w'))
    BTFile = csv.writer(open(os.path.join(OutputDir,'BangTime.csv'),'w'))
    # construct header for rate file:
    rateFileHeader = ["t (s)"]
    for i in reactions:
        rateFileHeader.append( i[0] + " (1/s)" )
    rateFile.writerow( rateFileHeader )
    
    # time step:
    dt = impl.dt()
    #iterate over all time:
    for it in range( impl.it_tc(), impl.it_max() ):
        rateFileRow = [ impl.t(it) ]
        
        #iterate over reactions
        for i in range(len(reactions)):
            [dY, dTi] = rate(reactions[i],it)
            Y[i] += dY*dt
            Ti[i] += dTi*dt
            rateFileRow.append(dY)
            if dY > PeakRate[i]:
                BT[i] = impl.t(it)
                PeakRate[i] = dY

        #output
        rateFile.writerow( rateFileRow )
    
    #If there is yield for a species, do output:
    #iterate over reactions
    for i in range(len(reactions)):
        if Y[i] > 0:
            Ti[i] = Ti[i] / Y[i]
            print(reactions[i][0]+" yield = " + '{:.2e}'.format(Y[i]))
            print(reactions[i][0]+" Ti = " + '{:.2f}'.format(Ti[i]))
            print(reactions[i][0]+" BT = " + '{:.2e}'.format(BT[i]))
            yieldFile.writerow( [reactions[i][0],Y[i]] )
            TiFile.writerow( [reactions[i][0],Ti[i]] )
            BTFile.writerow( [reactions[i][0],BT[i]] )
