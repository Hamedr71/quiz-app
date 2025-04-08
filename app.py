
import streamlit as st
import time
import uuid
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Quiz Game", layout="centered")

# Simulated session-based data
if "responses" not in st.session_state:
    st.session_state.responses = []
if "submitted_users" not in st.session_state:
    st.session_state.submitted_users = set()

# Timer settings
TIMER_MINUTES = 6
TIMER_SECONDS = TIMER_MINUTES * 60

# Unique ID for each session
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Quiz start
if "timer_start" not in st.session_state:
    st.title("Welcome to the Quiz Game!")
    if st.button("Start Quiz"):
        st.session_state.timer_start = time.time()
        st.success("Quiz has started! Timer is running.")
        st.stop()
    st.stop()

# Time remaining
def get_remaining_time():
    elapsed = int(time.time() - st.session_state.timer_start)
    return max(0, TIMER_SECONDS - elapsed)

remaining = get_remaining_time()

# Auto-refresh the app every 1 second (Streamlit Cloud safe)
st_autorefresh(interval=1000, limit=remaining, key="auto_refresh")

# Show live countdown
minutes = remaining // 60
seconds = remaining % 60
st.info(f"⏳ Time Remaining: {minutes:02d}:{seconds:02d}")

# If already submitted
if st.session_state.user_id in st.session_state.submitted_users:
    st.success("✅ You have already submitted. Thank you!")
    st.stop()

# Quiz data
correct_math = [2, 5, 19, 20, 3, 15]
correct_general = [False, False, True, False, True, False]

# Quiz form
with st.form("quiz_form"):
    st.header("Answer the following questions:")

    math_answers = []
    for i in range(1, 7):
        val = st.number_input(f"{i}. Your result:", key=f"math_{i}", step=1)
        math_answers.append(val)

    general_statements = [
        "Is Spanish the language with most native speakers?",
        "The Periodic table contains 125 elements.",
        "Always 4 ghosts chase Pac Man at the beginning of each game.",
        "Germany has won the most soccer World Cups.",
        "Hamburg has more than 2.5 Mio. inhabitants.",
        "There are 3 bones in an ear."
    ]
    general_answers = []
    for i, statement in enumerate(general_statements, 7):
        val = st.radio(f"{i}. {statement}", ["YES", "NO"], key=f"g_{i}")
        general_answers.append(val == "YES")

    estimated_correct = st.number_input("How many answers do you think you got correct (0-12)?", 0, 12, step=1)
    top_50 = st.radio("I think I did better than half the participants.", ["YES", "NO"]) == "YES"
    top_25 = st.radio("I think I did better than 75% of participants.", ["YES", "NO"]) == "YES"

    submitted = st.form_submit_button("Submit Now")

# Auto-submit if time expires
if remaining == 0 and st.session_state.user_id not in st.session_state.submitted_users:
    submitted = True

# Handle submission
if submitted and st.session_state.user_id not in st.session_state.submitted_users:
    actual_score = sum([a == b for a, b in zip(math_answers, correct_math)]) +                    sum([a == b for a, b in zip(general_answers, correct_general)])
    st.session_state.responses.append({
        "id": st.session_state.user_id,
        "score": actual_score,
        "estimate": estimated_correct,
        "top50": top_50,
        "top25": top_25
    })
    st.session_state.submitted_users.add(st.session_state.user_id)
    st.success(f"🎉 Your total score: {actual_score}/12")
    st.stop()

# Participation summary
st.subheader("👥 Participants Submitted:")
st.write(len(st.session_state.submitted_users))

# Final results
if remaining == 0:
    st.header("📊 All responses received — Results")
    st.write(st.session_state.responses)
