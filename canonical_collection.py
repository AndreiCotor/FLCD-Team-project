class CanonicalCollection:
    def __init__(self):
        self.states = []
        self.adjacency_list = {}

    def add_state(self, state):
        self.states.append(state)

    def connect_states(self, index_first_state, symbol, index_second_state):
        self.adjacency_list[(index_first_state, symbol)] = index_second_state

    def __str__(self):
        result = ""
        for state in self.states:
            result += str(state) + "\n"
        return result + f"Adjacency: {self.adjacency_list}"
