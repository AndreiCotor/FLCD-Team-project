from canonical_collection import CanonicalCollection
from item import Item
from state import State


def get_non_terminal_after_dot(item, grammar):
    if 0 <= item.dot_position < len(item.rhs):
        term = item.rhs[item.dot_position]
        if term in grammar.non_terminals:
            return term
    return None


def closure(item, grammar):
    current_closure = set()
    current_closure.add(item)

    while True:
        new_closure = current_closure.copy()
        for it in current_closure:
            non_terminal = get_non_terminal_after_dot(it, grammar)
            if non_terminal is None:
                continue

            productions = grammar.production_set.get_production_for_non_terminal(non_terminal)
            for production in productions:
                current_item = Item(non_terminal, production, 0)
                new_closure.add(current_item)

        if len(current_closure) == len(new_closure):
            break

        current_closure = new_closure

    return State(current_closure)


def go_to(state, element, grammar):
    result = set()

    for item in state.items:
        if item.dot_position < len(item.rhs) and item.rhs[item.dot_position] == element:
            next_item = Item(item.lhs, item.rhs, item.dot_position + 1)
            result.update(closure(next_item, grammar).items)

    return State(result)


def canonical_collection(grammar):
    canonical_collection_obj = CanonicalCollection()

    if not grammar.is_enriched:
        enr_grammar = grammar.get_enriched_grammar()
    else:
        enr_grammar = grammar

    initial_item = Item(
        enr_grammar.starting_symbol,
        enr_grammar.production_set.get_production_for_non_terminal(enr_grammar.starting_symbol)[0],
        0
    )
    canonical_collection_obj.add_state(closure(initial_item, enr_grammar))

    i = 0
    while i < len(canonical_collection_obj.states):
        symbols = canonical_collection_obj.states[i].get_symbols_succeeding_the_dot()
        for symbol in symbols:
            new_state = go_to(canonical_collection_obj.states[i], symbol, enr_grammar)
            if new_state in canonical_collection_obj.states:
                index_in_states = canonical_collection_obj.states.index(new_state)
            else:
                canonical_collection_obj.add_state(new_state)
                index_in_states = len(canonical_collection_obj.states) - 1

            canonical_collection_obj.connect_states(i, symbol, index_in_states)
        i += 1

    return canonical_collection_obj

