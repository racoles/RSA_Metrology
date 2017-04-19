'''
@title RSA3DPlot
@author: Rebecca Coles
Updated on Apr 19, 2017
Created on Apr 14, 2017
'''

# Import #######################################################################################
from numpy import array
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
        
    def coordTransform(self):
        '''
        Perform coordinate transform from PCS coordinate system to CCS coordinate system (180 degree rotation).
        '''
    
    def createVirtualRSA(self):
        '''
        Align data based on the sensor positions on the RSA.
        '''