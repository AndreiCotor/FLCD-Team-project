class ParsingTreeRow:
    def __init__(self, index, info, parent, right_sibling):
        self.index = index
        self.info = info
        self.parent = parent
        self.right_sibling = right_sibling
