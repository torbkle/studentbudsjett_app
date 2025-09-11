import streamlit as st

def vis_infoboks(tittel, verdi, ikon="ℹ️", farge="blue"):
    st.markdown(
        f"""
        <div style='padding:10px;border-radius:8px;background-color:{farge};color:white'>
            <h4>{ikon} {tittel}</h4>
            <p style='font-size:20px'>{verdi}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
