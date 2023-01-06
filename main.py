import sys
import os
import openpyxl
#import modelChecks.py
import modelChecks
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot
from modelChecks import *
class MainBackend(QObject):
    path1 = Signal(str, arguments=['write'])

    def __init__(self):
        QObject.__init__(self)

    # Logical Data Model Check
    @Slot('QString', 'QString', 'QString')
    def checkModel(self, pathLMD, pathStandard, pathSave):
        # Uploading Logical Data Model Check
        wb = openpyxl.load_workbook(filename = pathLMD)
        sheet = wb['Model']
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

        # Check for column duplicates
        columns = []
        unique_columns = []
        for row in sheet.iter_rows(min_row = 2, min_col = 3, max_col = 3):
            for cell in row:
                other_cell = sheet.cell(row = cell.row, column = 5)
                columns.append(cell.value + "." + other_cell.value)
        for i in columns:
            if i not in unique_columns:
                unique_columns.append(i)
            else:
                errors.append("Дублируется поле: {}".format(i))

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
        ## Подгружается файл с моделью
        wb = openpyxl.load_workbook(filename = pathLMD)
        sheet = wb['Model']
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
        with open('scripts.txt', 'w') as f:
            for table in scripts:
                f.write("\n")
                f.write("\n")
                for script in scripts[table]:
                    f.write(f"{script}")
                f.write(");")
        f.close()
        f = open('scripts.txt', 'r')
        data = f.read()
        data = data.replace(",)", "\n)")
        f.close()
        f = open('scripts.txt', 'w')
        f.write(data)
        f.close()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = MainBackend()
    engine.rootContext().setContextProperty("backend", backend)
    engine.load("main.qml")
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
