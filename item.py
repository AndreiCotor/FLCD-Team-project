class Item:
    def __init__(self, lhs, rhs, dot_position):
        self.lhs = lhs
        self.rhs = rhs
        self.dot_position = dot_position

    def __str__(self):
        rhs1 = ''.join(self.rhs[:self.dot_position])
        rhs2 = ''.join(self.rhs[self.dot_position:])
        return f"{self.lhs} -> {rhs1}.{rhs2}"

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs and self.dot_position == other.dot_position

    def __hash__(self):
        return hash((self.lhs, str(self.rhs), self.dot_position))
