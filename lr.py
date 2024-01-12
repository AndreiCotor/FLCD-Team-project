from canonical_collection import CanonicalCollection
from item import Item
from parser_output import ParserOutput
from parsing_tree_row import ParsingTreeRow
from row import Row
from state import State, StateType
from table import Table


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


def get_parsing_table(grammar):
    canonical_coll = canonical_collection(grammar)
    table = Table({})

    for key, value in canonical_coll.adjacency_list.items():
        state = canonical_coll.states[key[0]]
        if key[0] not in table.table_rows:
            table.table_rows[key[0]] = Row(state.state_type, {}, None)
        table.table_rows[key[0]].goto[key[1]] = value

    ordered_productions = grammar.production_set.get_ordered_productions()
    for index, state in enumerate(canonical_coll.states):
        if state.state_type == StateType.REDUCE:
            item = next(iter(state.items))
            reduction_index = ordered_productions.index((item.lhs, item.rhs))
            table.table_rows[index] = Row(state.state_type, None, reduction_index)
        if state.state_type == StateType.ACCEPT:
            table.table_rows[index] = Row(state.state_type, None, None)

    return table


def parse(list_of_strings, grammar):
    working_stack = [("$", 0)]
    remaining_stack = list_of_strings.copy()
    parsing_table = get_parsing_table(grammar)

    parsing_tree = ParserOutput()
    tree_stack = []
    current_index = 0

    ordered_productions = grammar.production_set.get_ordered_productions()
    while remaining_stack or working_stack:
        table_row = parsing_table.table_rows.get(working_stack[-1][1])
        if table_row is None:
            raise Exception(f"Invalid state {working_stack[-1][1]} in the working stack")

        if table_row.action == StateType.SHIFT:
            if not remaining_stack:
                raise Exception("Action is shift but nothing else is left in the remaining stack")
            token = remaining_stack[0]
            value = table_row.goto.get(token)
            if value is None:
                raise Exception(f"Invalid symbol \"{token}\" for goto of state {working_stack[-1][1]}")

            working_stack.append((token, value))
            remaining_stack.pop(0)
            tree_stack.append((token, current_index))
            current_index += 1

        elif table_row.action == StateType.ACCEPT:
            last_element = tree_stack.pop()
            parsing_tree.add(ParsingTreeRow(last_element[1], last_element[0], -1, -1))
            return parsing_tree

        elif table_row.action == StateType.REDUCE:
            production_to_reduce_to = ordered_productions[table_row.reduction_index]
            parent_index = current_index
            current_index += 1
            last_index = -1

            for _ in range(len(production_to_reduce_to[1])):
                working_stack.pop()
                last_element = tree_stack.pop()
                parsing_tree.add(ParsingTreeRow(last_element[1], last_element[0], parent_index, last_index))
                last_index = last_element[1]

            tree_stack.append((production_to_reduce_to[0], parent_index))
            previous = working_stack[-1]
            next_state = parsing_table.table_rows[previous[1]].goto[production_to_reduce_to[0]]
            working_stack.append((production_to_reduce_to[0], next_state))

        else:
            raise Exception(str(table_row.action))

    raise Exception("No ACCEPT found before stacks got empty")
