'''
@title RSA_Metrology
@author: Rebecca Coles
Updated on Apr 4, 2017
Created on Apr 4, 2017

'''

# Import #######################################################################################
from tkinter import Tk
from RSAMetGUI import RSAMetGUI
################################################################################################

if __name__ == '__main__':
    root = Tk()
    RSAGUI = RSAMetGUI(root)
    root.mainloop()
