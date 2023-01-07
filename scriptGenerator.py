# This file contains python function for generating DDL-scripts based on Logical Data Model
import os
from excelTools import *

def scriptGenerator (pathLMD, pathSave):
    sheet = setWorksheet(pathLMD, 'Model')
    # Creating a list of unique table names
    tables = []
    unique_tables = []
    for row in sheet.iter_rows(min_row = 2, min_col = 1, max_col = 1):
        for cell in row:
            other_cell = sheet.cell(row = cell.row, column = 3)
            tables.append(cell.value + "." + other_cell.value)
    for i in tables:
        if i not in unique_tables:
            unique_tables.append(i)
    # Creating a dictionary for storing scripts
    scripts = {}
    for i in unique_tables:
        scripts[i] = "create table " + i + " ("
    # Filling in scripts dictionary
    for row in sheet.iter_rows(min_row = 2, min_col = 1, max_col = 1):
        for cell in row:
            table_schema = sheet.cell(row = cell.row, column = 1)
            table_name = sheet.cell(row = cell.row, column = 3)
            column = sheet.cell(row = cell.row, column = 5)
            data_type = sheet.cell(row = cell.row, column = 6)
            nullable = sheet.cell(row = cell.row, column = 7)
            scripts[table_schema.value + "." + table_name.value] += ("\n\t" + column.value + " " + data_type.value + " " + nullable.value + ",")
    # DDL-scripts output
    os.chdir(pathSave)
    with open('scripts.sql', 'w') as f:
        for table in scripts:
            f.write("\n")
            f.write("\n")
            for script in scripts[table]:
                f.write(f"{script}")
            f.write(");")
    f.close()
    f = open('scripts.sql', 'r')
    data = f.read()
    data = data.replace(",)", "\n)")
    f.close()
    f = open('scripts.sql', 'w')
    f.write(data)
    f.close()
