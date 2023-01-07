# This file contains python functions for different Data Model checks
import re

def checkModelFile (sheetLDM):
    goalHeader = "table_schematable_typetable_nametable_descfield_namefield_typenull / not nullfield_descdistribution / partition"
    col1 = str(sheetLDM.cell(row = 1, column = 1).value)
    col2 = str(sheetLDM.cell(row = 1, column = 2).value)
    col3 = str(sheetLDM.cell(row = 1, column = 3).value)
    col4 = str(sheetLDM.cell(row = 1, column = 4).value)
    col5 = str(sheetLDM.cell(row = 1, column = 5).value)
    col6 = str(sheetLDM.cell(row = 1, column = 6).value)
    col7 = str(sheetLDM.cell(row = 1, column = 7).value)
    col8 = str(sheetLDM.cell(row = 1, column = 8).value)
    col9 = str(sheetLDM.cell(row = 1, column = 9).value)
    actualHeader = col1 + col2 + col3 + col4 + col5 + col6 + col7 + col8 + col9
    if (actualHeader == goalHeader):
        return ""
    else:
        return "Logical Data Model file does not follow structure guidelines"

def checkStandardFile (sheetStandard):
    goalHeader = "table_typefield_namefield_typenull / not null"
    col1 = str(sheetStandard.cell(row = 1, column = 1).value)
    col2 = str(sheetStandard.cell(row = 1, column = 2).value)
    col3 = str(sheetStandard.cell(row = 1, column = 3).value)
    col4 = str(sheetStandard.cell(row = 1, column = 4).value)
    actualHeader = col1 + col2 + col3 + col4
    if (actualHeader == goalHeader):
        return ""
    else:
        return "Modelling Standard file does not follow structure guidelines"

#To be updated
def checkColumnSymbols (sheet, column):
    def isValid (text):
        match = re.match("""^[a-zA-Z][a-z0-9 _"'.,]+$""", text)
        return bool(match)
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = column, max_col = column):
        for cell in row:
           if not isValid(cell.value):
               errors.append("Value '{}' does have invalid characters".format(cell.value))
    return errors

def checkUnknownStereotypes (sheet):
    stereotypes = ['HUB', 'SAT', 'LNK']
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = 2, max_col = 2):
        for cell in row:
            if cell.value not in stereotypes:
                errors.append("Unknown stereotype: '{}'".format(cell.value))
    return errors

def checkUnknownDataTypes (sheet):
    data_types = [
        'bigint',
        'bigserial',
        'boolean',
        'box',
        'char',
        'varchar',
        'cidr',
        'date',
        'cidr',
        'real',
        'polygon',
        'real',
        'serial',
        'smallint',
        'text',
        'timestamp',
        'uuid'
    ]
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = 6, max_col = 6):
        for cell in row:
            if cell.value not in data_types:
                errors.append("Unknown data type: '{}'".format(cell.value))
    return errors

def checkColumnDuplicates (sheet):
    errors = []
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
            errors.append("Duplicated field: '{}'".format(i))
    return errors

def checkNullables (sheet):
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = 7, max_col = 7):
        for cell in row:
            if cell.value not in ['null', 'not null']:
                errors.append("Invalid value in null / not null column: '{}'".format(cell.value))
    return errors

def checkEmptyTableDescriptions (sheet):
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = 4, max_col = 4):
        for cell in row:
            if not cell.value:
                errors.append("Empty table description (row {})".format(cell.row))
    return errors

def checkEmptyColumnDescriptions (sheet):
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = 8, max_col = 8):
        for cell in row:
            if not cell.value:
                errors.append("Empty table description (row {})".format(cell.row))
    return errors

def checkStandardFields (sheetLDM, sheetStandard):
    errors = []
    hubColumns = []
    satColumns = []
    lnkColumns = []
    for row in sheetStandard.iter_rows(min_row = 2, min_col = 1, max_col = 1):
        for cell in row:
            table_stereotype = sheetStandard.cell(row = cell.row, column = 1)
            field_name = sheetStandard.cell(row = cell.row, column = 2)
            field_type = sheetStandard.cell(row = cell.row, column = 3)
            nullable = sheetStandard.cell(row = cell.row, column = 4)
            col =  field_name.value + "." + field_type.value + "." + nullable.value
            if (table_stereotype.value == 'HUB'):
                hubColumns.append(col.lower())
            elif (table_stereotype.value == 'SAT'):
                satColumns.append(col.lower())
            elif (table_stereotype.value == 'LNK'):
                lnkColumns.append(col.lower())
    uniqueTables = []
    for row in sheetLDM.iter_rows(min_row = 2, min_col = 1, max_col = 1):
        for cell in row:
            tableName = sheetLDM.cell(row = cell.row, column = 3).value
            if tableName not in uniqueTables:
                uniqueTables.append(tableName)
    mandatoryColumns = []
    for table in uniqueTables:
        if table[:3].lower() == 'hub':
            for column in hubColumns:
                mandatoryColumns.append(table + "." + column)
        elif table[:3].lower() == 'sat':
            for column in satColumns:
                mandatoryColumns.append(table + "." + column)
        elif table[:3].lower() == 'sat':
            for column in lnkColumns:
                mandatoryColumns.append(table + "." + column)
        else:
            errors.append("Invalid prefix in table '" + table + "'")
    allColumns = []
    for row in sheetLDM.iter_rows(min_row = 2, min_col = 1, max_col = 1):
        for cell in row:
            table_name = sheetLDM.cell(row = cell.row, column = 3)
            field_name = sheetLDM.cell(row = cell.row, column = 5)
            field_type = sheetLDM.cell(row = cell.row, column = 6)
            nullable = sheetLDM.cell(row = cell.row, column = 7)
            col = str(table_name.value) + "." + str(field_name.value) + "." + str(field_type.value) + "." + str(nullable.value)
            allColumns.append (col)
    for mandatoryColumn in mandatoryColumns:
        if mandatoryColumn not in allColumns:
            errors.append("The following mandatory column is missed or does have invalid parameters: " + mandatoryColumn)
    return errors
