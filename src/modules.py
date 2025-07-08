"""
modules.py

Enthält Hauptfunktionen der App:
- Sporteinheiten auswählen
- Score berechnen
- Wochenplan erstellen (inkl. PDF-Export)
- Visualisierung des aktuellen Zyklusverlaufs
"""

#%% Imports
import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from streamlit_sortables import sort_items
from streamlit import experimental_rerun

from src.interface_components import (
    h2, h3, h4, view_score_percentage,
    info_card, button, textblock
)
from src.scores import calculate_match_scores
from src.globals import (
    get_main_data, get_current_index, get_current_cycle_day,
    get_color_palette, get_current_phase
)

#%% Sporteinheiten-Auswahl
def show_selection():
    """
    Zeigt die Auswahl aller verfügbaren Sporteinheiten nach Kategorie.
    Erlaubt das Hinzufügen und Entfernen zur Auswahl im Session-State.
    """
    h3("① Workouts auswählen")
    textblock("Wähle 3–5 Sporteinheiten aus, welche du in den nächsten 3–7 Tagen machen möchtest.")

    # Lade Einheiten aus Session
    strength_sessions = st.session_state.get("strength_sessions", [])
    cardio_sessions = st.session_state.get("cardio_sessions", [])
    low_impact_sessions = st.session_state.get("low_impact_sessions", [])

    if "selected_sessions" not in st.session_state:
        st.session_state.selected_sessions = []

    def render_sport_choices(title, sessions_list):
        h4(title)
        for index, session in enumerate(sessions_list):
            if st.button(session.session_name, key=f"{title}_{index}"):
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

    # Auswahl anzeigen
    with st.container():
        if st.session_state.selected_sessions:
            cols = st.columns(5)
            for idx, session in enumerate(st.session_state.selected_sessions[:]):
                with cols[idx % 5]:
                    st.markdown(
                        f"<div class='phasely-selected-box'>{session.session_name}</div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Entfernen", key=f"delete_{session.session_name}_{id(session)}"):
                        st.session_state.selected_sessions.remove(session)
                        experimental_rerun()
        else:
            st.write("Keine Sporteinheiten ausgewählt.")

#%% Score-Berechnung
def show_match_scores():
    """
    Berechnet und visualisiert, wie gut die Auswahl zur aktuellen Zyklusphase passt.
    Zeigt Gesamtscore, Kategorien und Tabelle der ausgewählten Workouts.
    """
    selected_sessions = st.session_state.get("selected_sessions", [])
    if not selected_sessions:
        st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
        st.warning("Noch keine Sporteinheiten ausgewählt.")
        return

    current_phase = get_current_phase()
    colors = get_color_palette()

    df_scores, final_score, s, c, l, intensity, score_texts = calculate_match_scores(selected_sessions, current_phase)

    st.markdown("---")
    h3("② Score Berechnung")
    textblock("Wie gut passen deine ausgewählten Sporteinheiten zu deiner aktuellen Zyklusphase?")

    # Score: Gesamt
    colleft, col1, colright = st.columns(3)
    with col1:
        view_score_percentage(final_score, "Dein Gesamtscore", colors["Highlight"])

    # Score: Ist
    colleft, col1, col2, col3, col4, colright = st.columns(6)
    with col1:
        view_score_percentage(s, "Kraft", colors["Highlight-light"])
    with col2:
        view_score_percentage(c, "Ausdauer", colors["Highlight-light"])
    with col3:
        view_score_percentage(l, "Low Impact", colors["Highlight-light"])
    with col4:
        view_score_percentage(intensity, "Ø Intensität", "#171664")

    # Score: Soll
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
                <div style="font-size: 40px; font-weight: bold; color: #Bebebe; margin-top: 20px;">
                    {int(min(current_phase.training_intensity) * 100)} - {int(max(current_phase.training_intensity) * 100)}%
                </div>
                <div style="margin-bottom: 8px;">Soll-Intensität</div>
            </div>
        """, unsafe_allow_html=True)

    # Hinweis je nach Score
    st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
    if final_score >= 0.7:
        st.success("Deine Auswahl passt super zusammen!")
    elif final_score >= 0.45:
        st.warning("Dein Score ist OK. Tausche noch ein bisschen herum!")
    else:
        st.error("Auweh! Wähle andere Sporteinheiten aus... dann passt dein Training besser zu deiner Zyklusphase!")

    # Tabelle
    h4("Übersicht aller Einheiten")
    st.dataframe(df_scores)

    st.markdown("---")
    button("show_wochenplanung", "Wochenplan erstellen")
    if st.session_state["show_wochenplanung"]:
        show_wochenplanung()

#%% Wochenplan-Tool
def show_wochenplanung():
    """
    Zeigt interaktive Sortierkomponente zur Wochenplanung.
    Erstellt optional einen PDF-Download aus dem Plan.
    """
    h3("③ Plane deine Woche")

    # Initiale Container
    sorted_sessions = [
        {"header": "Montag", "items": [s.session_name for s in st.session_state.selected_sessions]},
        {"header": "Dienstag", "items": []},
        {"header": "Mittwoch", "items": []},
        {"header": "Donnerstag", "items": []},
        {"header": "Freitag", "items": []},
        {"header": "Samstag", "items": []},
        {"header": "Sonntag", "items": []}
    ]

    # Custom Style
    custom_style = """
    .sortable-container-body {
        background-color: #f5f5f5;
        border-radius: 12px;
    }
    .sortable-item {
        background-color: #F3EAE2;
        padding: 10px;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: black !important;
    }
    .sortable-item::before {
        content: counter(item) ". ";
        counter-increment: item;
    }
    """
    sorted_sessions = sort_items(sorted_sessions, direction="vertical", custom_style=custom_style, multi_containers=True)

    # PDF-Erzeugung
    if sorted_sessions:
        max_len = max(len(day["items"]) for day in sorted_sessions)
        data = {day["header"]: day["items"] + [""] * (max_len - len(day["items"])) for day in sorted_sessions}
        df = pd.DataFrame(data)

        if not df.empty:
            def df_to_pdf_download(df):
                fig, ax = plt.subplots(figsize=(8, len(df) * 0.6 + 1))
                ax.axis("off")
                ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

                buffer = BytesIO()
                plt.savefig(buffer, format="pdf", bbox_inches="tight")
                buffer.seek(0)
                return buffer

            pdf_buffer = df_to_pdf_download(df)
            user = st.session_state.get("current_user", None)
            file_name = f"{user.user_name}'s_Wochenplan.pdf" if user else "Wochenplan.pdf"
            st.download_button("📄 Als PDF herunterladen", pdf_buffer, file_name=file_name, mime="application/pdf")
        else:
            st.info("Bitte wähle mindestens eine Sporteinheit aus, um einen Wochenplan zu erstellen.")
    else:
        st.info("Bitte wähle mindestens eine Sporteinheit aus, um einen Wochenplan zu erstellen.")

#%% Zykluskurve
def current_cycle_plot_2():
    """
    Zeichnet den aktuellen Zyklusverlauf (Intensität vs. Zyklustag) mit Phasenhintergrund.
    """
    main_data = get_main_data()
    current_index = get_current_index()
    current_cycle_day = get_current_cycle_day()
    colors = get_color_palette()

    # Daten vorbereiten
    history_days = np.arange(1, current_cycle_day + 1)
    future_days = np.arange(current_cycle_day, 29)

    history_intensity = [
        main_data["intensity_capacity"].iloc[i]
        for i in range(current_index, current_index - current_cycle_day, -1)
    ][::-1]

    future_intensity = [
        main_data["intensity_capacity"].iloc[i]
        for i in range(current_index + 1, int(current_index + (29 - current_cycle_day)))
    ]

    all_days = np.arange(1, 29)
    all_intensity = history_intensity + future_intensity

    # Glätten
    x_smooth = np.linspace(all_days.min(), all_days.max(), 300)
    spline = make_interp_spline(all_days, all_intensity, k=3)
    y_smooth = spline(x_smooth)

    # Phasen einfärben
    phases = list(main_data["phase"].iloc[current_index - current_cycle_day + 1: current_index + 1])
    phases += list(main_data["future_phase"].iloc[current_index + 1: current_index + 1 + (28 - len(phases))])

    phase_colors = {
        "Menstruation": "#DDBEA9",
        "Follikelphase": "#A5A58D",
        "Ovulation": "#6B705C",
        "Lutealphase": "#B7B7A4"
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    start_day = 1
    current_phase = phases[0]

    for day in range(1, len(phases) + 1):
        phase = phases[day - 1]
        if phase != current_phase:
            ax.axvspan(start_day - 0.5, day - 0.5, color=phase_colors.get(current_phase, "#eee"), alpha=0.1)
            ax.text((start_day + day - 1) / 2, ax.get_ylim()[1] + 0.06, current_phase,
                    ha="center", va="bottom", fontsize=10, color=phase_colors.get(current_phase, "#444"))
            current_phase = phase
            start_day = day

    # Letzte Phase
    ax.axvspan(start_day - 0.5, 28.5, color=phase_colors.get(current_phase, "#eee"), alpha=0.1)
    ax.text((start_day + 28) / 2, ax.get_ylim()[1] + 0.06, current_phase,
            ha="center", va="bottom", fontsize=10, color=phase_colors.get(current_phase, "#444"))

    # Plot zeichnen
    ax.plot(x_smooth, y_smooth, color=colors["Primary"], linewidth=2)
    ax.plot(current_cycle_day, spline(current_cycle_day), "o", color=colors["Highlight"], markersize=8)

    ax.set_xlabel("Zyklustag", fontsize=12)
    ax.set_ylabel("Intensitäts-Kapazität", fontsize=12)
    ax.set_xticks(np.arange(1, 29, 2))
    ax.set_ylim(0, 1.05)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.1)

    st.pyplot(fig)
