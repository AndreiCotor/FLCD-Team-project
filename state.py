class State:
    def __init__(self, items):
        self.items = items

    def get_symbols_succeeding_the_dot(self):
        symbols = set()
        for item in self.items:
            if item.dot_position < len(item.rhs):
                symbols.add(item.rhs[item.dot_position])
        return list(symbols)

    def __str__(self):
        result = ""
        for item in self.items:
            result += str(item) + "; "
        return result

    def __eq__(self, other):
        return self.items == other.items
