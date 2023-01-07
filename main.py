#This file contains basic back-end logic for the app

import sys
import os
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
    def checkModel(self, pathLDM, pathStandard, pathSave):
        structureError = ""
        errors = []

        # Setting Modelling Standards worksheet
        sheet = setWorksheet(pathStandard, 'Standards')

        # Checking Modelling Standards file structure
        structureError += checkStandardFile(sheet)

        # Setting Logical Data Model worksheet
        sheet = setWorksheet(pathLDM, 'Model')

        # Checking LDM file structure
        structureError += checkModelFile(sheet)

        if (structureError == ""):
        # Check table_schema for incorrect symbols
            errors += unwrapArray(checkColumnSymbols(sheet,1))

            # Check table_name for incorrect symbols
            errors += unwrapArray(checkColumnSymbols(sheet,3))

            # Check column_name for incorrect symbols
            errors += unwrapArray(checkColumnSymbols(sheet,5))

            # Check for unknown stereotypes
            errors += unwrapArray(checkUnknownStereotypes(sheet))

            # Check for unknown data types
            errors += unwrapArray(checkUnknownDataTypes(sheet))

            # Check for fields duplicates
            errors += unwrapArray(checkColumnDuplicates(sheet))

            # Check for empty table descriptions
            errors += unwrapArray(checkEmptyTableDescriptions(sheet))

            # Check for empty column descriptions
            errors += unwrapArray(checkEmptyTableDescriptions(sheet))

            # Check for technical fields according to modelling Standards
            errors += unwrapArray(checkStandardFields(setWorksheet(pathLDM, 'Model'), setWorksheet(pathStandard, 'Standards')))

        # Error report output
        os.chdir(pathSave)
        with open('error_report.txt', 'w') as f:
            if (structureError == ""):
                for error in errors:
                    f.write(f"{error}\n")
                if not errors:
                    f.write("Модель успешно прошла проверки")
            else:
                f.write(structureError)

    # DDL-structures Generator
    @Slot('QString', 'QString')
    def generateDatabase(self, pathLDM, pathSave):
        scriptGenerator(pathLDM, pathSave)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = MainBackend()
    engine.rootContext().setContextProperty("backend", backend)
    engine.load("main.qml")
    engine.quit.connect(app.quit)
    sys.exit(app.exec())
