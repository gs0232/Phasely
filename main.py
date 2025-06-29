#%% Import
from src.data_setup import load_data, set_sport_sessions, set_cycle_phases
from src.classes import User
from src.calculations import calculate_scores_complex, calculate_match_score_simple
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st #pdm add streamlit

#%% Configure Streamlit App

st.set_page_config(
    page_title="Phasely",
    #page_icon=":heart:",
    layout="centered",
    initial_sidebar_state="auto",
    )

if "current_subject" not in st.session_state:
    current_subject = "No subject selected"

#%% Set data
MAIN_FILE_PATH = "data/cycle_tracking_2025.csv"
SPORT_SESSIONS_PATH = "data/sport_sessions.csv"

main_data = load_data(MAIN_FILE_PATH)
sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions = set_sport_sessions(SPORT_SESSIONS_PATH)
cycle_phases = set_cycle_phases()

first_future_index = main_data[main_data["is_historic"] == False].index[0]
current_index = first_future_index - 1

print(current_index)


#%% Initialzie User and current phase
current_user = User(1, "Heidi", 22)
current_user.assign_user_data(main_data)

current_phase_name = main_data["phase"].iloc[current_index]

for i in cycle_phases:
    if i.phase_name == current_phase_name:
        current_phase = i
        break

# %%
selected_sport = cardio_sessions[3]  # Example: select the first strength session

match_score = calculate_match_score_simple(selected_sport, current_phase, main_data, current_index)
print(f"Match score for {selected_sport.session_name} in {current_phase.phase_name}: {match_score * 100}%")

#%% Complex Calculation

sport_sessions[0].select_session("selected")
sport_sessions[1].select_session("selected")
sport_sessions[2].select_session("selected")

final_score, final_strength_score, final_cardio_score, final_low_impact_score = calculate_scores_complex(sport_sessions, current_phase, main_data, current_index)
print(f"Der finale Kraft-Score ist: {final_strength_score *100}%")
print(f"Der finale Ausdauer-Score ist: {final_cardio_score *100}%")
print(f"Der finale Low-Impact-Score ist: {final_low_impact_score *100}%")

print(f"Der Gesamtscore ist: {final_score *100}%")

# %% Interface with Streamlit
st.title("Phasely - Your Personalized Training Companion")
st.sidebar.header("User Selection")
st.sidebar.write(f"Current User: {current_user.name} (ID: {current_user.user_id})")
st.sidebar.write(f"Current Phase: {current_phase.phase_name}")
st.sidebar.write(f"Current Index: {current_index}")
st.sidebar.write(f"Current Phase Start: {current_phase.start_date}")
st.sidebar.write(f"Current Phase End: {current_phase.end_date}")
st.sidebar.write(f"Current Phase Duration: {current_phase.duration} days")
st.sidebar.write(f"Current Phase Strength Focus: {current_phase.strength_focus}")
st.sidebar.write(f"Current Phase Cardio Focus: {current_phase.cardio_focus}")
st.sidebar.write(f"Current Phase Low Impact Focus: {current_phase.low_impact_focus}")
st.sidebar.write(f"Current Phase Strength Score: {current_phase.strength_score * 100}%")
st.sidebar.write(f"Current Phase Cardio Score: {current_phase.cardio_score * 100}%")
st.sidebar.write(f"Current Phase Low Impact Score: {current_phase.low_impact_score * 100}%")
st.sidebar.write(f"Current Phase Overall Score: {current_phase.overall_score * 100}%")
st.sidebar.write("Sport Sessions:")
for session in sport_sessions:
    st.sidebar.write(f"- {session.session_name} (Type: {session.session_type}, Duration: {session.duration} min, Intensity: {session.intensity})")
st.sidebar.write("Strength Sessions:")
for session in strength_sessions:
    st.sidebar.write(f"- {session.session_name} (Type: {session.session_type}, Duration: {session.duration} min, Intensity: {session.intensity})")
st.sidebar.write("Cardio Sessions:")
for session in cardio_sessions:
    st.sidebar.write(f"- {session.session_name} (Type: {session.session_type}, Duration: {session.duration} min, Intensity: {session.intensity})")
st.sidebar.write("Low Impact Sessions:")
for session in low_impact_sessions:
    st.sidebar.write(f"- {session.session_name} (Type: {session.session_type}, Duration: {session.duration} min, Intensity: {session.intensity})")
st.sidebar.write(f"Match Score for {selected_sport.session_name} in {current_phase.phase_name}: {match_score * 100}%")
st.sidebar.write(f"Final Strength Score: {final_strength_score * 100}%")
st.sidebar.write(f"Final Cardio Score: {final_cardio_score * 100}%")
st.sidebar.write(f"Final Low Impact Score: {final_low_impact_score * 100}%")
st.sidebar.write(f"Final Overall Score: {final_score * 100}%")
# Display the current phase data in a table
phase_data = {
    "Phase Name": [current_phase.phase_name],
    "Start Date": [current_phase.start_date],
    "End Date": [current_phase.end_date],
    "Duration (days)": [current_phase.duration],
    "Strength Focus": [current_phase.strength_focus],
    "Cardio Focus": [current_phase.cardio_focus],
    "Low Impact Focus": [current_phase.low_impact_focus],
    "Strength Score": [current_phase.strength_score * 100],
    "Cardio Score": [current_phase.cardio_score * 100],
    "Low Impact Score": [current_phase.low_impact_score * 100],
    "Overall Score": [current_phase.overall_score * 100]
}
phase_df = pd.DataFrame(phase_data)
st.sidebar.write("Current Phase Data:")
st.sidebar.dataframe(phase_df)
# Display the sport sessions in a table
sport_sessions_data = {
    "Session Name": [session.session_name for session in sport_sessions],
    "Session Type": [session.session_type for session in sport_sessions],
    "Duration (min)": [session.duration for session in sport_sessions],
    "Intensity": [session.intensity for session in sport_sessions],
    "Selected": [session.selected for session in sport_sessions]
}
sport_sessions_df = pd.DataFrame(sport_sessions_data)
st.sidebar.write("Sport Sessions Data:")
st.sidebar.dataframe(sport_sessions_df)
# Display the strength sessions in a table
strength_sessions_data = {
    "Session Name": [session.session_name for session in strength_sessions],
    "Session Type": [session.session_type for session in strength_sessions],
    "Duration (min)": [session.duration for session in strength_sessions],
    "Intensity": [session.intensity for session in strength_sessions]
}
strength_sessions_df = pd.DataFrame(strength_sessions_data)
st.sidebar.write("Strength Sessions Data:")
st.sidebar.dataframe(strength_sessions_df)
# Display the cardio sessions in a table
cardio_sessions_data = {
    "Session Name": [session.session_name for session in cardio_sessions],
    "Session Type": [session.session_type for session in cardio_sessions],
    "Duration (min)": [session.duration for session in cardio_sessions],
    "Intensity": [session.intensity for session in cardio_sessions]
}
cardio_sessions_df = pd.DataFrame(cardio_sessions_data)
st.sidebar.write("Cardio Sessions Data:")
st.sidebar.dataframe(cardio_sessions_df)
# Display the low impact sessions in a table
low_impact_sessions_data = {
    "Session Name": [session.session_name for session in low_impact_sessions],
    "Session Type": [session.session_type for session in low_impact_sessions],
    "Duration (min)": [session.duration for session in low_impact_sessions],
    "Intensity": [session.intensity for session in low_impact_sessions]
}
low_impact_sessions_df = pd.DataFrame(low_impact_sessions_data)
st.sidebar.write("Low Impact Sessions Data:")
st.sidebar.dataframe(low_impact_sessions_df)
# Display the match score in a table
match_score_data = {
    "Session Name": [selected_sport.session_name],
    "Phase Name": [current_phase.phase_name],
    "Match Score (%)": [match_score * 100]
}
match_score_df = pd.DataFrame(match_score_data)
st.sidebar.write("Match Score Data:")
st.sidebar.dataframe(match_score_df)
# Display the final scores in a table
final_scores_data = {
    "Final Strength Score (%)": [final_strength_score * 100],
    "Final Cardio Score (%)": [final_cardio_score * 100],
    "Final Low Impact Score (%)": [final_low_impact_score * 100],
    "Final Overall Score (%)": [final_score * 100]
}
final_scores_df = pd.DataFrame(final_scores_data)
st.sidebar.write("Final Scores Data:")
st.sidebar.dataframe(final_scores_df)
# Display a bar chart of the final scores
fig = px.bar(final_scores_df,
                x=final_scores_df.columns,
                y=final_scores_df.iloc[0],
                title="Final Scores",
                labels={"x": "Score Type", "y": "Score (%)"},
                color_discrete_sequence=["#636EFA"])
st.sidebar.plotly_chart(fig, use_container_width=True)
# Display a bar chart of the current phase scores
phase_scores_data = {
    "Score Type": ["Strength Score", "Cardio Score", "Low Impact Score", "Overall Score"],
    "Score (%)": [
        current_phase.strength_score * 100,
        current_phase.cardio_score * 100,
        current_phase.low_impact_score * 100,
        current_phase.overall_score * 100
    ]
}
phase_scores_df = pd.DataFrame(phase_scores_data)
fig_phase = px.bar(phase_scores_df,
                    x="Score Type",
                    y="Score (%)",
                    title="Current Phase Scores",
                    labels={"x": "Score Type", "y": "Score (%)"},
                    color_discrete_sequence=["#EF553B"])
st.sidebar.plotly_chart(fig_phase, use_container_width=True)
# Display a bar chart of the sport sessions
sport_sessions_scores_data = {
    "Session Name": [session.session_name for session in sport_sessions],
    "Score (%)": [session.selected * 100 for session in sport_sessions]
}
sport_sessions_scores_df = pd.DataFrame(sport_sessions_scores_data)
fig_sport_sessions = px.bar(sport_sessions_scores_df,
                            x="Session Name",
                            y="Score (%)",
                            title="Sport Sessions Scores",
                            labels={"x": "Session Name", "y": "Score (%)"},
                            color_discrete_sequence=["#00CC96"])
st.sidebar.plotly_chart(fig_sport_sessions, use_container_width=True)
# Display a bar chart of the strength sessions
strength_sessions_scores_data = {
    "Session Name": [session.session_name for session in strength_sessions],
    "Score (%)": [session.selected * 100 for session in strength_sessions]
}
strength_sessions_scores_df = pd.DataFrame(strength_sessions_scores_data)
fig_strength_sessions = px.bar(strength_sessions_scores_df,
                                x="Session Name",
                                y="Score (%)",
                                title="Strength Sessions Scores",
                                labels={"x": "Session Name", "y": "Score (%)"},
                                color_discrete_sequence=["#AB63FA"])
st.sidebar.plotly_chart(fig_strength_sessions, use_container_width=True)
# Display a bar chart of the cardio sessions
cardio_sessions_scores_data = {
    "Session Name": [session.session_name for session in cardio_sessions],
    "Score (%)": [session.selected * 100 for session in cardio_sessions]
}
cardio_sessions_scores_df = pd.DataFrame(cardio_sessions_scores_data)
fig_cardio_sessions = px.bar(cardio_sessions_scores_df,
                                x="Session Name",
                                y="Score (%)",
                                title="Cardio Sessions Scores",
                                labels={"x": "Session Name", "y": "Score (%)"},
                                color_discrete_sequence=["#FFA15A"])
st.sidebar.plotly_chart(fig_cardio_sessions, use_container_width=True)
# Display a bar chart of the low impact sessions
low_impact_sessions_scores_data = {
    "Session Name": [session.session_name for session in low_impact_sessions],
    "Score (%)": [session.selected * 100 for session in low_impact_sessions]
}
low_impact_sessions_scores_df = pd.DataFrame(low_impact_sessions_scores_data)
fig_low_impact_sessions = px.bar(low_impact_sessions_scores_df,
                                x="Session Name",
                                y="Score (%)",
                                title="Low Impact Sessions Scores",
                                labels={"x": "Session Name", "y": "Score (%)"},
                                color_discrete_sequence=["#19D3F3"])
st.sidebar.plotly_chart(fig_low_impact_sessions, use_container_width=True)
# Display a line chart of the user's scores over time
user_scores_data = {
    "Date": main_data["date"],
    "Strength Score (%)": main_data["strength_score"] * 100,
    "Cardio Score (%)": main_data["cardio_score"] * 100,
    "Low Impact Score (%)": main_data["low_impact_score"] * 100,
    "Overall Score (%)": main_data["overall_score"] * 100
}
user_scores_df = pd.DataFrame(user_scores_data)
fig_user_scores = px.line(user_scores_df,
                            x="Date",
                            y=["Strength Score (%)", "Cardio Score (%)", "Low Impact Score (%)", "Overall Score (%)"],
                            title="User Scores Over Time",
                            labels={"x": "Date", "y": "Score (%)"},
                            color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#AB63FA"])
st.sidebar.plotly_chart(fig_user_scores, use_container_width=True)
