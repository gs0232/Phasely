import streamlit as st
import pandas as pd
from src.classes import User
from src.data_setup import load_data
from src.interface_components import h1, textblock


# Seitenkonfiguration
st.set_page_config(page_title="Phasely | Start", layout="wide", initial_sidebar_state="collapsed")

# --- STARTSCREEN ---
def show_startscreen():
    """
    Zeigt den Startbildschirm, um Namen, Alter und CSV-Datei zu erfassen.
    Speichert alles in `st.session_state`.
    """

    h1("Willkommen bei Phasely")
    textblock("👋 Bevor es losgeht, sag uns kurz deinen Namen, dein Alter und lade deine Zyklusdaten hoch.")

    # Abstand eifügen
    st.markdown("<br>", unsafe_allow_html=True)
    # Formular für Eingaben
    colleft, col1, colright = st.columns([3, 6, 3])
    with col1:
        with st.form("user_form"):
            name = st.text_input("Vorname", placeholder="z. B. Heidi")
            age = st.number_input("Alter", min_value=10, max_value=100, value=25, step=1)
            uploaded_file = st.file_uploader("Zyklus-Tracking CSV-Datei", type=["csv"])
            submitted = st.form_submit_button("Daten hochladen")

        if submitted:
            if not name or not uploaded_file:
                st.warning("Bitte gib deinen Namen ein und lade eine CSV-Datei hoch.")
                return

            # CSV laden
            user_data = pd.read_csv(uploaded_file)

            # User-Objekt erstellen und speichern
            user = User(user_id=1, user_name=name, user_age=age)
            user.assign_user_data(user_data)

            # Session-State speichern
            st.session_state.current_user = user
            st.session_state.main_data = user_data
            st.session_state.has_started = True

            st.success("Daten erfolgreich geladen! Du kannst jetzt zur App wechseln.")

            if st.button("Weiter zu deinem Dashboard"):
                st.switch_page("00_Dashboard.py")

# --- MAIN ---
if "has_started" not in st.session_state:
    st.session_state.has_started = False

if not st.session_state.has_started:
    show_startscreen()
else:
    st.switch_page("00_Dashboard.py")
