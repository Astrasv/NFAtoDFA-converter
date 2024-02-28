def epsilon_closure(states, nfa_transitions):
    epsilon_closure_set = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        epsilon_transitions = nfa_transitions.get(state, {}).get('', set())
        for epsilon_state in epsilon_transitions:
            if epsilon_state not in epsilon_closure_set:
                epsilon_closure_set.add(epsilon_state)
                stack.append(epsilon_state)
    return frozenset(epsilon_closure_set)

def move(states, symbol, nfa_transitions):
    move_set = set()
    for state in states:
        move_set.update(nfa_transitions.get(state, {}).get(symbol, set()))
    return frozenset(move_set)

def nfa_to_dfa(nfa_states, alphabet, nfa_transitions, nfa_start_state, nfa_accept_states):
    dfa_states = set()
    dfa_transitions = {}
    dfa_start_state = epsilon_closure({nfa_start_state}, nfa_transitions)
    dfa_states.add(dfa_start_state)
    stack = [dfa_start_state]
    while stack:
        current_state = stack.pop()
        for symbol in alphabet:
            next_states = move(current_state, symbol, nfa_transitions)
            epsilon_closure_states = epsilon_closure(next_states, nfa_transitions)
            if epsilon_closure_states:
                dfa_transitions.setdefault(current_state, {})[symbol] = epsilon_closure_states
                if epsilon_closure_states not in dfa_states:
                    dfa_states.add(epsilon_closure_states)
                    stack.append(epsilon_closure_states)
    dfa_accept_states = {state for state in dfa_states if state.intersection(nfa_accept_states)}
    return dfa_states, dfa_transitions, dfa_start_state, dfa_accept_states

def display_transition_table(transition_table, alphabet):
    print("\nTransition Table (DFA):")
    print("State\t|\t", end="")
    for symbol in alphabet:
        print(symbol, end="\t|\t")
    print()
    print("--" * (6 + 8 * len(alphabet)))
    for state, transitions in transition_table.items():
        print(", ".join(sorted(state)), end="\t|\t")
        for symbol in alphabet:
            next_state = transitions.get(symbol, frozenset())
            print(", ".join(sorted(next_state)), end="\t|\t")
        print()

nfa_states = input("Enter states of NFA separated by comma: ").strip().split(',')
alphabet = input("Enter alphabet of NFA separated by comma: ").strip().split(',')
nfa_start_state = input("Enter start state of NFA: ").strip()
nfa_accept_states = input("Enter accept states of NFA separated by comma: ").strip().split(',')

nfa_transitions = {}
while True:
    transition = input("Enter transition (state, symbol, next_states) separated by comma (enter 'done' to finish): ").strip()
    if transition == "done":
        break
    state, symbol, next_states = map(str.strip, transition.split(','))
    nfa_transitions.setdefault(state, {}).setdefault(symbol, set()).update(next_states.split(','))

dfa_states, dfa_transitions, dfa_start_state, dfa_accept_states = nfa_to_dfa(nfa_states, alphabet, nfa_transitions, nfa_start_state, nfa_accept_states)
display_transition_table(dfa_transitions, alphabet)
