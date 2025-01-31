import streamlit as st
import sys
import os 
sys.path.append(os.pardir)
sys.path.append(os.path.join(os.pardir, os.pardir))
from src.Data_Transform.data_fetching import get_network_data,get_network_by_country,get_network_data_for_average
from src.Data_Metrics.data_visulization import plot_station_count, generate_summary_stats,pie_chart_by_country
from src.exception import CustomeException
from src.loggers import logging
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd

def show_dashboard():

  try:
    st.set_page_config(page_title="City Bike Sharing", page_icon="🧊",
     layout="centered",
     initial_sidebar_state="expanded")

    st.title("""City Bike Sharing Network Dashboard""")
    
   
    average_processed_data = get_network_data()
    processed_data=get_network_data_for_average()
    network_by_country_data=get_network_by_country()

    
    st.subheader('Number of Stations by Network',divider=True)
    plt= plot_station_count(processed_data)
    st.pyplot(plt)
    
    
    st.subheader('Average Stations by Country',divider=True)
    average_data = generate_summary_stats(average_processed_data)
    print(average_data)
    df=pd.DataFrame(average_data)
    st.write(df)
    

    
    st.subheader('Additional Insights',divider=True)
    st.write(f"Total number of networks: {len(processed_data)}")

    country_with_most = average_data.idxmax()
    st.write(f"Country with the highest number of stations: {country_with_most}")

    largest_network = max(processed_data, key=lambda x: x['station_count'])
    st.write(f"Network with largest number of stations: {largest_network['name']} with {largest_network['station_count']} stations")
    
    st.subheader('Network Distribution by Country',divider=True)
    pie_chart_by_country(network_by_country_data)
    

    
    
    
  
  except Exception as e:
            raise CustomeException(e,sys) 

if __name__ == "__main__":
    show_dashboard()