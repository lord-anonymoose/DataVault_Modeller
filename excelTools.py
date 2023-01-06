# This file contains useful custom excel tools
import openpyxl
import os

def setWorksheet (file, sheet):
    wb = openpyxl.load_workbook(filename = file)
    return (wb[sheet])

# Unwrapping an optional array
def unwrapArray (optArray):
    array = []
    array = optArray
    return array
