import streamlit as st
from src.globals import (
    MAIN_FILE_PATH, SPORT_SESSIONS_PATH, main_data,
    sport_sessions, strength_sessions, cardio_sessions, low_impact_sessions,
    cycle_phases, current_index, current_user, current_phase
)
from pages.trainingsplanung import show_trainingsplanung
from pages.zyklusuebersicht import show_zyklusuebersicht
from src.interface_components import h1

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

h1(current_user.user_name)
st.markdown(f"""
    <h1 style="text-align: center; font-family: 'Inter', cursive; color: black;">
        {current_user.user_name}'s Phasely Dashboard
    </h1>""", unsafe_allow_html=True)

colleft, col1, colright = st.columns([3, 6, 3])

with col1:
    st.write(f"""
        <p style="text-align: center; font-family: 'Inter', cursive; color: black;  margin-top: 20px;">
            Willkommen zu deinem Phasely Dashboard! Hier Hier bekommst du reichlich Infos über deine Zyklusphasen und die optimale Trainingsgestaltung während dieser Phasen. Du kannst sogar Sporteinheiten auswählen und sehen, wie gut sie zu deiner aktuellen Phase passen. Viel Spaß!
        </p>""", unsafe_allow_html=True)

    st.markdown(f"""<hr style="border: none; height: 2px; background: #00000010; margin-bottom: 10px">""", unsafe_allow_html=True)

    # Aktuelle Phase Anzeige
    st.markdown(f"""
        <h2 style="text-align: center; font-family: 'Inter', cursive; color: black; margin-top: 30px;">
            Du bist in deiner <span style="color: {primary_color};">{current_phase.phase_name}</span>
        </h2>""", unsafe_allow_html=True)

    st.write(f"""
        <p style="text-align: center; font-family: 'Inter';">
            {current_phase.description}
        </p>""", unsafe_allow_html=True)

# Titel für Trainingsverteilung
st.markdown(f"""
<h3 style="text-align:center; font-family:'Inter'; margin-top:30px; margin-bottom: 10px; margin-top: 40px;">
    Optimale Trainingsverteilung
</h3>
""", unsafe_allow_html=True)

# Kraft, Ausderung und Low-Impact Score Anzeige
colleft, col1, col2, col3, colright = st.columns([2, 1, 1, 1, 2])

with col1:
    st.markdown(f"""
    <div style="text-align: center; font-family: 'Inter', sans-serif;">
        <div style="font-size: {score_font_size}; font-weight: bold; color: {primary_color}; margin-top: 20px;">{current_phase.strength_score * 100}%</div>
        <div style="margin-bottom: 8px;">Krafttraining</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align: center; font-family: 'Inter', sans-serif;">
        <div style="font-size: {score_font_size}; font-weight: bold; color: {primary_color}; margin-top: 20px;">{current_phase.cardio_score * 100}%</div>
        <div style="margin-bottom: 8px;">Ausdauertraining</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="text-align: center; font-family: 'Inter', sans-serif;">
        <div style="font-size: {score_font_size}; font-weight: bold; color: {primary_color}; margin-top: 20px;">{current_phase.low_impact_score * 100}%</div>
        <div style="margin-bottom: 8px;">Low-Impact Training</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)  # etwas Abstand

colleft, col1, col2, colrigth = st.columns([2, 4, 4, 2])

with col1:
    st.markdown("""
    <div style="
        background-color: #F3F3F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        font-family: 'Inter', sans-serif;
        color: #2F2F2F;
        height: 100%;
        margin-top: 40px;
        margin-bottom: 20px;
    ">
        <h4 style="color: #6B705C;">Warum zyklusbasiertes Training?</h4>
        <p style="font-size: 16px; line-height: 1.6;">
            Dein Zyklus beeinflusst Energie, Belastbarkeit und Regeneration. Ein Training, das auf deine jeweilige Phase abgestimmt ist, kann effektiver, nachhaltiger und angenehmer sein.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background-color: #F3F3F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        font-family: 'Inter', sans-serif;
        color: #2F2F2F;
        height: 100%;
        margin-top: 40px;
        margin-bottom: 20px;
    ">
        <h4 style="color: #6B705C;">Wie funktioniert das?</h4>
        <p style="font-size: 16px; line-height: 1.6;">
            Je nach Phase (z. B. Menstruation, Follikelphase) verändern sich Hormone, die dein Training beeinflussen. Phasely passt deine Workouts daran an und unterstützt dich mit datenbasierten Empfehlungen.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Bereich mit Call-to-Action
st.markdown("""
    <h2 style="text-align: center; margin-top: 60px;">Erstelle dein zyklusbasiertes Training</h2>
    <p style="text-align: center; font-size: 16px;">
        Plane gezielt und passend zu deiner aktuellen Phase – Phasely hilft dir dabei.
    </p>
""", unsafe_allow_html=True)

# Button und Session-State für Anzeige
if "show_trainingsplanung" not in st.session_state:
    st.session_state["show_trainingsplanung"] = False

if "show_zyklusuebersicht" not in st.session_state:
    st.session_state["show_zyklusuebersicht"] = False

colleft, col1, col2, colright = st.columns([2, 4, 4, 2])
with col1:
    if st.button("✨ Zyklusbasierte Trainingswoche erstellen ✨"):
        st.session_state["show_trainingsplanung"] = True

with col2:
    if st.button("Deine Zyklusübersicht"):
        st.session_state["show_zyklusuebersicht"] = True

if st.session_state["show_trainingsplanung"]:
    show_trainingsplanung()

if st.session_state["show_zyklusuebersicht"]:
    show_zyklusuebersicht()
