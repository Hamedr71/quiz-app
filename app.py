
import streamlit as st
import uuid
import numpy as np
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Quiz Game", layout="centered")

# Refresh the page every 10 seconds to update performance data
st_autorefresh(interval=10000, key="refresh")

# Initialize session memory
if "responses" not in st.session_state:
    st.session_state.responses = []
if "submitted_users" not in st.session_state:
    st.session_state.submitted_users = set()
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Show result if already submitted
if st.session_state.user_id in st.session_state.submitted_users:
    st.success("✅ You have submitted. Here's your live-updating result:")

    # Fetch own response
    my_response = [r for r in st.session_state.responses if r["id"] == st.session_state.user_id][0]
    my_score = my_response["score"]
    estimate = my_response["estimate"]
    top_50_self = my_response["top50"]
    top_25_self = my_response["top25"]

    # All scores
    scores = [r["score"] for r in st.session_state.responses]
    median_score = np.median(scores)
    top_25_cutoff = np.percentile(scores, 75)

    # Evaluation
    st.markdown(f"### 🎯 Your score: **{my_score}/12**")
    if estimate == my_score:
        st.info(f"🧠 You estimated: {estimate}/12 → ✅ Accurate")
    elif estimate > my_score:
        st.warning(f"🧠 You estimated: {estimate}/12 → ❌ Overestimated")
    else:
        st.info(f"🧠 You estimated: {estimate}/12 → ❌ Underestimated")

    st.markdown("### 📊 Updated Group Analysis:")
    in_top_50 = my_score >= median_score
    in_top_25 = my_score >= top_25_cutoff

    st.write(f"📈 You said you're in the **top 50%** → {'✅ Correct' if top_50_self == in_top_50 else '❌ Incorrect'}")
    st.write(f"📈 You said you're in the **top 25%** → {'✅ Correct' if top_25_self == in_top_25 else '❌ Incorrect'}")

    st.markdown("---")
    st.subheader("👥 All Submissions:")
    st.write(st.session_state.responses)
    st.stop()

# Correct answers
correct_math = [2, 5, 19, 20, 3, 15]
correct_general = [False, False, True, False, True, False]

# Quiz form
with st.form("quiz_form"):
    st.title("🧠 Quiz Game – Answer the Questions")

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
    st.experimental_rerun()
