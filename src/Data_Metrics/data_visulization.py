import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('TkAgg')
from src.exception import CustomeException
from src.loggers import logging
import sys
import pycountry
#matplotlib.use('TkAgg')

# Create the main window




def plot_station_count(processed_data):
 try:  
    df=pd.DataFrame(processed_data)
    x=df['name']
    y=df['Station count']  
    plt.bar(x, y, color ='skyblue',
        align='center', width=0.3) 
    plt.xticks(rotation=60, fontsize = 'small')
    plt.xlabel('Name of Network')
    plt.ylabel('Number Of Stations')
    plt.title('City Bike Sharing Networks by Number of Stations')
    logging.info("Done with plot_station_count")
    return plt
 except Exception as e:
            raise CustomeException(e,sys)



def generate_summary_stats(processed_data):
   
    
    df = pd.DataFrame(processed_data)
    data = df.groupby('Country name')['Station count'].mean()
    logging.info("Done with generate_summary_stats")
    return data 
    
     



def pie_chart_by_country(processed_data):
  try: 
    
    data = pd.DataFrame(processed_data)
    df = pd.DataFrame(data, columns=["name", "city", "country","Country name"])
    print(df)
    country_distribution = df['Country name'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(country_distribution.values, labels=country_distribution.index,
           autopct='%.0f%%',
          wedgeprops={"linewidth" : 2.0, "edgecolor": "white"},
         textprops={'size': 'xx-large'})
    ax.set_title("Networks with respect to Country")
  

    #plt.tight_layout()

    #plt.legend(labels=country_distribution.index, loc='best')
   
    logging.info("Done with pie_chart_by_country")
    st.pyplot(plt)
    

  except Exception as e:
            raise CustomeException(e,sys)  
  
def  get_country_name(country_code):
 
  
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name if country else country_code
     
     