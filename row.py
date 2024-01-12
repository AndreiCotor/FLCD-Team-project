from state import StateType


class Row:
    def __init__(self, action, goto=None, reduction_index=None):
        self.action = action
        self.goto = goto
        self.reduction_index = reduction_index

    def __str__(self):
        if self.action == StateType.REDUCE:
            return f"REDUCE {self.reduction_index}"
        elif self.action == StateType.ACCEPT:
            return "ACCEPT"
        elif self.action == StateType.SHIFT:
            return f"SHIFT {self.goto}"
        else:
            raise Exception("No other states allowed")
