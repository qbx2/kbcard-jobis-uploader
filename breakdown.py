from collections import OrderedDict

import xlrd

HEADER_ROW_INDEX = 6


def row_to_text(row):
    return [str(cell.value).replace('\n', '') for cell in row]


def get_breakdown(filename):
    book = xlrd.open_workbook(filename)

    for sheet in book.sheets():
        print(sheet.name)

        header = row_to_text(sheet.row(HEADER_ROW_INDEX))
        print(header)

        for row in [sheet.row(i) for i in range(HEADER_ROW_INDEX + 1, sheet.nrows)]:
            yield OrderedDict(
                (k, v)
                for k, v in zip(header, row_to_text(row))
                if k
            )
