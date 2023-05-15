import streamlit as st
from PIL import Image, ImageOps
import pandas as pd
import pickle
import time
import locale

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression


img = Image.open('assets/app-icon.png')

st.set_page_config(
    layout="wide",
    page_title="NHL Salary Predictor",
    page_icon=img,
    initial_sidebar_state="expanded"
    )

st.title("NHL Player Salary Predictor")

"""
In the National Hockey League (NHL), team executives lack a robust, data-driven solution to estimate
player salaries, which hinder's their ability to perform effective roster building and financial planning. 
This stems from the inherent complexity of factors that drive player salaries, including their performance, 
the quality of the team's they have played for, and the value of contracts signed by similar players. 
This project sought to design a data-driven approach that can leverage historical data and advanced modeling 
techniques to help NHL executives balance their budgets, invest in their rosters, and remain competitive 
within the league.

This web app allows you to predict the average annual value of a player's contract for the upcoming 2023-24 season,
taking into account their performance in the 2022-23 season. The app uses a linear regression model trained on
historical player data to make the predictions. The model was trained on data from the 2010-11 season through the 2019-20
season and tested on contracts from the 2020-21 season and 2021-22 season.

Please note that his app is still in development and is not yet optimized. The predictions are not guaranteed to be accurate.

If you have any questions or feedback, please contact me at charlesjramey@gmail.com or through [LinkedIn](https://www.linkedin.com/in/charlesjramey/)

Enjoy!


---
"""

left, right = st.columns(2)   

# Load the models
forwards_model = pickle.load(open('models/forwards_model.pkl', 'rb'))
defense_model = pickle.load(open('models/defense_model.pkl', 'rb'))
goalies_model = pickle.load(open('models/goalies_model.pkl', 'rb'))

# Load the player stats data
forwards_stats = pd.read_csv('data/forwards_2023.csv')
defense_stats = pd.read_csv('data/defense_2023.csv')
goalies_stats = pd.read_csv('data/goalies_2023.csv')

# Load active contract data
forward_contracts = pd.read_csv('data/active_contracts_f.csv')
defense_contracts = pd.read_csv('data/active_contracts_d.csv')
goalies_contracts = pd.read_csv('data/active_contracts_g.csv')



# Function to make salary predictions
def make_prediction(model, player_stats):
    prediction = model.predict(player_stats)
    return prediction

# Function to display the player's current salary
def display_salary(player_name):
    if forward_contracts['player'].str.contains(player_name).any():
        player_salary = forward_contracts[forward_contracts['player'] == player_name]['salary'].values[0]
    elif defense_contracts['player'].str.contains(player_name).any():
        player_salary = defense_contracts[defense_contracts['player'] == player_name]['salary'].values[0]
    elif goalies_contracts['player'].str.contains(player_name).any():
        player_salary = goalies_contracts[goalies_contracts['player'] == player_name]['salary'].values[0]
    st.write(f"Current Salary: {player_salary}")

def format_currency(number):
    locale.setlocale(locale.LC_ALL, '')  # Use the default locale for formatting
    formatted_string = []
    for value in number:
        # Convert the number to a string with comma-separated thousands
        formatted_number = locale.format_string("%d", number, grouping=True)
        # Add the dollar sign and append the formatted string to the list
        formatted_string.append(f"${formatted_number}")
    return formatted_string


with left:
    # User input for player name
    player_name = st.text_input("Enter Player Name", "")

    # Display user input suggestions based on input so far
    if player_name.lower() != "enter player name":
        # Check if name exists in forwards database
        if forward_contracts['player'].str.lower().str.contains(player_name.lower()).any():
            suggestions = forward_contracts.loc[forward_contracts['player'].str.lower().str.contains(player_name.lower()), 'player'].values
            filtered_suggestions = [suggestion for suggestion in suggestions if player_name.lower() in suggestion.lower()]
            selected_option = st.selectbox("Suggestions:", filtered_suggestions)

        # Check if name exists in defense database
        elif defense_contracts['player'].str.lower().str.contains(player_name.lower()).any():
            suggestions = defense_contracts.loc[defense_contracts['player'].str.lower().str.contains(player_name.lower()), 'player'].values
            filtered_suggestions = [suggestion for suggestion in suggestions if player_name.lower() in suggestion.lower()]
            selected_option = st.selectbox("Suggestions:", filtered_suggestions)

        # Check if name exists in goalies database
        elif goalies_contracts['player'].str.lower().str.contains(player_name.lower()).any():
            suggestions = goalies_contracts.loc[goalies_contracts['player'].str.lower().str.contains(player_name.lower()), 'player'].values
            filtered_suggestions = [suggestion for suggestion in suggestions if player_name.lower() in suggestion.lower()]
            selected_option = st.selectbox("Suggestions:", filtered_suggestions)

    # Display player's current salary
    display_salary(selected_option)

    # Get features for model
    if forwards_stats['player'].str.contains(selected_option).any():
        player_stats = forwards_stats[forwards_stats['player'] == selected_option].drop(columns=['player'])
        st.write(f"Games Played: {player_stats['games_played'].values[0]}")
        st.write(f"Goals: {player_stats['goals'].values[0]}")
        st.write(f"Assists: {player_stats['assists'].values[0]}")
        st.write(f"Points: {player_stats['points'].values[0]}")
    elif defense_stats['player'].str.contains(selected_option).any():
        player_stats = defense_stats[defense_stats['player'] == selected_option].drop(columns=['player'])
        st.write(f"Games Played: {player_stats['games_played'].values[0]}")
        st.write(f"Goals: {player_stats['goals'].values[0]}")
        st.write(f"Assists: {player_stats['assists'].values[0]}")
        st.write(f"Points: {player_stats['points'].values[0]}")
    elif goalies_stats['player'].str.contains(selected_option).any():
        player_stats = goalies_stats[goalies_stats['player'] == selected_option].drop(columns=['player'])
        st.write(f"Games Played: {player_stats['games_played'].values[0]}")
        st.write(f"Save Percentage: {player_stats['save_pct_on_shots_on_goal'].values[0]}")
        st.write(f"Goals Against Average: {player_stats['gaa'].values[0]}")


    # Make salary prediction
    if st.button("Predict 2023-24 Contract Value"):
        with st.spinner('Predicting...'):
            time.sleep(3)
            if forwards_stats['player'].str.contains(selected_option).any():
                prediction = make_prediction(forwards_model, player_stats)
            elif defense_stats['player'].str.contains(selected_option).any():
                prediction = make_prediction(defense_model, player_stats)
            elif goalies_stats['player'].str.contains(selected_option).any():
                prediction = make_prediction(goalies_model, player_stats)
        formatted_prediction = format_currency(prediction)
        st.write(f"Predicted Contract Value: {formatted_prediction}")

with right:
    # Display image
    st.image(Image.open('assets/nhl-faceoff.jpg'), use_column_width=True)