'''
@title RSA3DPlot
@author: Rebecca Coles
Updated on Apr 19, 2017
Created on Apr 14, 2017
'''

# Import #######################################################################################
from numpy import array, rot90, full, concatenate, zeros
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
        
    def coordTransform(self, SensorArray):
        '''
        Perform coordinate transform from PCS coordinate system to CCS coordinate system (180 degree rotation).
        '''
        return rot90(SensorArray,2)
    
    def createVirtualRSA(self, S00, S01, S02, S10, S11, S12, S20, S21, S22):
        '''
        Align data based on the sensor positions on the RSA.
        
        Sensor location buttons to open data files for each sensor (CCS Coordinate system)
            S22    S12    S02
            S21    S11    S01    ^
            S20    S10    S00    |+Y
                                 
                        <--+X    Ø +Z
        '''
        ###########################################################################
        ###Add Color column for later plotting
        ###########################################################################
        #REB0 Sensors
        #S00
        white = full((S00.shape[0],1), 'w')
        concatenate((S00, full((S00.shape[0],1), 'S00')), axis=1)
        concatenate((S00, white), axis=1)        
        #S01
        purple = full((S01.shape[0],1), '#be63d6')
        concatenate((S01, full((S01.shape[0],1), 'S01')), axis=1)
        concatenate((S01, purple), axis=1)
        #S02
        yellow = full((S02.shape[0],1), 'y')
        concatenate((S02, full((S02.shape[0],1), 'S02')), axis=1)
        concatenate((S02, yellow), axis=1)
        
        #REB1 Sensors
        #S10
        cyan = full((S10.shape[0],1), 'c')
        concatenate((S10, full((S10.shape[0],1), 'S10')), axis=1)
        concatenate((S10, cyan), axis=1)
        #S11
        blue = full((S11.shape[0],1), 'b')
        concatenate((S11, full((S11.shape[0],1), 'S11')), axis=1)
        concatenate((S11, blue), axis=1)
        #S12
        orange = full((S12.shape[0],1), '#ffa802')
        concatenate((S12, full((S12.shape[0],1), 'S12')), axis=1)
        concatenate((S12, orange), axis=1)
        
        #REB2 Sensors
        #S20
        magenta = full((S20.shape[0],1), 'm')
        concatenate((S20, full((S20.shape[0],1), 'S20')), axis=1)
        concatenate((S20, magenta), axis=1)
        #S21
        green = full((S21.shape[0],1), 'g')
        concatenate((S21, full((S21.shape[0],1), 'S21')), axis=1)
        concatenate((S21, green), axis=1)
        #S22
        red = full((S22.shape[0],1), 'r')
        concatenate((S22, full((S22.shape[0],1), 'S22')), axis=1)
        concatenate((S22, red), axis=1)    
        
        ###########################################################################
        ###Find max/min (this will be used to place the sensor in the virtual RSA)
        ###########################################################################
        #REB0 Sensors
        #S00
        S00XMax, S00YMax = S00.nanmax(axis=0)
        print(S00XMax, S00YMax)
        #S01
        S01XMax, S01YMax = S01.nanmax(axis=0)
        print(S01XMax, S01YMax)
        #S02
        S02XMax, S02YMax = S02.nanmax(axis=0)
        print(S02XMax, S02YMax)
        
        #REB1 Sensors
        #S10
        S10XMax, S10YMax = S10.nanmax(axis=0)
        print(S10XMax, S10YMax)
        #S11
        S11XMax, S11YMax = S11.nanmax(axis=0)
        print(S11XMax, S11YMax)
        #S12
        S12XMax, S12YMax = S12.nanmax(axis=0)
        print(S12XMax, S12YMax)
        
        #REB2 Sensors
        #S20
        S20XMax, S20YMax = S20.nanmax(axis=0)
        print(S20XMax, S20YMax)
        #S21
        S21XMax, S21YMax = S21.nanmax(axis=0)
        print(S21XMax, S21YMax)
        #S22
        S22XMax, S22YMax = S22.nanmax(axis=0)
        print(S22XMax, S22YMax)
        
        ###########################################################################
        ###Turn list into CCD shaped array
        ###########################################################################   
        
        ###########################################################################
        ###Rotate sensors (coord transform from PCS to CCS coordinate systems)
        ###########################################################################   
        
        ###########################################################################
        ###Place sensors in RSA positions
        ###########################################################################
        #Create RSA array
        xx = S00.shape[0] + S01.shape[0] + S02.shape[0] + S10.shape[0] + S11.shape[0] + S12.shape[0] + S20.shape[0] + S21.shape[0] + S22.shape[0]
        yy = S00.shape[1] + S01.shape[1] + S02.shape[1] + S10.shape[1] + S11.shape[1] + S12.shape[1] + S20.shape[1] + S21.shape[1] + S22.shape[1]
        RSAarray = zeros(xx, yy)
        
        #Place sensors: from left to right and top to bottom
        #Sensor location buttons to open data files for each sensor (CCS Coordinate system)
        #    S22    S12    S02
        #    S21    S11    S01    ^
        #    S20    S10    S00    |+Y
        #                         
        #                <--+X    Ø +Z
        #This will be done by adding the appropriate value to each X and Y values 
        #    so that the plot will show the data in the proper position in a plot
        #S22
        
        #S12
        #S02
        #S21
        #S11
        #S01
        #S20
        #S10
        #S00
        
        
    def plotSensors3D(self):
        '''
        Plot RSA sensor array in 3D
        '''