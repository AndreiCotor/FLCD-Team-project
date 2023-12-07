class ProductionSet:
    def __init__(self, productions):
        # productions = {} is a hashmap
        self.productions = productions

    def get_productions_of(self, lhs):
        return self.productions.get(lhs, [])

    def get_all_productions(self):
        return self.productions

    def add_production(self, lhs, rhs):
        # lhs tuple because is imutable and hashable and rhs list of states
        if lhs not in self.productions:
            self.productions[lhs] = []

        self.productions[lhs].append(rhs)

    def copy(self):
        new_productions = {}
        for lhs, rhs in self.productions.items():
            new_productions[lhs] = rhs.copy()

        return ProductionSet(new_productions)

    def __str__(self):
        return str(self.productions)

    def get_ordered_productions(self):
        production_list = []
        for lhs in self.productions.keys():
            for rhs in self.productions[lhs]:
                production_list.append((lhs[0], rhs))

        return production_list


# S -> AB
# A -> Aaa | bbb
# A and S keys productions[A] = [Aaa, bbb]