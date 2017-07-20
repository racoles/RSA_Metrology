'''
@title RSA3DPlot
@author: Rebecca Coles
Updated on Jul 20, 2017
Created on Apr 14, 2017
'''

# Import #######################################################################################
from numpy import array, full, concatenate, copy, empty, savetxt, nanmax, nanmin, meshgrid, linspace
from re import findall
from mpl_toolkits.mplot3d import Axes3D
from statistics import median
import time
import matplotlib.pyplot as plt
import scipy.interpolate
################################################################################################

class RSA3DPlot(object):
    '''
    3D plot RSA data
    '''
    #Znom is the height that the sensor height is measured relative to.
    znom = 13000 #13mm

    def __init__(self):
        '''
        Constructor
        '''
        
    def _coordTransformSensorMCS(self, sensorPCS, Xmax, Ymax):
        '''
        Perform coordinate transform a sensor from PCS coordinate 
        system to CCS coordinate system for Sensors (180 degree rotation).
        
         CCS---> +X <---MCS
         |   __________   |
         +Y |        o |  +Y
            |          |
            |          |  
            |          |
         +Y |_o______o_|
         |
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
        sensorMCS = copy(sensorPCS)
        sensorMCS[:,0] = xValues    
        #Insert CCS Y coordinates into array
        sensorMCS[:,1] = yValues
        return sensorMCS
    
    def createVirtualRSA(self, S00List, S01List, S02List, S10List, S11List, S12List, S20List, S21List, S22List, 
                         ManualOrAutoBOOL, datumPlaneEqn, raftFitEqn):
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
        ###Place sensors in RSA positions (MCS)
        ###########################################################################
        timestr = 'none.csv'
        if ManualOrAutoBOOL == 0:
            RSAArray = self.manualPlacementMCS(S00CCS, S01CCS, S02CCS, S10CCS, S11CCS, S12CCS, S20CCS, S21CCS, S22CCS)
            timestr = time.strftime("%Y%m%d-%H%M%S") + '_manually_placed_virtualRSA.csv'
        #elif ManualOrAutoBOOL == 1:
        
        ###########################################################################
        ###Subtract Raft Base Plate from Virtual RSA
        ###########################################################################
        #Subtract the datum plane eqn from the raft fit eqn.
        raftBasePlateEqn = self._subtractRaftData(datumPlaneEqn, raftFitEqn)
        ##Add Raft Base Plate Plane to Virtual RSA
            #Note: raftBasePlateEqn is an array like [a,b,c] where: z = a + bx +cy
        for ii in range(0,(len(RSAArray))):
            RSAArray[ii,2] = (RSAArray[ii,2] + self.znom) 
            + (raftBasePlateEqn[0] + raftBasePlateEqn[1]*RSAArray[ii,0] + raftBasePlateEqn[2]*RSAArray[ii,1])

        ###########################################################################
        ###Save virtual RSA to text file
        ###########################################################################
        savetxt(timestr, RSAArray, fmt=['%.7f','%.7f','%.7f','%.0f'], delimiter=',')

        ###########################################################################
        ###Plot Virtual RSA
        ###########################################################################
        self._plotSensors3D(RSAArray, self.colorList)        
    
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
        ###########################################################################
        ###Plot Virtual RSA
        ###########################################################################
        #Set up figure
        fig = plt.figure(1)
        fig.canvas.set_window_title('Virtual RSA') 
        ax = Axes3D(fig) #instead of ax = fig.add_subplot(111, projection='3d')
        #Plot every tenth point (loop is used to make sure that sensor points are the proper colors)
        for ii in range(0,RSAArray.shape[0]-1, 10):
            ax.scatter(RSAArray[ii,0], RSAArray[ii,1], RSAArray[ii,2], c=colorList[int(RSAArray[ii,3])][1], marker='o')
        #Label axis
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.set_zlabel('Z (um)')
        #Set limits
        plt.gca().set_xlim(left=0)
        plt.gca().set_ylim(bottom=0)
        #Move Y axis to opposite side
        ax.view_init(ax.elev, ax.azim+270)
        #Suppress Z axis scientific notation
        ax.w_zaxis.get_major_formatter().set_useOffset(False)
        #Add raft labels (X+, X-, Y+, Y-)
        XMax, YMax, ZMax, _ = nanmax(RSAArray, axis=0)
        XMin, YMin, ZMin, _ = nanmin(RSAArray, axis=0)
        ax.text(median(RSAArray[:,0]), -20, ZMin, '-Y', size=15, zorder=1, clip_on=False, color='k') #-Y
        ax.text(-20, median(RSAArray[:,1]), ZMin, '+X', size=15, zorder=1, clip_on=False,  color='k') #+X
        ax.text(median(RSAArray[:,0]), YMax+20, ZMin, '+Y', size=15, zorder=1, clip_on=False,  color='k') #+Y
        ax.text(XMax+20, median(RSAArray[:,1]), ZMin,  '-X', size=15, zorder=1, clip_on=False,  color='k') #-X
        
        ###########################################################################
        ###RSA Contour Plot
        ###########################################################################
        #Set up figure
        fig2 = plt.figure(2)
        fig2.canvas.set_window_title('Virtual RSA: Absolute Height Contour') 
        # Set up a regular grid of interpolation points
        xi, yi = linspace(XMin, XMax, 100), linspace(YMin, YMax, 100)
        xi, yi = meshgrid(xi, yi)
        # Interpolate
        rbf = scipy.interpolate.Rbf(RSAArray[:,0], RSAArray[:,1], RSAArray[:,2], function='linear')
        zi = rbf(xi, yi)
        #Prepare contour
        plt.imshow(zi, vmin=ZMin, vmax=ZMax, origin='lower', extent=[XMin, XMax, YMin, YMax])
        #Suppress scientific notation in the color bar
        plt.colorbar(format ='%10.0f')
        
        #Show plots
        plt.show()
        
    def _reshape_3D_to_2D(self, numpyArray):
        '''
        Reshape a 3D numpy array of size (1,#,#) to (#,#)
        '''
        if numpyArray.shape[0] == 1:
            return numpyArray.reshape(numpyArray.shape[1:])
        
    def _subtractRaftData(self, datumPlaneEqn, raftFitEqn):
        '''
        Subtract Datum Plane Equation from Raft Plane Equation
        '''
        if datumPlaneEqn.get().strip() and raftFitEqn.get().strip():
            #Split string into array
            datumPlaneArray = findall(r"[-+]?\d*\.\d+|\d+", datumPlaneEqn.get())
            raftFitArray = findall(r"[-+]?\d*\.\d+|\d+", raftFitEqn.get())
            #Matrix subtraction (raft - datum plane)
            raft, datum = array(raftFitArray, dtype=float), array(datumPlaneArray, dtype=float) #convert to numpy array
            result = raft - datum
            #Return 1x3 array
            return result
        else:
            return [0,0,0]