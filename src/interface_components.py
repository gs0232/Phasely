import streamlit as st

def h1(text):
    '''
    H1 Component. Put in desired text or variable.
    '''
    st.markdown(f"""
    <h1 style="text-align: center; font-family: 'Inter', cursive; color: black;">
        {text}'s Phasely Dashboard
    </h1>""", unsafe_allow_html=True)