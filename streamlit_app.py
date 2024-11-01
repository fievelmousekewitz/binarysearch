import streamlit as st
import math

def initialize_state():
    if 'low_value' not in st.session_state:
        st.session_state['low_value'] = 0
    if 'high_value' not in st.session_state:
        st.session_state['high_value'] = 100
    if 'correct' not in st.session_state:
        st.session_state['correct'] = 50
    if 'attempts' not in st.session_state:
        st.session_state['attempts'] = 0
    if 'max_attempts' not in st.session_state:
        st.session_state['max_attempts'] = 7
    if 'game_started' not in st.session_state:
        st.session_state['game_started'] = False

def start_game():
    st.session_state['low_value'] = int(st.session_state['low_value_input'])
    st.session_state['high_value'] = int(st.session_state['high_value_input'])
    st.session_state['correct'] = (st.session_state['low_value'] + st.session_state['high_value']) // 2
    st.session_state['attempts'] = 0
    st.session_state['max_attempts'] = math.ceil(math.log2(st.session_state['high_value'] - st.session_state['low_value'] + 1))
    st.session_state['game_started'] = True

def process_guess(response):
    guess = st.session_state['correct']
    if response == 'L':
        st.session_state['low_value'] = guess + 1
    elif response == 'H':
        st.session_state['high_value'] = guess - 1
    elif response == 'R':
        st.session_state['game_started'] = False

    st.session_state['correct'] = (st.session_state['low_value'] + st.session_state['high_value']) // 2
    st.session_state['attempts'] += 1

initialize_state()

st.sidebar.title("Game Setup")
st.session_state['low_value_input'] = st.sidebar.number_input("Low Value", min_value=0, value=0)
st.session_state['high_value_input'] = st.sidebar.number_input("High Value", min_value=0, value=100)

st.sidebar.button("Start Game", on_click=start_game)

st.title("Guessing Game")

if not st.session_state['game_started']:
    st.write("Please set up the game in the sidebar.")
else:
    st.write(f"Range: {st.session_state['low_value']} - {st.session_state['high_value']}")
    st.write(f"Attempts: {st.session_state['attempts']} / {st.session_state['max_attempts']}")
    st.write(f"Is your number {st.session_state['correct']}?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Higher", on_click=process_guess, args=('H',))
    with col2:
        st.button("Lower", on_click=process_guess, args=('L',))
    with col3:
        st.button("Restart", on_click=process_guess, args=('R',))
