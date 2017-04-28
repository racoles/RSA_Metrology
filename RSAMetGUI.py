'''
@title RSAMetGUI
@author: Rebecca Coles
Updated on Apr 28, 2017
Created on Apr 4, 2017
'''

# Import #######################################################################################
from tkinter import Button, filedialog, PhotoImage, Label
from openpyxl import load_workbook
import ntpath
from RSA3DPlot import RSA3DPlot
################################################################################################

class RSAMetGUI(object):
    '''
    GUI for RSA Metrology
    '''
    #Initialize empty sensor data lists
    S00List = []
    S01List = []
    S02List = []
    S10List = []
    S11List = []
    S12List = []
    S20List = []
    S21List = []
    S22List = []

    def __init__(self, master):
        '''
        Constructor
        '''
        self.master = master
        master.title("RSA Meterology")
        
        #Construct GUI
        #Sensor location buttons to open data files for each sensor (CCS Coordinate system)
        #    S22    S12    S02
        #    S21    S11    S01    ^
        #    S20    S10    S00    |+Y
        #                         
        #                <--+X    Ø +Z
        
        #REB0
        S00 = Button(master, text="S00",bg = "white", command=lambda:self._loadInputDataFile(S00, RSAMetGUI.S00List)) #white
        S00.grid(row=2, column=2)
        
        S01 = Button(master, text="S01",bg = "purple", command=lambda:self._loadInputDataFile(S01, RSAMetGUI.S01List)) #purple
        S01.grid(row=1, column=2)

        S02 = Button(master, text="S02",bg = "yellow", command=lambda:self._loadInputDataFile(S02, RSAMetGUI.S02List)) #yellow
        S02.grid(row=0, column=2)
        
        #REB1
        S10 = Button(master, text="S10",bg = "cyan", command=lambda:self._loadInputDataFile(S10, RSAMetGUI.S10List)) #cyan
        S10.grid(row=2, column=1)

        S11 = Button(master, text="S11",bg = "blue", command=lambda:self._loadInputDataFile(S11, RSAMetGUI.S11List)) #blue
        S11.grid(row=1, column=1)

        S12 = Button(master, text="S12",bg = "orange", command=lambda:self._loadInputDataFile(S12, RSAMetGUI.S12List)) #orange
        S12.grid(row=0, column=1)
        
        #REB2
        S20 = Button(master, text="S20",bg = "magenta", command=lambda:self._loadInputDataFile(S20, RSAMetGUI.S20List)) #magenta
        S20.grid(row=2, column=0)

        S21 = Button(master, text="S21",bg = "green", command=lambda:self._loadInputDataFile(S21, RSAMetGUI.S21List)) #green
        S21.grid(row=1, column=0)

        S22 = Button(master, text="S22",bg = "red", command=lambda:self._loadInputDataFile(S22, RSAMetGUI.S22List)) #red
        S22.grid(row=0, column=0)
        
        #Add coordinate compass
        self.cordImage = PhotoImage(file="cord.pgm", width=100, height=79)
        cordLable = Label(image=self.cordImage)
        cordLable.grid(row=3, column=3)
        
        #Plot RSA for manually selected sensor positions
        manualPosition = Button(master, text = "Plot virtual RSA for manually selected sensor positions", 
                                command=lambda:RSA3DPlot().createVirtualRSA(RSAMetGUI.S00List, RSAMetGUI.S01List, RSAMetGUI.S02List, 
                                                                            RSAMetGUI.S10List, RSAMetGUI.S11List, RSAMetGUI.S12List, 
                                                                            RSAMetGUI.S20List, RSAMetGUI.S21List, RSAMetGUI.S22List, 0))
        manualPosition.grid(row=1, column=4)
        
        #Plot RSA for optimal sensor positions
        
        
    def _loadInputDataFile(self, sensorButton, sensorList):
        '''
        Load metrology data from input file using openpyxl library
        '''
        #open file
        fileName = self._openFile()
        #load workbook
        self.wb = load_workbook(fileName, read_only=True)
        #load Sheet1
        self.ws = self.wb.get_sheet_by_name('Sheet1')
        #create a python list of the data by iterating over all of the Sheet1 data
        sensorList.append(list(self._iter_rows(self.ws)))
        #update the button text to show the filename
        sensorButton.config(text = self._path_leaf(fileName))

        
    def _openFile(self):
        '''
        Create open file dialogue box
        '''
        return filedialog.askopenfilename()
    
    def _iter_rows(self, ws):
        '''
        iterate through xlsx list
        '''
        for row in self.ws.iter_rows(row_offset=1):
            yield [cell.value for cell in row]
            
    def _path_leaf(self, path):
        '''
        get filename from full path
        '''
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)