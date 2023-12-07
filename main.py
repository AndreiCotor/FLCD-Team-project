from grammar import Grammar
from production_set import ProductionSet


def gramar_function_test():
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


if __name__ == '__main__':
    menu()
