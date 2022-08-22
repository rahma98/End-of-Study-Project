
import streamlit as st
from PIL import Image
import gettext

def main():
    #st.set_page_config(layout="wide")
    st.title("Intelligent Stock Exchange System ")
    st.write("""####    This web application will be used to analyze, visualize the variation of the stock market data based on machine learning, web scraping and Natural language processing algorithms.""")
    image = Image.open("assets/th.JPG")
    st.image(image,width=1500, use_column_width=None)


         
    with st.expander("Métrique"):
        st.latex(r"""
         MAPE=\frac{1}{m} \sum _{i=1}^{m} \vert \frac{y^{i}-\hat{y}^{i}}{y^{i}} \vert     """)
         
        st.write("MAPE (Mean Absolute Percentage Error) également appelée écart en pourcentage absolu moyen, est une mesure de la précision de prédiction d’une méthode de prévision en statistique ,par exemple dans l’ estimation de tendance , également utilisée comme fonction de perte pour les problèmes de régression dans l’apprentissage machine")
        st.warning("MAPE > 20% is Bad")
        st.info("MAPE < 20% is Good")
        st.success("MAPE < 10% is Excellent")
        
 