# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 22:10:14 2021

@author: PC GAMER
"""
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import chart_studio.plotly as plotly
import plotly.figure_factory as ff
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from fbprophet.plot import add_changepoints_to_plot
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt 
from prophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation


@st.cache
def load_data_finance(ticker, START, TODAY):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data	


# Plot raw data
def plot_raw_data(data):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
    

       

def main():
    
           # col1,col2=st.columns(2) 
        #    with col1:
                
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    stock=("google","apple",'Microsoft Corporation','Fluor',"Gold ",'Crude Oil','International Paper Company','euro','blé','café',"argent",'cuivre')

    selected_stock = st.selectbox('Select dataset for prediction', stock)
            
    stocks = ('GOOG', 'AAPL', 'MSFT','FLR','GC=F','CL=F','IP','USDEUR=X','WEAT','CAFE','ARD.AX','HG=F')
    for i in stock:
        x=stock.index(selected_stock)
            
    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365
	
    data_load_state = st.text('Loading data...')
    data =load_data_finance(stocks[x], START, TODAY)
    data_load_state.text('Loading data... done!')

    st.header('Raw data')
    if st.checkbox("show row data"):
        
        st.write(data.tail())
    st.header('Plot Actual data')
    if st.checkbox("Show plot data "):
        plot_raw_data(data)

                # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

                # Show and plot forecast
    st.header('Forecast data')
    if st.checkbox("Show forcast data "):
        st.write(forecast())
    
    st.header(f'Forecast plot for {n_years} years')
    
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.header("Forecast components")
    if st.checkbox(" show Forecast components "):
        
        fig2 = m.plot_components(forecast)
        st.write(fig2)
                
"""    
            with col2:
                st.write("Ajoutez des valeurs from Yahoo Finance")
                
                value = st.text_area("Value",stock)
                symbol=st.text_input(" Symbole",stocks)  
                if value is not  None:
                    if symbol is not None:
                        if st.button("Ajouter"): 
                            stock = stock + value
                            stocks = stocks + symbol
            
        
 
"""
 
    
 
    
 
    
 
    
 
    
 
    
 