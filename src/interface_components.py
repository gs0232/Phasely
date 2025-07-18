import streamlit as st
from src.globals import (colors)

def h1(heading_text):
    '''
    H1 Component. Put in desired text and/or variable.
    '''
    st.markdown(f"""
    <h1 style="text-align: center; font-family: 'Inter', cursive; color: black; width: 50vw; margin:auto;">
        {heading_text}
    </h1>""", unsafe_allow_html=True)

def h2(heading_text):
    '''
    H2 Component. Put in desired text and/or variable.
    '''
    st.markdown(f"""
    <h2 style="text-align: center; font-family: 'Inter', cursive; color: black; width: 50vw; margin-top:30px; margin-right:auto; margin-left: auto;">
        {heading_text}
    </h2>""", unsafe_allow_html=True)

def h3(heading_text):
    '''
    H3 Component. Put in desired text and/or variable.
    '''
    st.markdown(f"""
    <h3 style="text-align: center; font-family: 'Inter', cursive; color: black; width: 50vw; margin-top:50px; margin-right:auto; margin-left: auto;">
        {heading_text}
    </h3>""", unsafe_allow_html=True)

def h4(heading_text):
    '''
    H4 Component. Put in desired text and/or variable.
    '''
    st.markdown(f"""
    <h4 style="font-family: 'Inter', cursive; color: black; margin-top:30px;">
        {heading_text}
    </h4>""", unsafe_allow_html=True)

def textblock(text):
    '''
    P-Text Component. Put in desired text and/or variable.
    '''
    st.write(f"""
        <p style="text-align: center; font-family: 'Inter'; color: black; width: 40vw; margin-top: 20px; margin-right:auto; margin-left: auto;">
            {text}
        </p>""", unsafe_allow_html=True)

def view_score_percentage(score, text, score_color):
    '''
    Block Component. Shows the percentage on top and the text underneath.

    Should be used in columns!
    '''
    st.markdown(f"""
        <div style="text-align: center; font-family: 'Inter', sans-serif;">
            <div style="font-size: 40px; font-weight: bold; color: {score_color}; margin-top: 20px;">{int(score * 100)}%</div>
            <div style="margin-bottom: 8px;">{text}</div>
        </div>
        """, unsafe_allow_html=True)

def info_card(heading_text, info_text):
    '''
    Card Component. Views a heading with text underneath. Has a background-color.

    Should be used in columns!
    '''
    st.markdown(f"""
        <div style="
            background-color: #F2F3F8;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            font-family: 'Inter', sans-serif;
            color: black;
            height: 100%;
            margin-top: 40px;
            margin-bottom: 40px;
            text-align: left;
        ">
            <h4 style="color: black; margin-top:0px"; margin-bottom:0px;>{heading_text}</h4>
            <p style="font-size: 16px; line-height: 1.6;">
                {info_text}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
def button(key:str, button_text:str):
    '''
    Button-Component + session configuration. 
    
    --> Add action underneath:

        if st.session_state[key]:
            action
    

    Cannot be styled with HTML.
    Can be put in columns.
    '''
    if key not in st.session_state:
        st.session_state[key] = False

    if st.button(button_text):
        st.session_state[key] = True
