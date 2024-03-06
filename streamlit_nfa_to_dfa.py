import streamlit as st
import pandas as pd

def set_theme():
    st.markdown(
        """
        <style>
            body {
                color: white;
                background-color: #202124; /* Dark gray background */
            }
            .stButton>button {
                color: white;
                background-color: #1976D2; /* Blue button */
                transition: 200ms ease;
            }
            .stButton>button:hover {
                color:white                
                background-color: #2976D2; /* Blue button */
                box-shadow: 0 0 30px 5px #0ef;

                
            }
            .css-1aumxhk {
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

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
        # Handling empty string transitions
        epsilon_states = epsilon_closure(current_state, nfa_transitions)
        if epsilon_states:
            dfa_transitions.setdefault(current_state, {}).setdefault('λ', set()).update(epsilon_states)
            if epsilon_states not in dfa_states:
                dfa_states.add(epsilon_states)
                stack.append(epsilon_states)
    dfa_accept_states = {state for state in dfa_states if state.intersection(nfa_accept_states)}
    return dfa_states, dfa_transitions, dfa_start_state, dfa_accept_states


def display_transition_table(transition_table, alphabet):
    st.subheader("DFA Transition table")
    df = pd.DataFrame(columns=['State'] + alphabet)  
    for state, transitions in transition_table.items():
        row = [", ".join(sorted(state))]
        for symbol in alphabet:
            next_state = transitions.get(symbol, frozenset())
            if next_state:
                row.append(", ".join(sorted(next_state)))
            else:
                row.append("φ")  
        df.loc[len(df)] = row
    st.dataframe(df, width=800)



def about_page():
    st.write("# About")
    st.write("This Streamlit application converts a Non-Deterministic Finite Automaton (NFA) into a Deterministic Finite Automaton (DFA) using the provided transition table.")
    st.button("[Go to Conversion Page](?page=conversion_page)")
    st.write("## How it Works")
    st.write("1. **Input**: Enter the states, alphabet, start state, and accept states of the NFA. Provide the NFA transition table by specifying each transition in the format `state, symbol, next_states`.")
    st.write("2. **Conversion**: Click the 'Convert to DFA' button. The application converts the NFA transition table into a DFA transition table.")
    st.write("3. **Output**: The resulting DFA transition table is displayed, showing the transitions for each state and symbol.")
    st.write("## Meet the Team")
    team_data = {
        "Name": ["Sudharsan Vanamali", "Ritesh Koushik", "Guda Sravanthi ","M.Nishanth Sai","Chennuru Sri Lahari "],
        "Role": ["CB.EN.U4CSE22049", "CB.EN.U4CSE22038", "CB.EN.U4CSE22014","CB.EN.U4CSE22028","CB.EN.U4CSE22008"]
    }
    team_df = pd.DataFrame(team_data)
    team_df_display = team_df.copy()  
    team_df_display.index = team_df_display.index+1
    st.dataframe(team_df_display,width=800)  

def conversion_page():
    set_theme()
    st.title("NFA to DFA Converter")

    st.subheader("Enter NFA Transition Table:")
    nfa_states_input = st.text_input("States (comma-separated)", "")
    alphabet_input = st.text_input("Alphabet (comma-separated)", "")
    nfa_start_state_input = st.text_input("Start State", "")
    nfa_accept_states_input = st.text_input("Accept States (comma-separated)", "")
    nfa_transitions_input = st.text_area("Transitions (state, symbol, next_states) - Use space for lambda transition", "")

    if st.button("Convert to DFA"):
        nfa_states = nfa_states_input.strip().split(',')
        alphabet = alphabet_input.strip().split(',')
        nfa_start_state = nfa_start_state_input.strip()
        nfa_accept_states = nfa_accept_states_input.strip().split(',')

        nfa_transitions = {}
        for transition in nfa_transitions_input.strip().split('\n'):
            state, symbol, next_states = map(str.strip, transition.split(','))
            nfa_transitions.setdefault(state, {}).setdefault(symbol, set()).update(next_states.split(','))

        dfa_states, dfa_transitions, dfa_start_state, dfa_accept_states = nfa_to_dfa(nfa_states, alphabet, nfa_transitions, nfa_start_state, nfa_accept_states)
        transition_table = display_transition_table(dfa_transitions, alphabet)



def main():
    set_theme()

    pages = {
        "About": about_page,
        "Conversion":conversion_page
    }

    selection = st.sidebar.radio("Navigate to", list(pages.keys()), index=1)
    pages[selection]()

if __name__ == "__main__":
    main()

