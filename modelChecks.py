# This file contains python functions for different Data Model checks

#To be updated
def checkModelFile (sheetLDM):
    errorMessage = ""
    return errorMessage

#To be updated
def checkStandardFile (sheetStandard):
    errorMessage = ""
    return errorMessage

#To be updated
def checkColumnSymbols (sheet, column):
    def match (text, alphabet=set('abcdefghijklmnopqrstuvwxyz_0123456789')):
        return not alphabet.isdisjoint(text.lower())
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = column, max_col = column):
        for cell in row:
           if not match(cell.value):
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
