'''
@title RSA3DPlot
@author: Rebecca Coles
Updated on Apr 19, 2017
Created on Apr 14, 2017
'''

# Import #######################################################################################
from numpy import array, rot90, full, concatenate
################################################################################################

class RSA3DPlot(object):
    '''
    3D plot RSA data
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    def convertToNumpy(self, RSAList):
        '''
        Convert python list to numpy array
        '''
        return array(RSAList)
        
    def coordTransform(self, RSAarray):
        '''
        Perform coordinate transform from PCS coordinate system to CCS coordinate system (180 degree rotation).
        '''
        return rot90(RSAarray,2)
    
    def createVirtualRSA(self, S00, S01, S02, S10, S11, S12, S20, S21, S22):
        '''
        Align data based on the sensor positions on the RSA.
        
        Sensor location buttons to open data files for each sensor (CCS Coordinate system)
            S22    S12    S02
            S21    S11    S01    ^
            S20    S10    S00    |+Y
                                 
                        <--+X    Ø +Z
        '''
        #REB0 Sensors
        #S00: find max/min and add plot color
        S00XMax, S00YMax = S00.max(axis=0)
        print(S00XMax, S00YMax)
        white = full((S00.shape[0],1), 'w')
        concatenate((S00, white), axis=1)
        #S01: find max/min and add plot color
        S01XMax, S01YMax = S01.max(axis=0)
        print(S01XMax, S01YMax)
        purple = full((S01.shape[0],1), '#be63d6')
        concatenate((S01, purple), axis=1)
        #S02: find max/min and add plot color
        S02XMax, S02YMax = S02.max(axis=0)
        print(S02XMax, S02YMax)
        yellow = full((S02.shape[0],1), 'y')
        concatenate((S02, yellow), axis=1)
        
        #REB1 Sensors
        #S10: find max/min and add plot color
        S10XMax, S10YMax = S10.max(axis=0)
        print(S10XMax, S10YMax)
        cyan = full((S10.shape[0],1), 'c')
        concatenate((S10, cyan), axis=1)
        #S11: find max/min and add plot color
        S11XMax, S11YMax = S11.max(axis=0)
        print(S11XMax, S11YMax)
        blue = full((S11.shape[0],1), 'b')
        concatenate((S11, blue), axis=1)
        #S12: find max/min and add plot color
        S12XMax, S12YMax = S12.max(axis=0)
        print(S12XMax, S12YMax)
        orange = full((S12.shape[0],1), '#ffa802')
        concatenate((S12, orange), axis=1)
        
        #REB2 Sensors
        #S20: find max/min and add plot color
        S20XMax, S20YMax = S20.max(axis=0)
        print(S20XMax, S20YMax)
        magenta = full((S20.shape[0],1), 'm')
        concatenate((S20, magenta), axis=1)
        #S21: find max/min and add plot color
        S21XMax, S21YMax = S21.max(axis=0)
        print(S21XMax, S21YMax)
        green = full((S21.shape[0],1), 'g')
        concatenate((S21, green), axis=1)
        #S22: find max/min and add plot color
        S22XMax, S22YMax = S22.max(axis=0)
        print(S22XMax, S22YMax)
        red = full((S22.shape[0],1), 'r')
        concatenate((S22, red), axis=1)
        
        #REB0 Sensors
        #Place S00 at CCS coordinate (0,0)
        #Place S01 on top of S00
        #Place S02 on top of S01
        
        #REB1 Sensors
        #Place S11 on top of S10
        #Place S12 on top of S11
        
        #REB2 Sensors
        #Place S21 on top of S20
        #Place S22 on top of S21
    def plotSensors3D(self):
        '''
        Plot RSA sensor array in 3D
        '''