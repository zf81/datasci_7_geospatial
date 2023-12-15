import requests 
import urllib.parse
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("GCP_API_KEY")

df = pd.read_csv("https://raw.githubusercontent.com/hantswilliams/HHA_507_2023/main/WK7/assignment7_slim_hospital_coordinates.csv")

df['GEO'] = df['X'].astype(str) + ',' + df['Y'].astype(str)

df_s = df.sample(100)

google_response = []

for coord in df_s['GEO']: 

    location_raw = coord
    location_clean = urllib.parse.quote(location_raw)

    reverse_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
    step1 = reverse_geocode_url + location_clean + '&key=' + API

    response = requests.get(step1)
    response_dictionary = response.json()

    address = response_dictionary['results'][0]['formatted_address']


    final = {'address': address, 'coordinates': coord}
    google_response.append(final)

    print(f'....finished with {coord}')

df_add = pd.DataFrame(google_response)

df_add.to_csv('reverse_geocoding.csv')