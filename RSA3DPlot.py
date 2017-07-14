'''
@title RSA3DPlot
@author: Rebecca Coles
Updated on Jul 11, 2017
Created on Apr 14, 2017
'''

# Import #######################################################################################
from numpy import array, full, concatenate, copy, empty, savetxt, nanmax
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
################################################################################################

class RSA3DPlot(object):
    '''
    3D plot RSA data
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def _coordTransformSensorCCS(self, sensorPCS, Ymax):
        '''
        Perform coordinate transform from PCS coordinate system to CCS coordinate system for Sensors (180 degree rotation).
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
        
    def _coordTransformSensorMCS(self, sensorPCS, Xmax, Ymax):
        '''
        Perform coordinate transform from PCS coordinate system to CCS coordinate system for Sensors (180 degree rotation).
                 +X<---MCS
             __________  |
            |        o | +Y
            |          |
            |          |  
         +Y |          |
         |  |_o______o_|
        PCS --->+X
        
        X(CCS) = X(PCS)
        Y(CCS) = Y(PCS)MAX - Y(PCS)
        '''
        #Coordinate transform X values
        xValues = copy(sensorPCS[:,0])
        xValues = [Xmax-xx for xx in xValues]    
        #Coordinate transform Y values
        yValues = copy(sensorPCS[:,1])
        yValues = [Ymax-yy for yy in yValues]
        #Insert CCS X coordinates into array
        sensorCCS = copy(sensorPCS)
        sensorCCS[:,0] = xValues    
        #Insert CCS Y coordinates into array
        sensorCCS[:,1] = yValues
        return sensorCCS
    
    def _coordTransformBasePlate(self):
        '''
        Perform coordinate transform from MCS coordinate system to CCS coordinate system for RAFT Base Plate(180 degree rotation).
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
    
    def createVirtualRSA(self, S00List, S01List, S02List, S10List, S11List, S12List, S20List, S21List, S22List, ManualOrAutoBOOL, datumPlaneEntry, raftFitEntry):
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
        S00 = self._reshape_3D_to_2D(array(S00List))
        S01 = self._reshape_3D_to_2D(array(S01List))
        S02 = self._reshape_3D_to_2D(array(S02List))
        #REB1
        S10 = self._reshape_3D_to_2D(array(S10List))
        S11 = self._reshape_3D_to_2D(array(S11List))
        S12 = self._reshape_3D_to_2D(array(S12List))
        #REB2
        S20 = self._reshape_3D_to_2D(array(S20List))
        S21 = self._reshape_3D_to_2D(array(S21List))
        S22 = self._reshape_3D_to_2D(array(S22List))
        
        ###########################################################################
        ###Add Color column for later plotting
        ###########################################################################
        #REB0 Sensors
        #S00
        white = full((S00.shape[0],1), 0)
        S00 = concatenate((S00, white), axis=1)
        #S01
        purple = full((S01.shape[0],1), 1) # #be63d6
        S01 = concatenate((S01, purple), axis=1)
        #S02
        yellow = full((S02.shape[0],1), 2)
        S02 = concatenate((S02, yellow), axis=1)
        
        #REB1 Sensors
        #S10
        cyan = full((S10.shape[0],1), 3)
        S10 = concatenate((S10, cyan), axis=1)
        #S11
        blue = full((S11.shape[0],1), 4)
        S11 = concatenate((S11, blue), axis=1)
        #S12
        orange = full((S12.shape[0],1), 5) # #ffa802
        S12 = concatenate((S12, orange), axis=1)
        
        #REB2 Sensors
        #S20
        magenta = full((S20.shape[0],1), 6)
        S20 = concatenate((S20, magenta), axis=1)
        #S21
        green = full((S21.shape[0],1), 7)
        S21 = concatenate((S21, green), axis=1)
        #S22
        red = full((S22.shape[0],1), 8)
        S22 = concatenate((S22, red), axis=1)
        
        self.colorList = [['S00', 'w'], ['S01', '#be63d6'], ['S02', 'y'], 
                          ['S10', 'c'], ['S11', 'b'], ['S12', '#ffa802'],
                          ['S20', 'm'], ['S21', 'g'], ['S22', 'r']]
        
        ###########################################################################
        ###Find max (this will be used to coordinate transform the sensor from PCS to CCS)
        ###########################################################################
        #REB0 Sensors
        #_, S00YMax, _, _  = nanmax(S00, axis=0)
        #_, S01YMax, _, _  = nanmax(S01, axis=0)
        #_, S02YMax, _, _  = nanmax(S02, axis=0)
        #REB1 Sensors
        #_, S10YMax, _, _  = nanmax(S10, axis=0)
        #_, S11YMax, _, _  = nanmax(S11, axis=0)
        #_, S12YMax, _, _  = nanmax(S12, axis=0)
        #REB2 Sensors
        #_, S20YMax, _, _  = nanmax(S20, axis=0)
        #_, S21YMax, _, _  = nanmax(S21, axis=0)
        #_, S22YMax, _, _  = nanmax(S22, axis=0)
        
        ###########################################################################
        ###Find max (this will be used to coordinate transform the sensor from PCS to MCS)
        ###########################################################################
        #REB0 Sensors
        S00XMax, S00YMax, _, _  = nanmax(S00, axis=0)
        S01XMax, S01YMax, _, _  = nanmax(S01, axis=0)
        S02XMax, S02YMax, _, _  = nanmax(S02, axis=0)
        #REB1 Sensors
        S10XMax, S10YMax, _, _  = nanmax(S10, axis=0)
        S11XMax, S11YMax, _, _  = nanmax(S11, axis=0)
        S12XMax, S12YMax, _, _  = nanmax(S12, axis=0)
        #REB2 Sensors
        S20XMax, S20YMax, _, _  = nanmax(S20, axis=0)
        S21XMax, S21YMax, _, _  = nanmax(S21, axis=0)
        S22XMax, S22YMax, _, _  = nanmax(S22, axis=0)
        
        ###########################################################################
        ###Rotate sensors (coordinate transform from PCS to CCS coordinate systems)
        ###########################################################################
        #REB0
        #S00CCS = self._coordTransformSensorCCS(S00, S00YMax)
        #S01CCS = self._coordTransformSensorCCS(S01, S01YMax)
        #S02CCS = self._coordTransformSensorCCS(S02, S02YMax)
        #REB1
        #S10CCS = self._coordTransformSensorCCS(S10, S10YMax)
        #S11CCS = self._coordTransformSensorCCS(S11, S11YMax)
        #S12CCS = self._coordTransformSensorCCS(S12, S12YMax)
        #REB2
        #S20CCS = self._coordTransformSensorCCS(S20, S20YMax)
        #S21CCS = self._coordTransformSensorCCS(S21, S21YMax)
        #S22CCS = self._coordTransformSensorCCS(S22, S22YMax)
        
        ###########################################################################
        ###Rotate sensors (coordinate transform from PCS to MCS coordinate systems)
        ###########################################################################
        #REB0
        S00CCS = self._coordTransformSensorMCS(S00, S00XMax, S00YMax)
        S01CCS = self._coordTransformSensorMCS(S01, S01XMax, S01YMax)
        S02CCS = self._coordTransformSensorMCS(S02, S02XMax, S02YMax)
        #REB1
        S10CCS = self._coordTransformSensorMCS(S10, S10XMax, S10YMax)
        S11CCS = self._coordTransformSensorMCS(S11, S11XMax, S11YMax)
        S12CCS = self._coordTransformSensorMCS(S12, S12XMax, S12YMax)
        #REB2
        S20CCS = self._coordTransformSensorMCS(S20, S20XMax, S20YMax)
        S21CCS = self._coordTransformSensorMCS(S21, S21XMax, S21YMax)
        S22CCS = self._coordTransformSensorMCS(S22, S22XMax, S22YMax)
        
        ###########################################################################
        ###Place sensors in RSA positions (CCS)
        ###########################################################################
        #timestr = 'none.csv'
        #if ManualOrAutoBOOL == 0:
        #    RSAArray = self.manualPlacementCCS(S00CCS, S01CCS, S02CCS, S10CCS, S11CCS, S12CCS, S20CCS, S21CCS, S22CCS)
        #    timestr = time.strftime("%Y%m%d-%H%M%S") + '_manually_placed_virtualRSA.csv'
        #elif ManualOrAutoBOOL == 1:
        
        ###########################################################################
        ###Place sensors in RSA positions (MCS)
        ###########################################################################
        timestr = 'none.csv'
        if ManualOrAutoBOOL == 0:
            RSAArray = self.manualPlacementMCS(S00CCS, S01CCS, S02CCS, S10CCS, S11CCS, S12CCS, S20CCS, S21CCS, S22CCS)
            timestr = time.strftime("%Y%m%d-%H%M%S") + '_manually_placed_virtualRSA.csv'
        #elif ManualOrAutoBOOL == 1:
        
        ###########################################################################
        ###Save virtual RSA to text file
        ###########################################################################
        savetxt(timestr, RSAArray, fmt=['%.7f','%.7f','%.7f','%.0f'], delimiter=',')

        ###########################################################################
        ###Plot Virtual RSA
        ###########################################################################
        self._plotSensors3D(RSAArray, self.colorList)        
                
    def manualPlacementCCS(self, S00CCS, S01CCS, S02CCS, S10CCS, S11CCS, S12CCS, S20CCS, S21CCS, S22CCS):
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
        RSAArray = empty((0,4))
        
        #Place sensors
        #S00
        RSAArray = concatenate((RSAArray, S00CCS))
        #S10 (next to S00): S10X + S00Xmax
        S00CCSXMax, S00CCSYMax, _, _ = nanmax(S00CCS, axis=0)
        S10CCS[:,0] = S10CCS[:,0] + S00CCSXMax #X
        RSAArray = concatenate((RSAArray, S10CCS))
        #S20 (next to S10): S20X + S10Xmax + S00XMax
        S10CCSXMax, S10CCSYMax, _, _ = nanmax(S10CCS, axis=0)
        S20CCS[:,0] = S20CCS[:,0] + S10CCSXMax #X (S10X already has S00X added to it)
        RSAArray = concatenate((RSAArray, S20CCS))
        #S01 (on top of S00): S01Y + S00CCSYmax)
        S01CCS[:,1] = S01CCS[:,1] + S00CCSYMax #Y
        RSAArray = concatenate((RSAArray, S01CCS))
        #S11 (on top of S10 AND next to S01)
        S01CCSXMax, S01CCSYMax, _, _ = nanmax(S01CCS, axis=0)
        S11CCS[:,0] = S11CCS[:,0] + S01CCSXMax #X
        S11CCS[:,1] = S11CCS[:,1] + S10CCSYMax #Y
        RSAArray = concatenate((RSAArray, S11CCS))
        #S21 (on top of S20 AND next to S11)
        _, S20CCSYMax, _, _ = nanmax(S20CCS, axis=0)
        S11CCSXMax, S11CCSYMax, _, _ = nanmax(S11CCS, axis=0)
        S21CCS[:,0] = S21CCS[:,0] + S11CCSXMax #X (S11X already has S01X added to it)
        S21CCS[:,1] = S21CCS[:,1] + S20CCSYMax
        RSAArray = concatenate((RSAArray, S21CCS))
        #S02 (on top of S00 and S01)
        S02CCS[:,1] = S02CCS[:,1] + S01CCSYMax #Y (S01Y already has S00Y added to it)
        RSAArray = concatenate((RSAArray, S02CCS))
        #S12 (on top of S10 and S11 AND next to S02)
        S02CCSXMax, _, _, _ = nanmax(S02CCS, axis=0)
        S12CCS[:,0] = S12CCS[:,0] + S02CCSXMax #X
        S12CCS[:,1] = S12CCS[:,1] + S11CCSYMax #Y (S11Y already has S10Y added to it)
        RSAArray = concatenate((RSAArray, S12CCS))
        #S22 (on top of S21 and S20 AND next to S12 and S02)
        S12CCSXMax, _, _, _ = nanmax(S12CCS, axis=0)
        _, S21CCSYMax, _, _ = nanmax(S21CCS, axis=0)
        S22CCS[:,0] = S22CCS[:,0] + S12CCSXMax #X (S12X already has S02X added to it)
        S22CCS[:,1] = S22CCS[:,1] + S21CCSYMax #Y (S21Y already has S20Y added to it)
        RSAArray = concatenate((RSAArray, S22CCS))
        
        return RSAArray
    
    def manualPlacementMCS(self, S00MCS, S01MCS, S02MCS, S10MCS, S11MCS, S12MCS, S20MCS, S21MCS, S22MCS):
        '''
        Manually Place sensors in RSA positions

        Place sensors: from left to right and bottom to top (to follow the MCS Coordinate system).
            S22    S12    S02
        ^   S21    S11    S01
        |+Y S20    S10    S00                        
        Ø +Z --->+X
        This will be done by adding the appropriate value to each X and Y values 
            so that the data will show the proper position in a plot
        '''
        #Create numpy RSA array
        RSAArray = empty((0,4))
        
        #Place sensors (left to right,bottom to top)
        #S20
        RSAArray = concatenate((RSAArray, S20MCS))
        #S10 (next to S20): S10X + S20Xmax
        S20MCSXMax, S20MCSYMax, _, _ = nanmax(S20MCS, axis=0)
        S10MCS[:,0] = S10MCS[:,0] + S20MCSXMax #X
        RSAArray = concatenate((RSAArray, S10MCS))
        #S00 (next to S10): S20X + S10XMax + S00X
        S10MCSXMax, S10MCSYMax, _, _ = nanmax(S10MCS, axis=0)
        S00MCS[:,0] = S00MCS[:,0] + S10MCSXMax #X (S10X already has S20X added to it)
        RSAArray = concatenate((RSAArray, S00MCS))
        #S21 (on top of S20): S21Y + S20CCSYmax)
        S21MCS[:,1] = S21MCS[:,1] + S20MCSYMax #Y
        RSAArray = concatenate((RSAArray, S21MCS))
        #S11 (on top of S10 AND next to S21)
        S21MCSXMax, S21MCSYMax, _, _ = nanmax(S21MCS, axis=0)
        S11MCS[:,0] = S11MCS[:,0] + S21MCSXMax #X
        S11MCS[:,1] = S11MCS[:,1] + S10MCSYMax #Y
        RSAArray = concatenate((RSAArray, S11MCS))
        #S01 (on top of S00 AND next to S11)
        _, S00MCSYMax, _, _ = nanmax(S00MCS, axis=0)
        S11MCSXMax, S11MCSYMax, _, _ = nanmax(S11MCS, axis=0)
        S01MCS[:,0] = S01MCS[:,0] + S11MCSXMax #X (S11X already has S21X added to it)
        S01MCS[:,1] = S01MCS[:,1] + S00MCSYMax
        RSAArray = concatenate((RSAArray, S01MCS))
        #S22 (on top of S20 and S21)
        S22MCS[:,1] = S22MCS[:,1] + S21MCSYMax #Y (S21Y already has S20Y added to it)
        RSAArray = concatenate((RSAArray, S22MCS))
        #S12 (on top of S10 and S11 AND next to S22)
        S22MCSXMax, _, _, _ = nanmax(S22MCS, axis=0)
        S12MCS[:,0] = S12MCS[:,0] + S22MCSXMax #X
        S12MCS[:,1] = S12MCS[:,1] + S11MCSYMax #Y (S11Y already has S10Y added to it)
        RSAArray = concatenate((RSAArray, S12MCS))
        #S02 (on top of S01 and S00 AND next to S12 and S22)
        S12MCSXMax, _, _, _ = nanmax(S12MCS, axis=0)
        _, S01MCSYMax, _, _ = nanmax(S01MCS, axis=0)
        S02MCS[:,0] = S02MCS[:,0] + S12MCSXMax #X (S12X already has S22X added to it)
        S02MCS[:,1] = S02MCS[:,1] + S01MCSYMax #Y (S01Y already has S00Y added to it)
        RSAArray = concatenate((RSAArray, S02MCS))
        
        return RSAArray
        
    def _plotSensors3D(self, RSAArray, colorList):
        '''
        Plot RSA sensor array in 3D
        '''
        #Set up figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #Plot every tenth point (loop is used to make sure that sensor points are the proper colors)
        for ii in range(0,RSAArray.shape[0]-1, 10):
            ax.scatter(RSAArray[ii,0], RSAArray[ii,1], RSAArray[ii,2], c=colorList[int(RSAArray[ii,3])][1], marker='o')
        #Label axis
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #Set limits
        plt.gca().set_xlim(left=0)
        plt.gca().set_ylim(bottom=0)
        #Move Y axis to oposite side
        ax.view_init(ax.elev, ax.azim+270)
        #Flip Z axis
        #ax.invert_zaxis()
        #Show plot
        plt.show()
        
    def _reshape_3D_to_2D(self, numpyArray):
        '''
        reshape a 3D numpy array of size (1,#,#) to (#,#)
        '''
        if numpyArray.shape[0] == 1:
            return numpyArray.reshape(numpyArray.shape[1:])
        
    def _subtractRaftData(self, datumPlaneEntry, raftFitEntry):
        '''
        Subtract Datum Plane Equation from Raft Plane Equation
        '''
        #Remove spaces from String
        #Split string into array
        #Matrix subtraction (raft - datum plane
        #Return 1x3 array