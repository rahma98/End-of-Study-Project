# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:44:08 2021

@author: PC GAMER
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
import seaborn as sns
import investpy



def plot_fig(data):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data.Date, y=data['Open'], name="stock_open",line_color='deepskyblue'))
	fig.add_trace(go.Scatter(x=data.Date, y=data['Close'], name="stock_close",line_color='dimgray'))
	fig.layout.update(title_text='Time Series data',xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	return fig

@st.cache
def load_data_tun(ticker, START, TODAY):
    data =investpy.get_stock_historical_data(stock=ticker,
                                        country='Tunisia',
                                        from_date= START,
                                        to_date= TODAY)
    data.reset_index(inplace=True)
    return data


def main():

    

    st.title('Dashboard')

    
    START = "01/01/2015"

    TODAY= "01/01/2030"
    stocks=('BIAT','UIB','BT','BNA','BH','SFBT','BHASS','AMI','TLS','ATB','MGR','MNP','BTEI','AL','ARTES','TAIR','SITS','ASSAD','ATL','TINV','SIPHA','TVAL')
    selected_stock_dash = st.selectbox('Select dataset for prediction', stocks)
    
    
    data_load_state = st.text('Loading data...')
    data = load_data_tun(selected_stock_dash, START, TODAY)
    data_load_state.text('Loading data... done!')



    if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(data)
        
        # plotting the figure of Actual Data
    plot_fig(data)
    
        #describe the data 
    if st.checkbox('Show data description'):        
        st.subheader("data description")
        st.write(data.describe())
    #####################################
              # Show Plots
    if st.checkbox('Show corrélation'):               
        st.subheader("corrélation")
        fig_corr, ax = plt.subplots()
        sns.heatmap(data.corr(), ax=ax)
        st.write(fig_corr)
    ########################
    
    st.write("# Data analysis by feature selection :")
    ft=('Close','Open','Volume','High','Low') 
    option_ft = st.selectbox('Select dataset to analyse',ft)
            #################################
    if st.checkbox("show chart bar"):
        st.subheader("chart bar")


        fig = px.bar(x=data["Date"], 
                     y=data[option_ft])
        st.plotly_chart(fig)
    
            ######################
    if st.checkbox("show boxplot"):
        st.subheader("boxplot")
        fig_box = plt.figure()
        box=sns.boxplot(data=data[option_ft])                                                                         
        st.pyplot(fig_box)
    
            ###################################
    if st.checkbox("show density"):
        st.subheader("descriptive statistics summary")
        data['Close'].describe()
    #check the decoration
        des= plt.figure()
        data.columns
        f=sns.distplot(data[option_ft])
        st.pyplot(des)
    
            #######################################
    if st.checkbox("show the frequency"):    
        st.subheader('frequency')
        fig1 = plt.figure()
        freq = sns.countplot(x=data[option_ft])
        st.pyplot(fig1)
 
    
       
        ####################################################################################

         
         
         
         
         
         
         
         
         
         