import streamlit as st
from src.globals import (current_user, current_phase, colors, current_cycle_day)
from src.interface_components import h1, h2, h3, textblock, view_score_percentage, info_card, button
from src.modules import show_match_scores, show_selection, show_wochenplanung, current_cycle_plot_2

if "current_subject" not in st.session_state:
    current_subject = "No subject selected"

#%% Configure Streamlit App

st.set_page_config(
    page_title="Phasely",
    page_icon=":heart:",
    layout="wide",
    initial_sidebar_state="collapsed",
    )


# Titelbereich
h1(f"""{current_user.user_name}'s Phasely Dashboard""")
textblock("Willkommen zu deinem Phasely Dashboard! Hier bekommst du reichlich Infos über deine Zyklusphasen und die optimale Trainingsgestaltung während dieser Phasen. Du kannst sogar Sporteinheiten auswählen und sehen, wie gut sie zu deiner aktuellen Phase passen. Viel Spaß!")
st.markdown("---")

# Current-Phase Bereich
h2(f"""Du bist in deiner <span style="color: {colors["Primary"]};">{current_phase.phase_name}</span>""")
textblock(current_phase.description)

with st.container():
    textblock(f"""<span style="font-weight:bold;">Heute ist dein {current_cycle_day}. Zyklustag!</span>""")
    colleft, col1, colright = st.columns([3,6,3])
    with col1:
        current_cycle_plot_2()

# Trainingsverteilung
h3("Optimale Trainingsverteilung")
colleft, col1, col2, col3, col4, colright = st.columns(6)
with col1:
    view_score_percentage(current_phase.strength_score, "Krafttraining", colors["Primary"])
with col2:
    view_score_percentage(current_phase.cardio_score, "Ausdauertraining", colors["Primary"])
with col3:
    view_score_percentage(current_phase.low_impact_score, "Low-Impact Training", colors["Primary"])
with col4:
    st.markdown(f"""
        <div style="text-align: center; font-family: 'Inter', sans-serif;">
            <div style="font-size: 40px; font-weight: bold; color: #834F34; margin-top: 20px;">{int(min(current_phase.training_intensity) * 100)} - {int(max(current_phase.training_intensity) * 100)}%</div>
            <div style="margin-bottom: 8px;">Intensität</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Call-To-Action
h2("Erstelle dein zyklusbasiertes Training")

# Info-Bereich
colleft, col1, col2, colrigth = st.columns([2, 4, 4, 2])
with col1:
    info_card("Warum zyklusbasiertes Training?", "Dein Zyklus beeinflusst Energie, Belastbarkeit und Regeneration. Ein Training, das auf deine jeweilige Phase abgestimmt ist, kann effektiver, nachhaltiger und angenehmer sein.")
with col2:
    info_card("Wie funktioniert das?", "Je nach Phase (z. B. Menstruation, Follikelphase) verändern sich Hormone, die dein Training beeinflussen. Phasely passt deine Workouts daran an und unterstützt dich mit datenbasierten Empfehlungen.")

# Button und Session-State für Anzeige
colleft, col1, colright = st.columns(3)
with col1:
    button("show_trainingsplanung", "✨ Zyklusbasierte Trainingswoche erstellen ✨")

if st.session_state["show_trainingsplanung"]:
    show_selection()
    show_match_scores()
