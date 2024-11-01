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

    if 'prev_low' not in st.session_state:
        st.session_state['prev_low'] = 0
    if 'prev_high' not in st.session_state:
        st.session_state['prev_high'] = 0

def start_game():
    st.session_state['low_value'] = int(st.session_state['low_value_input'])
    st.session_state['high_value'] = int(st.session_state['high_value_input'])
    st.session_state['correct'] = (st.session_state['low_value'] + st.session_state['high_value']) // 2
    st.session_state['attempts'] = 0
    st.session_state['max_attempts'] = math.ceil(math.log2(st.session_state['high_value'] - st.session_state['low_value'] + 1))
    st.session_state['latexattempts'] = r'\text{{max\_attempts}} = \lceil \log_2(\text{{high\_value}} - \text{{low\_value}} + 1) \rceil'

    st.session_state['prev_high'] = st.session_state['high_value']
    st.session_state['prev_low'] = st.session_state['low_value']

    st.session_state['game_started'] = True

def process_guess(response):
    guess = st.session_state['correct']
    if response == 'L':
        st.session_state['prev_low'] = st.session_state['low_value']
        st.session_state['prev_high'] = st.session_state['high_value']
        st.session_state['low_value'] = guess + 1

    elif response == 'H':
        st.session_state['prev_high'] = st.session_state['high_value']
        st.session_state['prev_low'] = st.session_state['low_value']
        st.session_state['high_value'] = guess - 1

    elif response == 'R':
        st.session_state['game_started'] = False

    st.session_state['correct'] = (st.session_state['low_value'] + st.session_state['high_value']) // 2
    st.session_state['attempts'] += 1

initialize_state()

st.sidebar.title("Search Setup")
st.session_state['low_value_input'] = st.sidebar.number_input("Low Value", min_value=0, value=0)
st.session_state['high_value_input'] = st.sidebar.number_input("High Value", min_value=0, value=100)


st.sidebar.button("Start Game", on_click=start_game)

st.title("Binary Number Search")
st.caption("by jeffix")

if not st.session_state['game_started']:
    st.write("Please setup values in the left sidebar.")
else:
    #st.write(f"Range: {st.session_state['low_value']} - {st.session_state['high_value']}")

    col1, col2 = st.columns(2)
    lowdelta = st.session_state['low_value'] - st.session_state['prev_low']
    if lowdelta == 0:
        lowdelta = None
    highdelta = st.session_state['high_value'] - st.session_state['prev_high']
    if highdelta == 0:
        highdelta = None
    col1.metric("Low Value", st.session_state['low_value'], lowdelta)
    col2.metric("High Value", st.session_state['high_value'], highdelta)


    st.write(f"Attempts: {st.session_state['attempts']} / {st.session_state['max_attempts']}")
    #st.latex(st.session_state['latexattempts'])
    #st.markdown(f"Next Guess: :blue[{st.session_state['correct']}]")

    st.metric("Next Attempt:", st.session_state['correct'],"")

    st.button("This number was :red[Higher] than the correct number", on_click=process_guess, args=('H',))
    st.button("This number was :red[Lower] than the correct number", on_click=process_guess, args=('L',))
    st.button("Reset", on_click=process_guess, args=('R',))
