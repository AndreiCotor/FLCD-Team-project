class ParserOutput:
    def __init__(self):
        self.tree_rows = []

    def add(self, parsing_tree_row):
        self.tree_rows.append(parsing_tree_row)

    def print_to_console(self):
        print(str(self))

    def print_to_file(self, file):
        with open(file, "w") as file:
            file.write(str(self))

    def __str__(self):
        sorted_tree_rows = sorted(self.tree_rows, key=lambda x: x.index)
        res = ""
        for row in sorted_tree_rows:
            res += f"{row.index}: {row.info}, {row.parent}, {row.right_sibling}\n"

        return res
