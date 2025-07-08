"""
interface_components.py

Enthält wiederverwendbare UI-Komponenten für die Phasely App, 
darunter Überschriften, Textblöcke, Score-Anzeigen, Infokarten und Buttons.
"""

import streamlit as st
from src.globals import get_color_palette


def h1(heading_text: str):
    """Große zentrierte Überschrift (H1) im Inter-Design."""
    st.markdown(f"""
        <h1 style="text-align: center; font-family: 'Inter', sans-serif; color: black; width: 50vw; margin:auto;">
            {heading_text}
        </h1>
    """, unsafe_allow_html=True)


def h2(heading_text: str):
    """Zentrierte Zwischenüberschrift (H2)."""
    st.markdown(f"""
        <h2 style="text-align: center; font-family: 'Inter', sans-serif; color: black; width: 50vw; margin-top:30px; margin:auto;">
            {heading_text}
        </h2>
    """, unsafe_allow_html=True)


def h3(heading_text: str):
    """Zentrierte Überschrift (H3) mit Abstand."""
    st.markdown(f"""
        <h3 style="text-align: center; font-family: 'Inter', sans-serif; color: black; width: 50vw; margin-top:50px; margin:auto;">
            {heading_text}
        </h3>
    """, unsafe_allow_html=True)


def h4(heading_text: str):
    """Kleine Abschnittsüberschrift (H4)."""
    st.markdown(f"""
        <h4 style="font-family: 'Inter', sans-serif; color: black; margin-top:30px;">
            {heading_text}
        </h4>
    """, unsafe_allow_html=True)


def textblock(text: str):
    """Zentrierter Fließtext-Block mit dezenter Formatierung."""
    st.write(f"""
        <p style="text-align: center; font-family: 'Inter', sans-serif; color: black; width: 40vw; margin-top: 20px; margin:auto;">
            {text}
        </p>
    """, unsafe_allow_html=True)


def view_score_percentage(score: float, label: str, score_color: str):
    """
    Visualisiert einen Score als große Prozentzahl mit beschriftetem Label.

    Args:
        score (float): Score-Wert von 0.0 bis 1.0.
        label (str): Beschriftung unter der Zahl.
        score_color (str): Farbe der Prozentzahl.
    """
    st.markdown(f"""
        <div style="text-align: center; font-family: 'Inter', sans-serif;">
            <div style="font-size: 40px; font-weight: bold; color: {score_color}; margin-top: 20px;">
                {int(score * 100)}%
            </div>
            <div style="margin-bottom: 8px;">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def info_card(heading_text: str, info_text: str):
    """
    Info-Karte mit Titel und erklärendem Textblock.

    Args:
        heading_text (str): Überschrift.
        info_text (str): Fließtext.
    """
    st.markdown(f"""
        <div style="
            background-color: #F2F3F8;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            font-family: 'Inter', sans-serif;
            color: black;
            height: 100%;
            margin-top: 80px;
            margin-bottom: 40px;
            text-align: left;
        ">
            <h4 style="color: black; margin-top:0px;">{heading_text}</h4>
            <p style="font-size: 16px; line-height: 1.6;">
                {info_text}
            </p>
        </div>
    """, unsafe_allow_html=True)


def button(key: str, label: str):
    """
    Button-Komponente mit zugehörigem Session-State Key.

    Args:
        key (str): Key im st.session_state.
        label (str): Beschriftung auf dem Button.
    
    Beispiel:
        if st.session_state["mein_key"]:
            ...
    """
    if key not in st.session_state:
        st.session_state[key] = False

    if st.button(label):
        st.session_state[key] = True
