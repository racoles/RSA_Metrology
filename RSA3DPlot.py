'''
@title RSA3DPlot
@author: Rebecca Coles
Updated on Apr 19, 2017
Created on Apr 14, 2017
'''

# Import #######################################################################################
from numpy import array, full, concatenate, copy, empty
################################################################################################

class RSA3DPlot(object):
    '''
    3D plot RSA data
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def coordTransform(self, sensorPCS, Ymax):
        '''
        Perform coordinate transform from PCS coordinate system to CCS coordinate system (180 degree rotation).
        CCS --->+X
         |   __________
         +Y |        o |
            |          |
            |          |  
         +Y |          |
         |  |_o______o_|
        PCS --->+X
        
        X(CCS) = X(PCS)
        Y(CCS) = Y(PCS)MAX - Y(PCS)
        '''
        #Coordinate transform Y values
        yValues = copy(sensorPCS[:,1])
        yValues = [Ymax-yy for yy in yValues]
        print(yValues)
        #Insert CCS Y coordinates into array
        sensorCCS = copy(sensorPCS)
        sensorCCS[:,1] = yValues
        return sensorCCS
        
        
    
    def createVirtualRSA(self, S00List, S01List, S02List, S10List, S11List, S12List, S20List, S21List, S22List):
        '''
        Align data based on the sensor positions on the RSA.
        
        Sensor location buttons to open data files for each sensor (CCS Coordinate system)
            S22    S12    S02
            S21    S11    S01    ^
            S20    S10    S00    |+Y
                                 
                        <--+X    Ø +Z
        '''
        ###########################################################################
        ###Convert from Python list to Numpy array
        ###########################################################################
        #REB0
        S00 = array(S00List)
        S01 = array(S01List)
        S02 = array(S02List)
        #REB1
        S10 = array(S10List)
        S11 = array(S11List)
        S12 = array(S12List)
        #REB2
        S20 = array(S20List)
        S21 = array(S21List)
        S22 = array(S22List)
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
        S01XMax, S01YMax = S01.nanmax(axis=0)
        print(S01XMax, S01YMax)
        S02XMax, S02YMax = S02.nanmax(axis=0)
        print(S02XMax, S02YMax)
        
        #REB1 Sensors
        S10XMax, S10YMax = S10.nanmax(axis=0)
        print(S10XMax, S10YMax)
        S11XMax, S11YMax = S11.nanmax(axis=0)
        print(S11XMax, S11YMax)
        S12XMax, S12YMax = S12.nanmax(axis=0)
        print(S12XMax, S12YMax)
        
        #REB2 Sensors
        #S20
        S20XMax, S20YMax = S20.nanmax(axis=0)
        print(S20XMax, S20YMax)
        S21XMax, S21YMax = S21.nanmax(axis=0)
        print(S21XMax, S21YMax)
        S22XMax, S22YMax = S22.nanmax(axis=0)
        print(S22XMax, S22YMax)
        
        ###########################################################################
        ###Rotate sensors (coordinate transform from PCS to CCS coordinate systems)
        ###########################################################################
        #REB0
        S00CCS = self.coordTransform(S00, S00YMax)
        S01CCS = self.coordTransform(S01, S01YMax)
        S02CCS = self.coordTransform(S02, S02YMax)
        #REB1
        S10CCS = self.coordTransform(S10, S10YMax)
        S11CCS = self.coordTransform(S11, S11YMax)
        S12CCS = self.coordTransform(S12, S12YMax)
        #REB2
        S20CCS = self.coordTransform(S20, S20YMax)
        S21CCS = self.coordTransform(S21, S21YMax)
        S22CCS = self.coordTransform(S22, S22YMax)
        
        ###########################################################################
        ###Place sensors in RSA positions
        ###########################################################################
        #Place sensors: from right to left and bottom to top (to follow the CCS Coordinate system).
        #Sensor location buttons to open data files for each sensor (CCS Coordinate system).
        #    S22    S12    S02
        #    S21    S11    S01    ^
        #    S20    S10    S00    |+Y
        #                         
        #                <--+X    Ø +Z
        #This will be done by adding the appropriate value to each X and Y values 
        #    so that the data will show the proper position in a plot
        #
        #Create numpy RSA array
        RSAArray = empty(0,4)
        #S00
        concatenate((RSAArray, S00CCS))
        #S10 (next to S00): S10X + S00Xmax
        S10CCS[:,0] + S00XMax
        concatenate((RSAArray, S10CCS))
        #S20 (next to S10): S20X + S10Xmax + S00XMax
        S20CCS[:,0] + S10XMax + S00XMax
        concatenate((RSAArray, S20CCS))
        #S01 (on top of S00): S01Y + S00CCSYmax)
        S00CCSXMax, S00CCSYMax = S00CCS.nanmax(axis=0)
        S01CCS[:,1] + S00CCSYMax
        concatenate((RSAArray, S01CCS))
        #S11 (on top of S10 AND next to S01)
        
        
    def plotSensors3D(self):
        '''
        Plot RSA sensor array in 3D
        '''