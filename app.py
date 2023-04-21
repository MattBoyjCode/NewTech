import requests
import json
import csv
import streamlit as st

# replace these with the app ID and name of the game you want to get prices for
APP_ID = '730'
GAME_NAME = 'Counter-Strike: Global Offensive'

st.title("CS:GO Skin Price Checker")

# prompt user for weapon type and item name
weapon_type = st.text_input("Enter weapon type (e.g. AK-47, M4A4): ")
item_name = st.text_input("Enter item name: ")

# button for submitting the form
submit_button = st.button("Get Prices")

if submit_button:
    # retrieve the current price of an item
    item_names = [
        f'{weapon_type} | {item_name} (Battle-Scarred)',
        f'{weapon_type} | {item_name} (Well-Worn)',
        f'{weapon_type} | {item_name} (Field-Tested)',
        f'{weapon_type} | {item_name} (Minimal Wear)',
        f'{weapon_type} | {item_name} (Factory New)'
    ]

    # create a list to store the results
    results = []

    # loop through item names and retrieve prices
    for item_name in item_names:
        url = f'https://steamcommunity.com/market/priceoverview/?appid={APP_ID}&currency=1&market_hash_name={item_name}'
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            if data['success']:
                price = data['lowest_price']
                results.append([item_name, price])
                st.write(f'{item_name}: {price}')
            else:
                results.append([item_name, 'Failed to retrieve price'])
                st.write(f'Failed to retrieve price for {item_name}')
        else:
            results.append([item_name, 'Failed to connect to Steam Community Market'])
            st.write('Failed to connect to Steam Community Market')

    # open CSV file for writing
    with open(f'{weapon_type}_{item_name}_prices.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # write header row
        writer.writerow(['Item Name', 'Price'])

        # write results to the CSV file
        for result in results:
            writer.writerow(result)

    st.success("Results saved to CSV file.")
