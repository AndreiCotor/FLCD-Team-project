class State:
    def __init__(self, items):
        self.items = items
        if len(items) == 1:
            first_item = next(iter(items))
            if len(first_item.rhs) == first_item.dot_position:
                if first_item.lhs == "S0":
                    self.state_type = StateType.ACCEPT
                else:
                    self.state_type = StateType.REDUCE
            else:
                self.state_type = StateType.SHIFT
        elif len(items) > 1 and all(len(item.rhs) == item.dot_position for item in items):
            self.state_type = StateType.REDUCE_REDUCE_CONFLICT
        elif all(len(item.rhs) > item.dot_position for item in items):
            self.state_type = StateType.SHIFT
        else:
            self.state_type = StateType.SHIFT_REDUCE_CONFLICT

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


class StateType:
    REDUCE = 1
    ACCEPT = 2
    SHIFT = 3
    SHIFT_REDUCE_CONFLICT = 4
    REDUCE_REDUCE_CONFLICT = 5
