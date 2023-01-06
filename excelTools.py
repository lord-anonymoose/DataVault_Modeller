# This file contains useful custom excel tools
import openpyxl

def setWorksheet (file, sheet):
    wb = openpyxl.load_workbook(filename = file)
    return (wb[sheet])
