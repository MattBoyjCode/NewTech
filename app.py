import streamlit as st
import requests
import json
import pandas as pd

st.title('CS:GO Skin Price Checker')

# replace these with the app ID and name of the game you want to get prices for
APP_ID = '730'
GAME_NAME = 'Counter-Strike: Global Offensive'

# list of available weapon types
weapon_types = [
       "AK-47",
    "M4A4",
    "M4A1-S",
    "Galil AR",
    "FAMAS",
    "AUG",
    "SG 553",
    "AWP",
    "G3SG1",
    "SCAR-20",
    "SSG 08",
    "MAC-10",
    "MP9",
    "MP7",
    "UMP-45",
    "P90",
    "PP-Bizon",
    "Nova",
    "XM1014",
    "MAG-7",
    "M249",
    "Negev",
    "Glock-18",
    "USP-S",
    "P2000",
    "P250",
    "Dual Berettas",
    "Five-SeveN",
    "CZ75-Auto",
    "Desert Eagle",
    "R8 Revolver",
    "Tec-9",
    "Bayonet",
    "Flip Knife",
    "Gut Knife",
    "Karambit",
    "M9 Bayonet",
    "Huntsman Knife",
    "Butterfly Knife",
    "Falchion Knife",
    "Shadow Daggers",
    "Bowie Knife",
    "Ursus Knife",
    "Navaja Knife",
    "Stiletto Knife",
    "Talon Knife",
    "Classic Knife",
    "Paracord Knife",
    "Survival Knife",
    "Nomad Knife",
    "Skeleton Knife",
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
        f'{weapon_type} | {item_name} (Factory New)',
        f'StatTrak™ {weapon_type} | {item_name} (Battle-Scarred)',
        f'StatTrak™ {weapon_type} | {item_name} (Well-Worn)',
        f'StatTrak™ {weapon_type} | {item_name} (Field-Tested)',
        f'StatTrak™ {weapon_type} | {item_name} (Minimal Wear)',
        f'StatTrak™ {weapon_type} | {item_name} (Factory New)'
    ]

    # create an empty DataFrame for displaying the results
    results_df = pd.DataFrame(columns=["Item Name", "Price"])

    # loop through item names and retrieve prices
    for item_name in item_names:
        url = f'https://steamcommunity.com/market/priceoverview/?appid={APP_ID}&currency=1&market_hash_name={item_name}'
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            if data['success']:
                if 'lowest_price' in data:
                    price = data['lowest_price']
                    results_df = results_df.append({"Item Name": item_name, "Price": price}, ignore_index=True)
                else:
                    results_df = results_df.append({"Item Name": item_name, "Price": "No steam listings found"}, ignore_index=True)
            else:
                results_df = results_df.append({"Item Name": item_name, "Price": "Failed to retrieve price"}, ignore_index=True)
        else:
            results_df = results_df.append({"Item Name": item_name, "Price": "Failed to connect to Steam Community Market"}, ignore_index=True)

    # Add custom CSS styles
    custom_css = """
    <style>
        table td:first-child {
            text-align: left;
        }
        .stOrange {
            color: orange;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Replace "StatTrak" with a styled version
    results_df["Item Name"] = results_df["Item Name"].apply(lambda x: x.replace("StatTrak™", "<span class='stOrange'>StatTrak™</span>"))

    # display the results as a table without the index column
    st.write(results_df.to_html(index=False, escape=False, classes=["table", "table-striped", "table-bordered"], border=0), unsafe_allow_html=True)
