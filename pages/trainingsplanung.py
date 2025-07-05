import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from streamlit_sortables import sort_items
from streamlit import experimental_rerun
from src.globals import (
    MAIN_FILE_PATH, SPORT_SESSIONS_PATH, main_data,
    sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions,
    cycle_phases, current_index, current_user, current_phase
)
from src.calculations import calculate_scores_complex, calculate_match_score_simple

#st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

def show_trainingsplanung():
    # CSS für vertikale Linie & Layout
    st.markdown("""
        <style>
            body {
                display: flex;
                text-align: center;
            }
            h3, h4 {
                font-family: 'Inter', sans-serif;
                margin-top: 40px;
                margin-bottom: 10px;
            }
            .phasely-selected-box {
                background-color: #F3F3F0;
                padding: 10px;
                border-radius: 12px;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                color: #2F2F2F;
                display: flex;
                margin-bottom: 10px;
                text-align: center;
                justify-content: center;
                align-items: center;
            }
            .phasely-delete-btn {
                background-color: #e57373;
                color: white;
                border: none;
                font-size: 1rem;
                float: right;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .phasely-delete-btn:hover {
                background-color: #d32f2f;
            }
        </style>
    """, unsafe_allow_html=True)

    custom_style = """
    .sortable-component {
        border: none;
        padding: 0px;
        margin: 0px;
    }
    .sortable-container {
        background-color: none;
        counter-reset: item;
        padding: 0px;
        margin: 0px;
        width: 14%;
    }
    .sortable-container-header {
        background-color: none;
        padding-left: 1rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sortable-container-body {
        background-color: #f4f4f4;
        border-radius: 12px;
        width: 100%;
        margin: 0px;
    }
    .sortable-item, .sortable-item:hover {
        background-color: #6B705C;
        padding: 10px;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
        font-size: 0.8rem;
    }
    .sortable-item::before {
        content: counter(item) ". ";
        counter-increment: item;
    }
    """

    st.markdown("""<h3>① Workouts auswählen</h3>""", unsafe_allow_html=True)
    st.write("Wähle 3–5 Sporteinheiten aus, welche du in den nächsten 3–7 Tagen machen möchtest.")

    # Sporteinheiten in Spalten anzeigen
    with st.container():
        if "selected_sessions" not in st.session_state:
                st.session_state.selected_sessions = []

        def render_sport_choices(title, sessions_list):
            st.markdown(f"""<h4>{title}</h4>""", unsafe_allow_html=True)

            #cols = st.columns(3)

            for index, session in enumerate(sessions_list):
                #with cols[index % 3]:
                    if st.button(session.session_name, key=f"kraft_{index}_{title}"):
                        if session in st.session_state.selected_sessions:
                            st.session_state.selected_sessions.remove(session)
                        elif len(st.session_state.selected_sessions) < 5:
                            st.session_state.selected_sessions.append(session)
        col1, col2, col3 = st.columns(3)
        with col1:
            render_sport_choices("🏋️ Krafttraining", strength_sessions)
        with col2:
            render_sport_choices("🏃 Ausdauertraining", cardio_sessions)
        with col3:
            render_sport_choices("🧘 Low-Impact", low_impact_sessions)

    # Abstand einfügen
    st.markdown("""<div style="height=50px;""", unsafe_allow_html=True)      

    # Ausgewählte Sporteinheiten anzeigen
    selected_sessions = []
    with st.container():
        session_placeholder = []
        st.markdown("""<h3>② Deine Auswahl</h3>""", unsafe_allow_html=True)

        if st.session_state.selected_sessions:
            cols = st.columns(5)  # 5 gleich breite Spalten

            for idx, session in enumerate(st.session_state.selected_sessions[:]):
                col = cols[idx % 5]  # rotiere durch die Spalten
                with col:
                    st.markdown(
                        f"<div class='phasely-selected-box'>{session.session_name}</div>",
                        unsafe_allow_html=True
                    )
                    session_placeholder.append(session.session_name)
                    if st.button("Entfernen", key=f"delete_{session.session_name}_{id(session)}"):
                        st.session_state.selected_sessions.remove(session)
                        st.experimental_rerun()
        else:
            st.write("Keine Sporteinheiten ausgewählt.")


    with st.container():
        st.markdown("""<h3>③ Plane deine Woche</h3>""", unsafe_allow_html=True)
        sorted_sessions = [
            {"header": "Montag", "items": session_placeholder},
            {"header": "Dienstag", "items": []},
            {"header": "Mittwoch", "items": []},
            {"header": "Donnerstag", "items": []},
            {"header": "Freitag", "items": []},
            {"header": "Samstag", "items": []},
            {"header": "Sonntag", "items": []}
        ]
        sorted_sessions = sort_items(sorted_sessions, direction="vertical", custom_style=custom_style, multi_containers=True)


    # ...existing code...

    if not sorted_sessions == []:
        # 1. Max. Anzahl an Einheiten pro Tag ermitteln (für Zeilenanzahl)
        max_len = max(len(block["items"]) for block in sorted_sessions)

        # 2. Dictionary vorbereiten: jeder Tag als Schlüssel, Liste der Einheiten als Wert (ggf. mit Leerzellen aufgefüllt)
        data = {
            block["header"]: block["items"] + [""] * (max_len - len(block["items"]))
            for block in sorted_sessions
        }

        # 3. DataFrame generieren: jede Spalte = ein Tag, jede Zeile = eine Einheit
        df = pd.DataFrame(data)

        if not df.empty and df.shape[0] > 0:
            def df_to_pdf_download(df):
                fig, ax = plt.subplots(figsize=(8, len(df)*0.6 + 1))  # Automatische Höhe
                ax.axis('off')
                ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

                buffer = BytesIO()
                plt.savefig(buffer, format='pdf', bbox_inches='tight')
                buffer.seek(0)
                return buffer

            pdf_buffer = df_to_pdf_download(df)
            st.download_button("📄 Als PDF herunterladen", pdf_buffer, file_name=f"{current_user.user_name}'s wochenplan.pdf", mime="application/pdf")
        else:
            st.info("Bitte wähle mindestens eine Sporteinheit aus, um einen Wochenplan zu erstellen.")
    else:
        st.info("Bitte wähle mindestens eine Sporteinheit aus, um einen Wochenplan zu erstellen.")

# %%
selected_sport = cardio_sessions[3]  # Example: select the first strength session

match_score = calculate_match_score_simple(selected_sport, current_phase, main_data, current_index)
print(f"Match score for {selected_sport.session_name} in {current_phase.phase_name}: {match_score * 100}%")

#%% Complex Calculation

sport_sessions[0].select_session("deselected")
sport_sessions[1].select_session("deselected")
sport_sessions[2].select_session("deselected")

final_score, final_strength_score, final_cardio_score, final_low_impact_score = calculate_scores_complex(sport_sessions, current_phase, main_data, current_index)
print(f"Der finale Kraft-Score ist: {final_strength_score *100}%")
print(f"Der finale Ausdauer-Score ist: {final_cardio_score *100}%")
print(f"Der finale Low-Impact-Score ist: {final_low_impact_score *100}%")

print(f"Der Gesamtscore ist: {final_score *100}%")
