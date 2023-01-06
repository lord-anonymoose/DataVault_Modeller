# This file contains python functions for different Data Model checks

def checkColumnSymbols (sheet, column):
    def match (text, alphabet=set('abcdefghijklmnopqrstuvwxyz_0123456789')):
        return not alphabet.isdisjoint(text.lower())
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = column, max_col = column):
        for cell in row:
           if not match(cell.value):
               errors.append("Value {} does have invalid characters".format(cell.value))
    return errors

def checkUnknownStereotypes (sheet):
    stereotypes = ['HUB', 'SAT', 'LNK']
    errors = []
    for row in sheet.iter_rows(min_row = 2, min_col = 2, max_col = 2):
        for cell in row:
            if cell.value not in stereotypes:
                errors.append("Stereotype {} is invalid".format(cell.value))
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
                errors.append("Unknown data type: {}".format(cell.value))
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
            errors.append("Duplicated field: {}".format(i))
