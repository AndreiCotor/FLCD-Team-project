import lr
from grammar import Grammar
from pif import read_pif
from production_set import ProductionSet
from lr import canonical_collection


def grammar_function_test():
    # Test grammar
    prod = ProductionSet({})
    prod.add_production(('A', 'AB'), ['BC', 'DE'])
    print(prod)


def menu():
    grammar = Grammar()
    while True:
        print("Choose option:")
        print("1. Read grammar")
        print("2. Check Context free grammar")
        print("3. Enrich grammar")
        print("4. Print grammar")
        print("5. Print productions for non-terminal")

        opt = input("Option: ")
        if opt == "1":
            file = input("File: ")
            grammar.read(file)
        if opt == "2":
            print(grammar.check_cfg())
        if opt == "3":
            grammar = grammar.get_enriched_grammar()
        if opt == "4":
            print("Non-terminals: ", grammar.non_terminals)
            print("Terminals: ", grammar.terminals)
            print("Starting symbol: ", grammar.starting_symbol)
            print("Productions: ", grammar.production_set)
        if opt == "5":
            non_term = input("Non-Terminal: ")
            print(grammar.get_productions_for_non_terminal(non_term))


def print_canonical_collection():
    grammar = Grammar()
    grammar.read('g1.in')
    print(canonical_collection(grammar))


def parsing():
    grammar = Grammar()
    grammar.read('g1.in')
    grammar_enr = grammar.get_enriched_grammar()
    parser_output = lr.parse(["a", "b", "b", "c", "d"], grammar_enr)
    parser_output.print_to_console()


if __name__ == '__main__':
    read_pif()
    parsing()
