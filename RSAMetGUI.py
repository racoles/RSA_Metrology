'''
@title RSAMetGUI
@author: Rebecca Coles
Updated on Apr 6, 2017
Created on Apr 4, 2017
'''

# Import #######################################################################################
from tkinter import Button, filedialog, PhotoImage, Label
from openpyxl import load_workbook
################################################################################################

class RSAMetGUI(object):
    '''
    GUI for RSA Metrology
    '''

    def __init__(self, master):
        '''
        Constructor
        '''
        self.master = master
        master.title("RSA Meterology")
        
        #Construct GUI
        #Sensor location buttons to open data files for each sensor
        #    S22    S12    S02
        #    S21    S11    S01    ^
        #    S20    S10    S00    |+Y
        #                         
        #                <--+X    Ø +Z
        
        #REB0
        S00 = Button(master, text="S00", width=10, command=lambda:self.loadInputDataFile(S00))
        S00.grid(row=2, column=2)

        S01 = Button(master, text="S01", width=10, command=self.loadInputDataFile)
        S01.grid(row=1, column=2)

        S02 = Button(master, text="S02", width=10, command=self.loadInputDataFile)
        S02.grid(row=0, column=2)
        
        #REB1
        S10 = Button(master, text="S10", width=10, command=self.loadInputDataFile)
        S10.grid(row=2, column=1)

        S11 = Button(master, text="S11", width=10, command=self.loadInputDataFile)
        S11.grid(row=1, column=1)

        S12 = Button(master, text="S12", width=10, command=self.loadInputDataFile)
        S12.grid(row=0, column=1)
        
        #REB2
        S20 = Button(master, text="S20", width=10, command=self.loadInputDataFile)
        S20.grid(row=2, column=0)

        S21 = Button(master, text="S21", width=10, command=self.loadInputDataFile)
        S21.grid(row=1, column=0)

        S22 = Button(master, text="S22", width=10, command=self.loadInputDataFile)
        S22.grid(row=0, column=0)
        
        #Add coordinate compass
        self.cordImage = PhotoImage(file="cord.pgm", width=100, height=79)
        cordLable = Label(image=self.cordImage)
        cordLable.grid(row=3, column=3)
        
        
    def loadInputDataFile(self, sensorButton):
        '''
        Load metrology data from input file using openpyxl library
        '''
        fileName = self.openFile()
        self.wb = load_workbook(fileName, read_only=True)
        self.ws = self.wb.get_sheet_by_name('Sheet1')
        pythonList = list(self.iter_rows(self.ws))
        print(pythonList)
        sensorButton.config(text = fileName)

        
    def openFile(self):
        '''
        Create open file dialogue box
        '''
        return filedialog.askopenfilename()
    
    def iter_rows(self, ws):
        '''
        itterate through xlsx list
        '''
        for row in self.ws.iter_rows(row_offset=1):
            yield [cell.value for cell in row]