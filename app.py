import streamlit as st
import requests
import json

st.title('CS:GO Skin Price Checker')

# replace these with the app ID and name of the game you want to get prices for
APP_ID = '730'
GAME_NAME = 'Counter-Strike: Global Offensive'

# list of available weapon types
weapon_types = [
    "AK-47",
    "M4A4",
    "AWP",
    "Glock-18",
    "USP-S",
    "P2000",
    "Desert Eagle",
    # add more weapon types here
]

# create a dropdown for weapon type and prompt user for item name
weapon_type = st.selectbox("Select weapon type:", weapon_types)
item_name = st.text_input("Enter item name: ")

if st.button("Get Prices"):
    # retrieve the current price of an item
    item_names = [
        f'{weapon_type} | {item_name} (Battle-Scarred)',
        f'{weapon_type} | {item_name} (Well-Worn)',
        f'{weapon_type} | {item_name} (Field-Tested)',
        f'{weapon_type} | {item_name} (Minimal Wear)',
        f'{weapon_type} | {item_name} (Factory New)'
    ]

    # loop through item names and retrieve prices
    for item_name in item_names:
        url = f'https://steamcommunity.com/market/priceoverview/?appid={APP_ID}&currency=1&market_hash_name={item_name}'
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            if data['success']:
                if 'lowest_price' in data:
                    price = data['lowest_price']
                    st.write(f'{item_name}: {price}')
                else:
                    st.write(f'No steam listings found for {item_name}')
            else:
                st.write(f'Failed to retrieve price for {item_name}')
        else:
            st.write('Failed to connect to Steam Community Market')

