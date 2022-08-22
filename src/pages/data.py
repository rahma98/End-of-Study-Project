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

import investpy

   

@st.cache(allow_output_mutation=True)
def load_data_sma(tt, START, TODAY):
    data =investpy.get_stock_historical_data(stock=tt,
                                        country='Tunisia',
                                        from_date= START,
                                        to_date= TODAY)
    data.reset_index(inplace=True)
    return data	

@st.cache
def load_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    return data


@st.cache(allow_output_mutation=True)
def run_ema_data(stk, STR, TOD):
    dF =investpy.get_stock_historical_data(stock=stk, country='Tunisia', from_date= STR, to_date= TOD)
    dF.reset_index(inplace=True)
    return dF



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
    
    


    
def plot_fig(data):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data.dateHisto, y=data['openvalue'], name="stock_open",line_color='deepskyblue'))
	fig.add_trace(go.Scatter(x=data.dateHisto, y=data['closevalue'], name="stock_close",line_color='dimgray'))
	fig.layout.update(title_text='Time Series data with Rangeslider',xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	return fig
def plot_fig_SMA(data,sma30,sma100):
                fig=go.Figure()
                fig.add_trace(go.Scatter(x=data.Date, y=data['Close'], name="open value"))
                fig.add_trace(go.Scatter(x=data.Date, y=sma30['Close'], name="sma30"))    
                fig.add_trace(go.Scatter(x=data.Date, y=sma100['Close'], name="sma100"))
                fig.layout.update(title_text='Trading ', xaxis_rangeslider_visible=True)
                st.plotly_chart(fig)
 
# Plot raw data
def plot_raw_data_tun(data):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
    
@st.cache
def load_data_tun(ticker, START, TODAY):
    data =investpy.get_stock_historical_data(stock=ticker,
                                        country='Tunisia',
                                        from_date= START,
                                        to_date= TODAY)
    data.reset_index(inplace=True)
    return data	

	

                
#def plot_buysell(data,sma30,sma100,df):
 #               fig=go.Figure()
#                fig.add_trace(go.Scatter(x=data.dateHisto, y=data['closevalue'], name="open value"))
 #               fig.add_trace(go.Scatter(x=data.dateHisto, y=sma30['closevalue'], name="sma30"))    
  #              fig.add_trace(go.Scatter(x=data.dateHisto, y=sma100['closevalue'], name="sma100"))
#
 #               fig.add_trace(go.Scatter(df.index, df.sigPriceBuy,label='Buy',marker='^',color='green'))
  #              fig.add_trace(go.Scatter(df.index, df.sigPriceSell,label='Sell',marker='v',color='red'))
   #             fig.layout.update(title_text='buy & sell ', xaxis_rangeslider_visible=True)
    #            st.plotly_chart(fig)            

def main():
    
    
    
    

        
        graph_type = st.sidebar.selectbox("Choix", ["High-frequency trading(ML)", "algorithmic trading(EMA)" ,"algorithmic trading(SMA)"])



        if graph_type == "High-frequency trading(ML)":
            st.title('Stock Market Forecast with Machine Learning Algorithms')
            START = "01/01/2015"
            TODAY= "01/01/2030"
            dataset = ('BIAT','UIB','BT','BNA','BH','SFBT','BHASS','AMI','TLS','ATB','MGR','MNP','BTEI','AL','ARTES','TAIR','SITS','ASSAD','ATL','TINV','SIPHA','TVAL')
            selected_stock = st.selectbox('Select dataset for prediction', dataset)

            data_load_state = st.text('Loading data...')
            data = load_data_tun(selected_stock, START, TODAY)
            data_load_state.text('Loading data... done!') 
            
            year = st.slider('Year of prediction:',1,4)
            period = year * 365

            st.header('Row data')
            if st.checkbox('Show raw data'):
                st.subheader('Raw data')
                st.write(data)
        
            # plotting the figure of Actual Data
            st.header("plotting the figure of Actual Data")
            if st.checkbox('show plotting the figure of Actual Data:'):
                plot_raw_data_tun(data)
    
            # preparing the data for Facebook-Prophet.
            #col1,col2= st.columns(2)
            data_pred = data[['Date','Close']]
            data_pred=data_pred.rename(columns={"Date": "ds", "Close": "y"})

            # code for facebook prophet prediction

            m = Prophet()
            m.fit(data_pred)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)
            
            #plot forecast

            fig1 = plot_plotly(m, forecast)

                        
            st.header(f'Forecast plot for {year} years')
            st.plotly_chart(fig1)
            if st.checkbox('Show forecast data'):
                        st.subheader('forecast data')
                        st.write(forecast)                    

                

                

            #plot component wise forecast
            st.header("Component wise forecast")
            if st.checkbox('Show Component wise forecast'):
                fig2 = m.plot_components(forecast)
                st.write(fig2)
        
            #plot component wise forecast
            st.header("Change points component")
            if st.checkbox('Show the plot of Change points component'):
                fig3 = m.plot(forecast)
                a = add_changepoints_to_plot(fig3.gca(), m, forecast)
                st.write(fig3)
            
            
           # search_result = investpy.search_quotes(text=selected_stock , products=['stocks'],
              #                         countries=['tunisia'], n_results=1)
            #st.write(search_result)
           # technical_indicators = search_result.retrieve_technical_indicators(interval='daily')
            #st.write(technical_indicators)
            
           # x=investpy.news.economic_calendar()
           # st.write(x)
            
            
        if graph_type == "algorithmic trading(EMA)":
            
            st.title("Trading method with Exponential Moving Average (EMA)")
            START = "01/01/2015"
            TODAY= "01/01/2030"
            dataset = ('BIAT','UIB','BT','BNA','BH','SFBT','BHASS','AMI','TLS','ATB','MGR','MNP','BTEI','AL','ARTES','TAIR','SITS','ASSAD','ATL','TINV','SIPHA','TVAL')
            selected_stock_ema = st.selectbox('Select dataset for prediction', dataset)

            data_load_state = st.text('Loading data...')
            data =run_ema_data(selected_stock_ema, START, TODAY)
            data_load_state.text('Loading data... done!')
            

            for i in ['Open', 'High', 'Low', 'Close','Volume']:
                    data[i] = data[i].astype('float64')
            avg_20 = data.Close.rolling(window=20, min_periods=1).mean()
            avg_50 = data.Close.rolling(window=50, min_periods=1).mean()
            avg_200 = data.Close.rolling(window=200, min_periods=1).mean()
            set1 = { 'x': data.Date, 'open': data.Open, 'close': data.Close, 'high': data.High, 'low': data.Low, 'type': 'candlestick',}
            set2 = { 'x': data.Date, 'y': avg_20, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'MA 20 periods'}
            set3 = { 'x': data.Date, 'y': avg_50, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'yellow' },'name': 'MA 50 periods'}
            set4 = { 'x': data.Date, 'y': avg_200, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'black' },'name': 'MA 200 periods'}
            data = [set1, set2, set3, set4]
            fig = go.Figure(data=data)
            st.plotly_chart(fig)
            
            st.header('information ')
            
            search_result = investpy.search_quotes(text=selected_stock_ema , products=['stocks'],
                                       countries=['tunisia'], n_results=1)
        
            information = search_result.retrieve_information()
            df=pd.Series(information).to_frame()
            df.to_csv("assets/information.csv") 
            fb=pd.read_csv('assets/information.csv')
            st.dataframe(fb)
        

            
            
         
        if graph_type == "algorithmic trading(SMA)":
            st.title("Trading method with Moving Average Analysis (MA)")
            START = "01/01/2015"
            TODAY= "01/01/2030"
            dataset = ('BIAT','UIB','BT','BNA','BH','SFBT','BHASS','AMI','TLS','ATB','MGR','MNP','BTEI','AL','ARTES','TAIR','SITS','ASSAD','ATL','TINV','SIPHA','TVAL')
            selected_stock_sma = st.selectbox('Select dataset for prediction', dataset)

            
            data_load_state = st.text('Loading data...')
            data =  load_data_sma(selected_stock_sma, START, TODAY)
            data_load_state.text('Loading data... done!')
            
            

            sma30 = pd.DataFrame()
            sma30['Close'] = data['Close'].rolling(window=30).mean()
            sma100 = pd.DataFrame()
            sma100['Close'] = data['Close'].rolling(window=100).mean()
            plot_fig_SMA(data,sma30,sma100)
            
            df = pd.DataFrame()
            df['data'] = data['Close']
            df['SMA30'] = sma30['Close']
            df['SMA100'] = sma100['Close'] 
            
            def buy_sell(df):
                    sigPriceBuy=[]
                    sigPriceSell=[]
                    flag=-1


                    for i in range(len(df)):
                        if df['SMA30'][i]>df['SMA100'][i]:
                            if flag != 1:
                                sigPriceBuy.append(df['data'][i])
                                sigPriceSell.append(np.nan)
                                flag=1
                            else:
                                sigPriceBuy.append(np.nan)
                                sigPriceSell.append(np.nan)
                        elif df['SMA30'][i]<df['SMA100'][i]:
                            if flag != 0 :
                                sigPriceBuy.append(np.nan)
                                sigPriceSell.append(df['data'][i])
                                flag = 0
                            else:
                                sigPriceBuy.append(np.nan)
                                sigPriceSell.append(np.nan)
                        else:
                            sigPriceBuy.append(np.nan)
                            sigPriceSell.append(np.nan)


                    return(sigPriceBuy,sigPriceSell)
                
            buy_sell = buy_sell(df)
            df['Close'] = buy_sell[0]
            df['Close'] = buy_sell[1]
            
            data_sma = investpy.moving_averages(name=selected_stock_sma , country='tunisia', product_type='stock', interval='daily')
            st.table(data_sma)
            st.header('pivot points')
            pivot_point = investpy.pivot_points(name=selected_stock_sma, country='tunisia', product_type='stock', interval='daily')
            st.write(pivot_point)
            
            st.header('technical indicators')
            tech = investpy.technical_indicators(name= selected_stock_sma ,country='tunisia', product_type='stock', interval='daily')
            st.write(tech)
      #      plot_buysell(data,sma30,sma100,df)
              
            
   