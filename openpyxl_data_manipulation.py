class Column:
    def __init__(self, name):
        self.name = name

    name = ""
    header_col = -1
    header_row = -1

    def __str__(self):
        return f"{self.name}({self.header_col}, {self.header_row})"


def get_cell_position(worksheet, val):
    for row in worksheet.iter_rows():
        for cell in row:
            if cell.value == val:
                return cell.column, cell.row
    return None, None


def get_column_positions(sheet, req_cols):
    for i, col in enumerate(req_cols):
        c, r = get_cell_position(sheet, col.name)  # vraca 7 5, (7=G) tkd G5

        req_cols[i].header_col = c
        req_cols[i].header_row = r


def has_columns(worksheet_name, columns):
    for col in columns:
        if col.header_col is None or col.header_row is None:
            print(f"Missing {col.name} column in sheet {worksheet_name}")
            return False
    return True


def are_col_headers_on_same_row(columns):
    row = columns[0].header_row
    for r in columns[1:]:
        if r.header_row != row:
            print("Required columns headings not aligned on the same row")
            return False
    return True
