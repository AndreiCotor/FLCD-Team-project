from production_set import ProductionSet

class Grammar:
    ENRICHED_GRAMMAR_STARTING_SYMBOL = "S0"

    def __init__(self):
        self.is_enriched = None
        self.non_terminals = None
        self.terminals = None
        self.starting_symbol = None
        self.production_set = None

    def from_values(self, non_terminals, terminals, starting_symbol, production_set):
        # non_term is a list of strings, terminals list of string
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.starting_symbol = starting_symbol
        self.production_set = production_set
        self.is_enriched = True

    def read(self, filename: str):
        with open(filename, "r") as f:
            lines = f.readlines()

            self.non_terminals = lines[0].strip().split(" ")
            self.terminals = lines[1].strip().split(" ")
            self.starting_symbol = lines[2].strip()

            self.production_set = ProductionSet({})
            for i in range(3, len(lines)):
                splited_list = lines[i].strip().split("->")
                lhs = tuple(splited_list[0].strip().split(" "))
                rhs = splited_list[1].strip().split(" ")
                self.production_set.add_production(lhs, rhs)

        self.is_enriched = False

    def check_cfg(self):
        ok = True
        for production in self.production_set.get_all_productions().keys():
            if len(production) > 1 and production[0] not in self.non_terminals:
                ok = False

        return ok

    def get_enriched_grammar(self):
        if self.is_enriched:
            raise Exception("Grammar already enriched!")

        enriched_production_set = self.production_set.copy()

        enriched_grammar = Grammar()
        enriched_grammar.from_values(self.non_terminals, self.terminals, self.ENRICHED_GRAMMAR_STARTING_SYMBOL, enriched_production_set)
        enriched_grammar.non_terminals.append(self.ENRICHED_GRAMMAR_STARTING_SYMBOL)
        enriched_grammar.production_set.add_production((self.ENRICHED_GRAMMAR_STARTING_SYMBOL, ), [self.starting_symbol])

        return enriched_grammar

# {('S',): ['a', 'A'], ('A',): ['b', 'A', 'c']}
#{('S',): [['a', 'A']], ('A',): [['b', 'A'], ['c']]}