import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from streamlit_sortables import sort_items
from streamlit import experimental_rerun
from src.interface_components import h2, h3, h4, view_score_percentage, info_card, button, textblock
from src.scores import calculate_match_scores
from src.globals import (strength_sessions, cardio_sessions, low_impact_sessions, current_user, current_phase, colors)

def show_selection():
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
                background-color: #F3EAE2;
                padding: 10px;
                border-radius: 12px;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                color: black !important;
                display: flex;
                margin-bottom: 10px;
                margin-top: 40px;
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

    h3("① Workouts auswählen")
    textblock("Wähle 3–5 Sporteinheiten aus, welche du in den nächsten 3–7 Tagen machen möchtest.")

    # Sporteinheiten in Spalten anzeigen
    with st.container():
        if "selected_sessions" not in st.session_state:
                st.session_state.selected_sessions = []

        def render_sport_choices(title, sessions_list):
            h4(title)

            for index, session in enumerate(sessions_list):
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

        # Ausgewählte Sporteinheiten anzeigen
        #selected_sessions = []
        with st.container():
            session_placeholder = []

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
                        #selected_sessions.append(session)
                        if st.button("Entfernen", key=f"delete_{session.session_name}_{id(session)}"):
                            st.session_state.selected_sessions.remove(session)
                            #selected_sessions.remove(session)
                            st.experimental_rerun()

            else:
                st.write("Keine Sporteinheiten ausgewählt.")



def show_match_scores():
    selected_sessions = st.session_state.get("selected_sessions", [])
    if not selected_sessions:
        st.markdown(f"""<div style='margin-top:60px'></div>""", unsafe_allow_html=True)
        st.warning("Noch keine Sporteinheiten ausgewählt.")
        return
    
    df_scores, final_overall_score, final_strength_score, final_cardio_score, final_low_impact_score, final_intensity_score, text = calculate_match_scores(selected_sessions, current_phase)

    st.markdown("---")

    h3("② Score Berechnung")
    textblock("Wie gut passen deine ausgewählten Sporteinheiten zu deiner aktuellen Zyklusphase?")

    colleft, col1, colright = st.columns(3)
    with col1:
        view_score_percentage(final_overall_score, "Dein Gesamtscore", colors["Highlight"])

    # Score-Anzeige in Spalten
    colleft, col1, col2, col3, col4, colright = st.columns(6)
    with col1:
        view_score_percentage(final_strength_score, "Kraft", colors["Highlight-light"])
    with col2:
        view_score_percentage(final_cardio_score, "Ausdauer", colors["Highlight-light"])
    with col3:
        view_score_percentage(final_low_impact_score, "Low Impact", colors["Highlight-light"])
    with col4:
        view_score_percentage(final_intensity_score, "Intensität", "#171664")

    # So soll es sein
    colleft, col1, col2, col3, col4, colright = st.columns(6)
    with col1:
        view_score_percentage(current_phase.strength_score, "Soll-Kraft", "#bebebe")
    with col2:
        view_score_percentage(current_phase.cardio_score, "Soll-Ausdauer", "#bebebe")
    with col3:
        view_score_percentage(current_phase.low_impact_score, "Soll-Low-Impact", "#bebebe")
    with col4:
        st.markdown(f"""
            <div style="text-align: center; font-family: 'Inter', sans-serif;">
                <div style="font-size: 40px; font-weight: bold; color: #Bebebe; margin-top: 20px;">{int(min(current_phase.training_intensity) * 100)} - {int(max(current_phase.training_intensity) * 100)}%</div>
                <div style="margin-bottom: 8px;">Soll-Intensität</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""<div style='margin-top:60px'></div>""", unsafe_allow_html=True)

    if final_overall_score >= 0.7:
        st.success("Deine Auswahl passt super zusammen!")
    elif final_overall_score >= 0.45 and final_overall_score < 0.7:
        st.warning("Dein Score ist OK. Tausche noch ein bisschen herum!")
    else:
        st.error("Auweh! Wähle andere Sporteinheiten aus... dann passt dein Training besser zu deiner Zyklusphase!")

    # Tabelle mit Übersicht
    h4("Übersicht aller Einheiten")
    st.dataframe(df_scores)

    st.markdown("---")

    button("show_wochenplanung", "Wochenplan erstellen")
    if st.session_state["show_wochenplanung"]:
        show_wochenplanung()


def show_wochenplanung():
     
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
        background-color: #f5f5f5;
        border-radius: 12px;
        width: 100%;
        margin: 0px;
    }
    .sortable-item, .sortable-item:hover {
        background-color: #F3EAE2;
        padding: 10px;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        color: black !important;
        font-size: 0.8rem;
    }
    .sortable-item::before {
        content: counter(item) ". ";
        counter-increment: item;
    }"""

    with st.container():
        h3("③ Plane deine Woche")
        sorted_sessions = [
            {"header": "Montag", "items": [s.session_name for s in st.session_state.selected_sessions]},
            {"header": "Dienstag", "items": []},
            {"header": "Mittwoch", "items": []},
            {"header": "Donnerstag", "items": []},
            {"header": "Freitag", "items": []},
            {"header": "Samstag", "items": []},
            {"header": "Sonntag", "items": []}
        ]
        sorted_sessions = sort_items(sorted_sessions, direction="vertical", custom_style=custom_style, multi_containers=True)


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