import streamlit as st
import requests

API_URL = 'https://opentdb.com/api.php'

def get_trivia_questions(category, difficulty, num_questions):
    params = {
        'amount': num_questions,
        'category': category,
        'difficulty': difficulty,
        'type': 'multiple'
    }
    response = requests.get(API_URL, params=params)
    return response.json().get('results', [])

st.title('Trivia Quiz Application')

# Sidebar for settings
st.sidebar.header('Settings')
category = st.sidebar.selectbox('Category', [
    'General Knowledge', 'Books', 'Film', 'Music', 'Musicals & Theatres', 
    'Television', 'Video Games', 'Board Games', 'Science & Nature', 
    'Computers', 'Mathematics', 'Mythology', 'Sports', 'Geography', 
    'History', 'Politics', 'Art', 'Celebrities', 'Animals', 
    'Vehicles', 'Comics', 'Gadgets', 'Anime & Manga', 'Cartoon & Animations'
], index=0)
difficulty = st.sidebar.radio('Difficulty', ['easy', 'medium', 'hard'], index=0)
num_questions = st.sidebar.slider('Number of Questions', 1, 10, 5)

# Mapping category names to their corresponding IDs
category_map = {
    'General Knowledge': 9,
    'Books': 10,
    'Film': 11,
    'Music': 12,
    'Musicals & Theatres': 13,
    'Television': 14,
    'Video Games': 15,
    'Board Games': 16,
    'Science & Nature': 17,
    'Computers': 18,
    'Mathematics': 19,
    'Mythology': 20,
    'Sports': 21,
    'Geography': 22,
    'History': 23,
    'Politics': 24,
    'Art': 25,
    'Celebrities': 26,
    'Animals': 27,
    'Vehicles': 28,
    'Comics': 29,
    'Gadgets': 30,
    'Anime & Manga': 31,
    'Cartoon & Animations': 32
}
category_id = category_map[category]

# Initialize session state variables
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def start_quiz():
    st.session_state.questions = get_trivia_questions(category_id, difficulty, num_questions)
    st.session_state.user_answers = [None] * num_questions
    st.session_state.submitted = False

def submit_quiz():
    st.session_state.submitted = True

# Button to start quiz
if not st.session_state.submitted:
    st.button('Start Quiz', on_click=start_quiz)

# Display quiz questions and form
if st.session_state.questions and not st.session_state.submitted:
    with st.form(key='quiz_form'):
        for i, question in enumerate(st.session_state.questions):
            st.write(f"**Q{i+1}:** {question['question']}")
            options = question['incorrect_answers'] + [question['correct_answer']]
            options = sorted(options)
            st.session_state.user_answers[i] = st.radio(f'Options for Q{i+1}', options, key=f'question_{i}')
        submit_button = st.form_submit_button('Submit Answers', on_click=submit_quiz)

# Display score after submission
if st.session_state.submitted:
    score = sum(1 for i, question in enumerate(st.session_state.questions) if st.session_state.user_answers[i] == question['correct_answer'])
    st.write(f'## Your Score: {score}/{num_questions}')

