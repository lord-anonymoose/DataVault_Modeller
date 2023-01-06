#This file contains basic back-end logic for the app

import sys
import os
#import openpyxl
import modelChecks
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot
from modelChecks import *
from scriptGenerator import *
from excelTools import *

class MainBackend(QObject):
    path1 = Signal(str, arguments=['write'])

    def __init__(self):
        QObject.__init__(self)

    # Logical Data Model Check
    @Slot('QString', 'QString', 'QString')
    def checkModel(self, pathLMD, pathStandard, pathSave):
        # Setting Logical Data Model worksheet
        sheet = setWorksheet(pathLMD, 'Model')
        errors = []
        goodStructure = True

        # Check table_schema for incorrect symbols
        errors.append(checkColumnSymbols(sheet,1))

        # Check table_name for incorrect symbols
        errors.append(checkColumnSymbols(sheet,3))

        # Check column_name for incorrect symbols
        errors.append(checkColumnSymbols(sheet,5))

        # Check for unknown stereotypes
        errors.append(checkUnknownStereotypes(sheet))

        # Check for unknown data types
        errors.append(checkUnknownDataTypes(sheet))

        # Check for fields duplicates
        errors.append(checkColumnDuplicates(sheet))

        # Full structure check
        #goodStructure = checkColumn(1, "table_schema") and checkColumn(2, "table_type") and checkColumn(3, "table_name") and checkColumn(4, "table_desc") and checkColumn(5, "field_name") and checkColumn(6, "field_type") and checkColumn(7, "null / not null") and checkColumn(8, "field_desc") and checkColumn(9, "distribution / partition")


        # Check for empty table descriptions
        for row in sheet.iter_rows(min_row = 2, min_col = 4, max_col = 4):
            for cell in row:
                if not cell.value:
                    errors.append("Встречаются незаполненные описания таблиц")


        # Check for unknown values in "null / not null" column
        for row in sheet.iter_rows(min_row = 2, min_col = 7, max_col = 7):
            for cell in row:
                if cell.value not in ['null', 'not null']:
                    errors.append("Некорректное значение в столбце null / not null: {}".format(cell.value))

        # Check for empty column descriptions
        for row in sheet.iter_rows(min_row = 2, min_col = 8, max_col = 8):
            for cell in row:
                if not cell.value:
                    errors.append("Встречаются незаполненные описания столбцов")



        # Mandatory fields check
        wb = openpyxl.load_workbook(filename = pathStandard)
        sheet = wb['Standards']

        # Fetching mandatory columns for Data Vault stereotypes
        hubColumns = []
        satColumns = []
        lnkColumns = []
        for row in sheet.iter_rows(min_row = 2, min_col = 1, max_col = 1):
            for cell in row:
                table_stereotype = sheet.cell(row = cell.row, column = 1)
                print(table_stereotype)
                field_name = sheet.cell(row = cell.row, column = 2)
                field_type = sheet.cell(row = cell.row, column = 3)
                nullable = sheet.cell(row = cell.row, column = 4)
                #new_col = field_name.value + "." + field_type.value + "." + nullable.value
                new_col = field_name.value
                print(new_col)
                if (table_stereotype == 'HUB'):
                    hubColumns.append(new_col)
                elif (table_stereotype == 'SAT'):
                    satColumns.append(new_col)
                elif (table_stereotype == 'LNK'):
                    lnkColumns.append(new_col)

        # Fetching unique tables from Data Model
        unique_tables = []
        for row in sheet.iter_rows(min_row = 2, min_col = 1, max_col = 1):
            for cell in row:
                tableName = sheet.cell(row = cell.row, column = 3)
                if tableName not in unique_tables:
                    unique_tables.append(tableName)

        #mandatoryColumns = [

        # Error report output
        os.chdir(pathSave)
        with open('error_report.txt', 'w') as f:
            if goodStructure:
                for error in errors:
                    f.write(f"{error}\n")
                if not errors:
                    f.write("Модель успешно прошла проверки")
            else:
                f.write("Некорректная структура файла модели")




    # DDL-structures Generator
    @Slot('QString', 'QString')
    def generateDatabase(self, pathLMD, pathSave):
        scriptGenerator(pathLMD, pathSave)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = MainBackend()
    engine.rootContext().setContextProperty("backend", backend)
    engine.load("main.qml")
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
