import streamlit as st
import math

# Initialize session state variables if they don't exist
if 'low_value' not in st.session_state:
    st.session_state['low_value'] = None
if 'high_value' not in st.session_state:
    st.session_state['high_value'] = None
if 'correct' not in st.session_state:
    st.session_state['correct'] = None
if 'attempts' not in st.session_state:
    st.session_state['attempts'] = 0
if 'max_attempts' not in st.session_state:
    st.session_state['max_attempts'] = 0
if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False

# Function to start a new game
def start_game():
    low_value = st.session_state['low_value_input']
    high_value = st.session_state['high_value_input']

    st.session_state['low_value'] = low_value
    st.session_state['high_value'] = high_value
    st.session_state['correct'] = (low_value + high_value) // 2
    st.session_state['attempts'] = 0
    st.session_state['max_attempts'] = math.ceil(math.log2(high_value - low_value + 1))
    st.session_state['game_started'] = True

# Function to process user's response
def process_guess(response):
    # Debug
    print('Response: ' + response)
    print('LowValue: ' + str(st.session_state['low_value']))
    print('HighValue: ' + str(st.session_state['high_value']))
    print('Correct: ' + str(st.session_state['correct']))

    guess = (st.session_state['low_value'] + st.session_state['high_value']) // 2
    st.session_state['attempts'] += 1

    if response == 'L':
        st.session_state['low_value'] = guess + 1
    if response == 'H':
        st.session_state['high_value'] = guess - 1
    if response == 'R':
        st.session_state['game_started'] = False  # End the game by setting game_started to False

    st.session_state['correct'] = (st.session_state['low_value'] + st.session_state['high_value']) // 2

# Sidebar input for initial values
st.sidebar.title("Game Setup")
st.sidebar.subheader("Enter the range for the guessing game")

low_value_input = st.sidebar.number_input("Low Value", min_value=0, value=0)
high_value_input = st.sidebar.number_input("High Value", min_value=0, value=100)

if st.sidebar.button("Start Game"):
    st.session_state['low_value_input'] = int(low_value_input)
    st.session_state['high_value_input'] = int(high_value_input)
    start_game()

# Main Game Interface
st.title("Guessing Game")

if not st.session_state['game_started']:
    st.write("Please set up the game in the sidebar.")
if st.session_state['game_started']:
    st.write(f"Attempts: {st.session_state['attempts']} / {st.session_state['max_attempts']}")
    st.write(f"Is your number {st.session_state['correct']}?")

    if st.button("Lower"):
        process_guess('H')
    if st.button("Higher"):
        process_guess('L')
    if st.button("Correct"):
        st.write("Game over! Restart the game from the sidebar.")
        st.session_state['game_started'] = False
        
