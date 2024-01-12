class Table:
    def __init__(self, table_rows):
        self.table_rows = table_rows

    def __str__(self):
        string = ""
        for row_index, row in sorted(self.table_rows.items()):
            string += f"{row_index}: {row}\n"
        return string
