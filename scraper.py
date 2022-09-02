import requests
import pandas as pd
from typing import List
import time
from requests.models import to_key_val_list
import os


def load(directory: str) -> dict:
    if os.path.exists(directory):
        df = pd.read_csv(directory, dtype=str)
        columns = df.columns.tolist()
        data = {}

        # Sets the corresponding columns in dict
        # and its list of values
        for column in columns:
            data[column] = list(df[column])
        return data


#Set the CSV like a DataFrame
db = load('DataBaseStickers.csv')


for i in range(len(db['Adesivo'])):

    #Take all Stickers Names and format to url type
    nameOfStickers =  db["Adesivo"][i]
    nameOfStickersFormated = db["Adesivo"][i].replace(" ",'%20').replace("|",'%7C').replace("(",'%28').replace(")",'%29')
    url = f'https://steamcommunity.com/market/priceoverview/?country=BR&currency=7&appid=730&market_hash_name=Sticker%20%7C%20{nameOfStickersFormated}'
    
    #Search the url with json and take the prices
    Valuess = requests.get(url).json()
    Price = Valuess['lowest_price']
    newPrice = Price[3:]
    newPrice = newPrice.replace('.', ',')
    print(f'{nameOfStickers} R${db["Preco Hoje"][i]} --> R${newPrice} ')
    print('-'*10)

    #Change the prices in the CSV
    list = db['Preco Hoje']
    list[i] = newPrice
    df = pd.DataFrame(db)
    df.to_csv('DataBaseStickers.csv', index=False)
    
    #Timer to dont get banned of Steam Market
    time.sleep(10)