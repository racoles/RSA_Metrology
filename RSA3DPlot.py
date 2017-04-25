'''
@title RSA3DPlot
@author: Rebecca Coles
Updated on Apr 19, 2017
Created on Apr 14, 2017
'''

# Import #######################################################################################
from numpy import array, full, concatenate, copy, empty, savetxt
import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show
################################################################################################

class RSA3DPlot(object):
    '''
    3D plot RSA data
    '''

    def __init__(self, S00List, S01List, S02List, S10List, S11List, S12List, S20List, S21List, S22List, ManualOrAutoBOOL):
        '''
        Constructor
        '''
        self.createVirtualRSA(S00List, S01List, S02List, S10List, S11List, S12List, S20List, S21List, S22List, ManualOrAutoBOOL)
        
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
        #Insert CCS Y coordinates into array
        sensorCCS = copy(sensorPCS)
        sensorCCS[:,1] = yValues
        return sensorCCS
        
        
    
    def createVirtualRSA(self, S00List, S01List, S02List, S10List, S11List, S12List, S20List, S21List, S22List, ManualOrAutoBOOL):
        '''
        Align data based on the sensor positions on the RSA.
        
        Sensor location buttons to open data files for each sensor (CCS Coordinate system)
            S22    S12    S02
            S21    S11    S01    ^
            S20    S10    S00    |+Y
                                 
                        <--+X    Ø +Z
                        
        ManualOrAutoBOOL = 0: Manual sensor position.
        ManualOrAutoBOOL = 1: Auto calculate sensor position for optimal flatness.
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
        ###Find max/min (this will be used to coordinate transform the sensor from PCS to CCS)
        ###########################################################################
        #REB0 Sensors
        S00XMax, S00YMax = S00.nanmax(axis=0)
        S01XMax, S01YMax = S01.nanmax(axis=0)
        S02XMax, S02YMax = S02.nanmax(axis=0)
        #REB1 Sensors
        S10XMax, S10YMax = S10.nanmax(axis=0)
        S11XMax, S11YMax = S11.nanmax(axis=0)
        S12XMax, S12YMax = S12.nanmax(axis=0)
        #REB2 Sensors
        S20XMax, S20YMax = S20.nanmax(axis=0)
        S21XMax, S21YMax = S21.nanmax(axis=0)
        S22XMax, S22YMax = S22.nanmax(axis=0)
        
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
        timestr = 'none.csv'
        if ManualOrAutoBOOL == 0:
            RSAArray = self.manualPlacement(S00CCS, S01CCS, S02CCS, S10CCS, S11CCS, S12CCS, S20CCS, S21CCS, S22CCS)
            timestr = time.strftime("%Y%m%d-%H%M%S") + '_manually_placed_virtualRSA.csv'
        #elif ManualOrAutoBOOL == 1:
        
        ###########################################################################
        ###Save virtual RSA to text file
        ###########################################################################
        savetxt(timestr, RSAArray, delimiter=',')

    def manualPlacement(self, S00CCS, S01CCS, S02CCS, S10CCS, S11CCS, S12CCS, S20CCS, S21CCS, S22CCS):
        '''
        Manually Place sensors in RSA positions

        Place sensors: from right to left and bottom to top (to follow the CCS Coordinate system).
        Sensor location buttons to open data files for each sensor (CCS Coordinate system).
            S22    S12    S02
            S21    S11    S01    ^
            S20    S10    S00    |+Y
                                 
                        <--+X    Ø +Z
        This will be done by adding the appropriate value to each X and Y values 
            so that the data will show the proper position in a plot
        '''
        #Create numpy RSA array
        RSAArray = empty(0,4)
        
        #Place sensors
        #S00
        concatenate((RSAArray, S00CCS))
        #S10 (next to S00): S10X + S00Xmax
        S00CCSXMax, S00CCSYMax = S00CCS.nanmax(axis=0)
        S10CCS[:,0] + S00CCSXMax #X
        concatenate((RSAArray, S10CCS))
        #S20 (next to S10): S20X + S10Xmax + S00XMax
        S10CCSXMax, S10CCSYMax = S10CCS.nanmax(axis=0)
        S20CCS[:,0] + S10CCSXMax #X (S10X already has S00X added to it)
        concatenate((RSAArray, S20CCS))
        #S01 (on top of S00): S01Y + S00CCSYmax)
        S01CCS[:,1] + S00CCSYMax #Y
        concatenate((RSAArray, S01CCS))
        #S11 (on top of S10 AND next to S01)
        S01CCSXMax, S01CCSYMax = S01CCS.nanmax(axis=0)
        S11CCS[:,0] + S01CCSXMax #X
        S11CCS[:,1] + S10CCSYMax #Y
        concatenate((RSAArray, S11CCS))
        #S21 (on top of S20 AND next to S11)
        S20CCSXMax, S20CCSYMax = S20CCS.nanmax(axis=0)
        S11CCSXMax, S11CCSYMax = S11CCS.nanmax(axis=0)
        S21CCS[:,0] + S11CCSXMax #X (S11X already has S01X added to it)
        S21CCS[:,1] + S20CCSYMax
        concatenate((RSAArray, S21CCS))
        #S02 (on top of S00 and S01)
        S02CCS[:,1] + S01CCSYMax #Y (S01Y already has S00Y added to it)
        concatenate((RSAArray, S02CCS))
        #S12 (on top of S10 and S11 AND next to S02)
        S02CCSXMax, S02CCSYMax = S02CCS.nanmax(axis=0)
        S12CCS[:,0] + S02CCSXMax #X
        S12CCS[:,1] + S11CCSYMax #Y (S11Y already has S10Y added to it)
        concatenate((RSAArray, S12CCS))
        #S22 (on top of S21 and S20 AND next to S12 and S02)
        S12CCSXMax, S12CCSYMax = S02CCS.nanmax(axis=0)
        S21CCSXMax, S21CCSYMax = S21CCS.nanmax(axis=0)
        S22CCS[:,0] + S12CCSXMax #X (S12X already has S02X added to it)
        S22CCS[:,1] + S21CCSYMax #Y (S21Y already has S20Y added to it)
        
        return RSAArray
        
    def plotSensors3D(self, RSAArray):
        '''
        Plot RSA sensor array in 3D
        '''
        #Set up figure
        fig = figure()
        ax = fig.add_subplot(111, projection='3d')
        #Plot points (loop is used to make sure that sensor points are the proper colors)
        for ii in range(0,RSAArray.shape[0]-1):
            ax.scatter(RSAArray[ii,0], RSAArray[ii,1], RSAArray[ii,2], c=RSAArray[ii,3], marker='o')
        #Label axis
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #Show plot
        show()
        