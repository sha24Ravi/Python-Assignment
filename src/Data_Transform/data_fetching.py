import sys
import os
import asyncio
import aiohttp
sys.path.append(os.pardir)
sys.path.append(os.path.join(os.pardir, os.pardir))
import requests
import json
import pandas as pd

from dataclasses import dataclass
from src.exception import CustomeException
from src.loggers import logging
from flask import Flask, render_template, jsonify, request
from aiohttp import ClientResponseError
import pycountry


    
def fetch_data():
        url = 'http://api.citybik.es/v2/networks'
        headers = {'user-agent': 'my-app/0.0.1'}
        data = requests.get(url, headers=headers)
        return data.json().get('networks',[])
        
        


def fetch_all_station_data(network_ids):

 url = f"https://api.citybik.es/v2/networks/{network_ids}"
 response=requests.get(url)
 print(response.text)
 data=response.json()
 return data

 

    
def read_network_ids_from_csv(file_path):
 try:
    df = pd.read_csv(file_path,nrows=10)
    network_id=[]
    network_id= df['id'].tolist()
    logging.info("read the first 10 network Ids from the Csv file")
    return network_id
 except Exception as e:
            raise CustomeException(e,sys)
    

async def fetch_network_data(session, network_id):
    url = f"https://api.citybik.es/v2/networks/{network_id}"
    try:
        async with session.get(url) as response:
            response.raise_for_status()  
            data = await response.json()
            logging.info("Return the 'network' part of the response")
            return data.get('network')  
    except aiohttp.ClientError as e:
        print(f"Error fetching data for {network_id}: {e}")
        raise CustomeException(e,sys)
        


async def fetch_all_network_data():
  try:  
    network_ids = read_network_ids_from_csv("src/data/city_bike.csv")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_network_data(session, network_id) for network_id in network_ids]
        results = await asyncio.gather(*tasks)  # Run tasks concurrently
        return [result for result in results if result]  # Filter out None results
  except Exception as e:
            raise CustomeException(e,sys) 


def get_network_for_country(data):
   
 try: 
   processed_networks = []
   for network in data:
            # Extracting the essential details
            network_name = network['name']
            city = network['location']['city']
            country = network['location']['country']  
            

            processed_networks.append({
                'name': network_name,
                'city': city,
                'country': country,
                
            })
   logging.info("Extracting the essential newtwork details with respect to Country from the API response")          
   return processed_networks
 except Exception as e:
            raise CustomeException(e,sys)
 

def cal_station_count(processed_data):    
 try:  
    processed_networks = []
    for network in processed_data:
        try:
            # Extracting the essential details
            network_name = network['name']
            city = network['location']['city']
            country = network['location']['country']
            latitude = network['location']['latitude']
            longitude = network['location']['longitude']
            station_count = len(network['stations'])  # Number of stations

            # Adding the data to a list
            processed_networks.append({
                'name': network_name,
                'city': city,
                'country': country,
                'latitude': latitude,
                'longitude': longitude,
                'station_count': station_count,
            })
           
        except Exception as e:
            raise CustomeException(e,sys)
    
    logging.info("Extracting the essential details from the API response with respect each ID")
    return  processed_networks 
   
 except Exception as e:
            raise CustomeException(e,sys)




def get_network_data():
 try: 
     all_network_data = asyncio.run(fetch_all_network_data())
     station_data=cal_station_count(all_network_data)
     if station_data:
       df=pd.DataFrame(station_data)
       df['country_name'] = df['country'].apply(get_country_name)
       print(df)
       return df
 except Exception as e:
            raise CustomeException(e,sys)  


def  get_network_data_for_average():
    try: 
     all_network_data = asyncio.run(fetch_all_network_data())
     station_data=cal_station_count(all_network_data)
     if station_data:
       return station_data
    except Exception as e:
            raise CustomeException(e,sys)  

def get_network_by_country(): 
 try: 
     file_path="src/data/network_country.csv"
     df = pd.read_csv(file_path,nrows=9)
     df['country_name'] = df['country'].apply(get_country_name)
     return df
 except Exception as e:
            raise CustomeException(e,sys)    


def get_country_name(country_code):
    
        return pycountry.countries.get(alpha_2=country_code).name

def save_data():
    try:    
        processed_data=fetch_data()
        processed_df=get_network_for_country(processed_data)
        df = pd.DataFrame(processed_df)
        df.to_csv('data/network_country.csv',index=False,header=True)
        logging.info("Network and Country Data Saved Succesfully")
        
    except Exception as e:
            raise CustomeException(e,sys)   
    



    


