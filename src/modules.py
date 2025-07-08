#%% Import
import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from streamlit_sortables import sort_items
from streamlit import experimental_rerun
from src.interface_components import h2, h3, h4, view_score_percentage, info_card, button, textblock
from src.scores import calculate_match_scores
from src.globals import (MAIN_FILE_PATH, main_data, current_index, strength_sessions, cardio_sessions, low_impact_sessions, current_user, current_phase, colors, current_cycle_day)

#%% Main
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


def current_cycle_plot_2():
    # Zyklusdaten vorbereiten
    current_cycle_days_history = np.arange(1, current_cycle_day + 1)
    current_cycle_days_future = np.arange(current_cycle_day, 29)

    current_cycle_intensity_history = [
        main_data["intensity_capacity"].iloc[i]
        for i in range(current_index, current_index - current_cycle_day, -1)
    ][::-1]

    current_cycle_intensity_future = [
        main_data["intensity_capacity"].iloc[i]
        for i in range(current_index+1, int(current_index + (29 - current_cycle_day)))
    ]

    # Alle Daten zusammenführen
    all_days = np.arange(1, 29)
    all_intensity = current_cycle_intensity_history + current_cycle_intensity_future

    # Glättung mit Spline
    x_smooth = np.linspace(all_days.min(), all_days.max(), 300)
    spline = make_interp_spline(all_days, all_intensity, k=3)
    y_smooth = spline(x_smooth)

    current_y = spline(current_cycle_day)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Hole exakt 28 Tage der Phase-Daten
    phases = list(main_data["phase"].iloc[current_index - current_cycle_day + 1 : current_index + 1])
    phases += list(main_data["future_phase"].iloc[current_index + 1 : current_index + 1 + (28 - len(phases))])

    phase_colors = {
        "Menstruation": "#DDBEA9",
        "Follikelphase": "#A5A58D",
        "Ovulation": "#6B705C",
        "Lutealphase": "#B7B7A4"
    }

    # Hintergrund einfärben
    start_day = 1
    current_phase = phases[0]

    for day in range(1, len(phases) + 1):
        phase = phases[day - 1]
        if phase != current_phase:
            # Vorherige Phase einfärben & labeln
            ax.axvspan(start_day - 0.5, day - 0.5, color=phase_colors.get(current_phase, "#eee"), alpha=0.1)
            ax.text(
                (start_day + day - 1) / 2,
                ax.get_ylim()[1] + 0.06,
                current_phase,
                ha="center",
                va="bottom",
                fontsize=10,
                color=phase_colors.get(current_phase, "#444"),
                alpha=1.0
            )
            current_phase = phase
            start_day = day

    # Letzte Phase bis zum Ende (Tag 28.5)
    ax.axvspan(start_day - 0.5, 28.5, color=phase_colors.get(current_phase, "#eee"), alpha=0.1)
    ax.text(
        (start_day + 28) / 2,
        ax.get_ylim()[1] + 0.06,
        current_phase,
        ha="center",
        va="bottom",
        fontsize=10,
        color=phase_colors.get(current_phase, "#444"),
        alpha=1.0
    )

    ax.plot(x_smooth, y_smooth, color=colors["Primary"], linewidth=2)
    ax.plot(current_cycle_day, current_y, "o", color=colors["Highlight"], markersize=8, label="Heute")

    # Achsen
    ax.set_xlabel("Zyklustag", fontsize=12)
    ax.set_ylabel("Intensitäts-Kapazität", fontsize=12)
    ax.set_xticks(np.arange(1, 29, 2))
    ax.set_ylim(0, 1.05)
    ax.xaxis.set_label_coords(0.5, -0.08)
    ax.yaxis.set_label_coords(-0.07, 0.5)

    # Stil
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.1)

    st.pyplot(fig)
# %%
