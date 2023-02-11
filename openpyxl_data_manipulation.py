
def get_cell_position(worksheet, val):
    for row in worksheet.iter_rows():
        for cell in row:
            if cell.value == val:
                return cell.column, cell.row
