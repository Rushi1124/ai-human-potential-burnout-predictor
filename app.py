import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from src.predictor import predict_risk, get_demo_model_info, FEATURES
from src.interventions import recommend_actions

st.set_page_config(
    page_title="Human Potential AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 1.7rem; padding-bottom: 3rem; max-width: 1200px;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#eef2ff,#f0fdfa);}
.hero h1 {margin: 0; color: #172554;}
.hero p {margin: .5rem 0 0; color: #334155; font-size: 1.05rem;}
.small-note {font-size: .86rem; color: #64748b;}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "saved_actions" not in st.session_state:
    st.session_state.saved_actions = []

with st.sidebar:
    st.title("🌱 Human Potential AI")
    st.caption("Human-centered well-being prototype")
    page = st.radio(
        "Navigate",
        ["Dashboard", "Assessment", "History", "About & Limitations"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Prototype v1.0 • Demo model")

if page == "Dashboard":
    st.markdown("""
    <div class="hero">
      <h1>Understand your patterns. Choose your next step.</h1>
      <p>A reflective tool for exploring sleep, workload, stress, focus, motivation, and balance.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    a, b, c = st.columns(3)
    a.metric("Assessments this session", len(st.session_state.history))
    b.metric("Latest assessment", "Available" if st.session_state.latest_result else "Not completed")
    c.metric("Your control", "You choose the actions")
    st.subheader("How it works")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("### 01 · Check in")
        st.write("Answer a few questions about your recent routine and experience.")
    with cols[1]:
        st.markdown("### 02 · Understand")
        st.write("Review a demonstration risk estimate and the patterns in your answers.")
    with cols[2]:
        st.markdown("### 03 · Choose")
        st.write("Select small, practical actions that feel useful to you.")
    st.warning(
        "This is an educational prototype using synthetic training data. "
        "It is not a clinical tool and cannot diagnose or reliably predict burnout."
    )
    if st.session_state.latest_result:
        r = st.session_state.latest_result
        st.subheader("Latest result")
        x, y = st.columns([1, 2])
        with x:
            st.metric("Demo model category", r["category"])
            st.metric("Demo model score", f'{r["risk_percent"]}%')
        with y:
            st.write("This score reflects the artificial rules used to generate demo labels, not a validated probability of burnout.")
            st.button("Start a new assessment", on_click=lambda: st.session_state.update({"latest_result": None}))

elif page == "Assessment":
    st.title("Personal check-in")
    st.write("Think about your recent routine. Use your own judgment; there are no right or wrong answers.")
    with st.form("assessment"):
        st.subheader("Daily routine")
        c1, c2, c3 = st.columns(3)
        with c1:
            sleep = st.slider("Sleep per night (hours)", 0.0, 12.0, 7.0, 0.5)
        with c2:
            workload = st.slider("Work/study hours per day", 0.0, 18.0, 7.0, 0.5)
        with c3:
            exercise = st.slider("Days with physical activity per week", 0, 7, 3)
        st.subheader("Your recent experience")
        c4, c5 = st.columns(2)
        with c4:
            stress = st.slider("Perceived stress (1 = low, 10 = high)", 1, 10, 5)
            motivation = st.slider("Motivation (1 = low, 10 = high)", 1, 10, 6)
        with c5:
            focus = st.slider("Ability to focus (1 = low, 10 = high)", 1, 10, 6)
            balance = st.slider("Work-life balance (1 = difficult, 10 = manageable)", 1, 10, 6)
        submitted = st.form_submit_button("Analyze my responses", type="primary", use_container_width=True)

    if submitted:
        answers = {
            "sleep_hours": sleep,
            "workload_hours": workload,
            "exercise_days": exercise,
            "stress": stress,
            "motivation": motivation,
            "focus": focus,
            "work_life_balance": balance,
        }
        result = predict_risk(answers)
        result["answers"] = answers
        st.session_state.latest_result = result
        st.session_state.history.append({
            "Assessment": len(st.session_state.history) + 1,
            "Category": result["category"],
            "Demo score (%)": result["risk_percent"],
            "Sleep (h)": sleep,
            "Workload (h)": workload,
            "Stress": stress,
        })
        st.rerun()

    result = st.session_state.latest_result
    if result:
        st.divider()
        st.header("Your result")
        left, right = st.columns([1, 1.4])
        with left:
            st.subheader(result["category"])
            st.metric("Demo model score", f'{result["risk_percent"]}%')
            st.caption("Not a clinically meaningful probability.")
            st.progress(result["risk_percent"] / 100)
        with right:
            st.subheader("Your response patterns")
            pattern = result["pattern_indicators"]
            chart_df = pd.DataFrame({"Factor": list(pattern.keys()), "Indicator": list(pattern.values())})
            fig = px.bar(chart_df, x="Indicator", y="Factor", orientation="h",
                         title="Simple indicators from your answers",
                         color_discrete_sequence=["#6366f1"])
            fig.update_layout(height=330, margin=dict(l=10, r=10, t=50, b=10), yaxis_title=None, xaxis_title="Indicator (not a clinical scale)")
            st.plotly_chart(fig, use_container_width=True)
        st.info("Why the caution? The model learned artificial labels generated by hand-written rules. These results demonstrate the app flow, not real-world burnout prediction.")
        st.subheader("Suggested actions")
        actions = recommend_actions(result["answers"])
        st.write("Select the actions you would actually like to try. You remain in control.")
        selected = []
        for i, action in enumerate(actions):
            if st.checkbox(action, key=f"action_{i}_{len(st.session_state.history)}"):
                selected.append(action)
        if st.button("Save selected actions for this session"):
            st.session_state.saved_actions = selected
            st.success(f"Saved {len(selected)} action(s) for this session.")
        if st.session_state.saved_actions:
            st.markdown("**Your selected actions**")
            for action in st.session_state.saved_actions:
                st.markdown(f"- {action}")

elif page == "History":
    st.title("Assessment history")
    st.write("History is stored in this active Streamlit session only. It is not written to a permanent database.")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.plotly_chart(
            px.line(df, x="Assessment", y="Demo score (%)", markers=True,
                    title="Demo score across assessments",
                    color_discrete_sequence=["#6366f1"]),
            use_container_width=True
        )
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download session history as CSV", csv, "assessment_history.csv", "text/csv")
        if st.button("Clear session history"):
            st.session_state.history = []
            st.session_state.latest_result = None
            st.session_state.saved_actions = []
            st.rerun()
    else:
        st.info("No assessments yet. Complete an assessment to see results here.")

else:
    st.title("About the project")
    st.markdown("""
### Project objective
Explore a human-centered interface that helps people reflect on workload, sleep, stress, motivation, focus, and work-life balance.

### Current technical design
- **UI:** Streamlit
- **Logic:** Python
- **Demo ML model:** Scikit-learn Random Forest
- **Charts:** Plotly
- **Data:** Synthetic data generated for demonstration

### What this prototype can do
- Collect user responses through an interactive form.
- Return a demo model category and score.
- Display response-pattern indicators.
- Offer optional, rule-based suggestions.
- Show session history and allow CSV export.

### What it cannot claim
- It has not been validated on real burnout outcomes.
- Its score is not a clinical probability.
- The demo model's feature importance does not establish causation.
- Recommendations are general well-being suggestions, not treatment.

### Next steps for a research-grade version
1. Find an ethically appropriate, documented dataset with relevant target labels.
2. Define the prediction target and intended use clearly.
3. Split data into training, validation, and test sets before model selection.
4. Compare a baseline model with candidate models.
5. Report precision, recall, F1, ROC-AUC where appropriate, and calibration.
6. Assess data leakage, subgroup performance, bias, and limitations.
7. Obtain appropriate consent and approvals before collecting personal data.
""")
    st.caption("Privacy note: this starter app does not use an external API or save assessment data to a permanent database.")
