
import streamlit as st
import time
import uuid

st.set_page_config(page_title="Quiz Game", layout="centered")

# Simulated database (use cloud database in production)
if "responses" not in st.session_state:
    st.session_state.responses = []
if "submitted_users" not in st.session_state:
    st.session_state.submitted_users = set()

# Timer setup
TIMER_MINUTES = 6
TIMER_SECONDS = TIMER_MINUTES * 60

# Generate a unique session ID for each participant
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Timer initialization
if "timer_start" not in st.session_state:
    if st.button("Start Quiz"):
        st.session_state.timer_start = time.time()
        st.session_state.timer_start = time.time()
st.success("Quiz has started! Timer is running.")
    st.stop()

# Calculate remaining time
def get_remaining_time():
    elapsed = int(time.time() - st.session_state.timer_start)
    return max(0, TIMER_SECONDS - elapsed)

remaining = get_remaining_time()

# Show countdown timer
timer_placeholder = st.empty()
if remaining > 0:
    with timer_placeholder.container():
        minutes = remaining // 60
        seconds = remaining % 60
        st.info(f"⏳ Time Remaining: {minutes:02d}:{seconds:02d}")
        time.sleep(1)
        st.experimental_rerun()
else:
    st.success("⏰ Time is up! Auto-submitting your answers...")

# Prevent multiple submissions
if st.session_state.user_id in st.session_state.submitted_users:
    st.success("✅ You have already submitted. Thank you!")
    st.stop()

# Quiz questions
correct_math = [2, 5, 19, 20, 3, 15]
correct_general = [False, False, True, False, True, False]

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

# Auto-submit if time runs out
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

# Show participation info
st.subheader("👥 Participants Submitted:")
st.write(len(st.session_state.submitted_users))

# Display all results if quiz is over
if remaining == 0:
    st.header("📊 All responses received — Results")
    st.write(st.session_state.responses)
