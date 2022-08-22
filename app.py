import streamlit as st
import src.pages.home
import src.pages.data
import src.pages.contribute
import src.pages.about
import src.pages.dash
import seaborn as sns
from PIL import Image

from os import system, path
import src.pages.international
PAGES = {
    "Home": src.pages.home,
    "Dashboard": src.pages.dash,
    "Prediction": src.pages.data,
    "International": src.pages.international,
    "About": src.pages.about,
    "Key words": src.pages.contribute
}


st.set_page_config( 
    page_title='ISES',
    layout="wide",
    page_icon='💰')

def main():
    #st.set_page_config(layout="wide")
   

    image = Image.open("logo2.jpg")
    st.sidebar.image(image, width=230)


    st.sidebar.title("Menu")
    choice = st.sidebar.radio(" ", list(PAGES.keys()))
    PAGES[choice].main()
    st.sidebar.title("About")
    st.sidebar.info(
        """
        Un cadre de scraping web pour la modélisation du prix des actions en utilisant méthodes d'apprentissage profond.
        """
    )
    st.sidebar.title("Key words")
    st.sidebar.info(" Big data, neural networks, deep learning, web scraping, stock price modelling, time series, NLP")
    
    st.write("      ")
    
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: visible;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)


if __name__ == "__main__":
    main()