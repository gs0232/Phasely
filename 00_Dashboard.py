import streamlit as st
from src.globals import (current_user, current_phase)
from pages.trainingsplanung import show_trainingsplanung
from pages.gesamtscore import show_match_scores
from src.interface_components import h1, h2, h3, textblock, h_divider, view_score_percentage, info_card, button

if "current_subject" not in st.session_state:
    current_subject = "No subject selected"

#%% Configure Streamlit App

st.set_page_config(
    page_title="Phasely",
    page_icon=":heart:",
    layout="wide",
    initial_sidebar_state="collapsed",
    )

# %% Interface with Streamlit

primary_color = "#CB997E"
highlight_color = "#FF69B4"  # für pink
mint = "#95d5b2"
menstruation = "#DDBEA9"
follikelphase = "#A5A58D"
ovulation = "#6B705C"
lutealphase = "#B7B7A4"

# Schriftgrößen und Layout
score_font_size = "36px"

# Titelbereich
h1(f"""{current_user.user_name}'s Phasely Dashboard""")
textblock("Willkommen zu deinem Phasely Dashboard! Hier Hier bekommst du reichlich Infos über deine Zyklusphasen und die optimale Trainingsgestaltung während dieser Phasen. Du kannst sogar Sporteinheiten auswählen und sehen, wie gut sie zu deiner aktuellen Phase passen. Viel Spaß!")
h_divider()

# Current-Phase Bereich
h2(f"""Du bist in deiner <span style="color: {primary_color};">{current_phase.phase_name}</span>""")
textblock(current_phase.description)

# Trainingsverteilung
h3("Optimale Trainingsverteilung")
colleft, col1, col2, col3, colright = st.columns([2, 1, 1, 1, 2])
with col1:
    view_score_percentage(current_phase.strength_score, "Krafttraining")
with col2:
    view_score_percentage(current_phase.cardio_score, "Ausdauertraining")
with col3:
    view_score_percentage(current_phase.low_impact_score, "Low-Impact Training")

# Info-Bereich
colleft, col1, col2, colrigth = st.columns([2, 4, 4, 2])
with col1:
    info_card("Warum zyklusbasiertes Training?", "Dein Zyklus beeinflusst Energie, Belastbarkeit und Regeneration. Ein Training, das auf deine jeweilige Phase abgestimmt ist, kann effektiver, nachhaltiger und angenehmer sein.")
with col2:
    info_card("Wie funktioniert das?", "Je nach Phase (z. B. Menstruation, Follikelphase) verändern sich Hormone, die dein Training beeinflussen. Phasely passt deine Workouts daran an und unterstützt dich mit datenbasierten Empfehlungen.")

# Call-To-Action
h2("Erstelle dein zyklusbasiertes Training")
textblock("Plane gezielt und passend zu deiner aktuellen Phase – Phasely hilft dir dabei.")

# Button und Session-State für Anzeige
colleft, col1, colright = st.columns(3)
with col1:
    button("show_trainingsplanung", "✨ Zyklusbasierte Trainingswoche erstellen ✨")
    button("show_zyklusuebersicht", "Deine Zyklusübersicht")

if st.session_state["show_trainingsplanung"]:
    show_trainingsplanung()
    button("show_match_scores", "Matched dein Training zu deiner Phase?")
    if st.session_state["show_match_scores"]:
        show_match_scores()
