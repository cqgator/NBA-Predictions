import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from io import StringIO

# Define the URL of the page
url = 'https://www.basketball-reference.com/playoffs/NBA_2024_advanced.html'

# Send a GET request
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with player stats
player_table = soup.find('table', {'id': 'advanced_stats'})

# Use StringIO to handle the HTML content as a file-like object
html_string = str(player_table)
data = pd.read_html(StringIO(html_string))[0]

# Drop columns where all values are NaN
data = data.dropna(axis=1, how='all')
# Remove rows where 'Rk' column has non-numeric values
data = data[data['Rk'].apply(lambda x: x.isnumeric())]

# Resetting the index
data.reset_index(drop=True, inplace=True)

# List of column names you want to convert to string
columns_to_convert_to_string = ['Player', 'Tm', 'Pos']  # Add any other text-based columns as needed

# Loop over the list and convert each column to string type
for column in columns_to_convert_to_string:
    data[column] = data[column].astype(str)

# List of column names you want to convert to numeric
columns_to_convert = ['VORP', 'Age', 'MP']  # Add any other columns as needed


# Loop over the list and convert each column
for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column], errors='coerce')
    data[column] = data[column].fillna(0)

data.rename(columns={'Tm': 'Team'}, inplace=True)

data[['Player', 'Tm', 'Pos', 'Age', 'MP', 'VORP']].to_csv('nba_player_stats.csv', index=False)

def get_team_input():
    team1 = input("Enter the first team: ")
    team2 = input("Enter the second team: ")
    return team1, team2

team1, team2 = get_team_input()

def compare_teams(team1, team2, data):
    team1_data = data[data['Tm'] == team1]
    team2_data = data[data['Tm'] == team2]
    # Compare stats - mean, median, etc.
    comparison_result = {
        'VORP': (round(team1_data['VORP'].mean(), 3), round(team2_data['VORP'].mean(), 3))
        
        # Add other stats here
    }
    return comparison_result

comparison_result = compare_teams(team1, team2, data)
print(comparison_result)

def plot_comparison(comparison_result, team1, team2):
    categories = list(comparison_result.keys())
    team1_stats = [result[0] for result in comparison_result.values()]
    team2_stats = [result[1] for result in comparison_result.values()]

    x = range(len(categories))
    plt.bar(x, team1_stats, width=0.4, label=team1, color='b')
    plt.bar([p + 0.4 for p in x], team2_stats, width=0.4, label=team2, color='r')
    plt.xticks([p + 0.2 for p in x], categories)
    plt.ylabel('Stats')
    plt.title('Team Comparison')
    plt.legend()
    plt.show()

plot_comparison(comparison_result, team1, team2)

# print(data['VORP'].dtype)
# print(data['VORP'].isna().sum())

# data.sort_values(by='VORP', ascending=True, inplace=True)
# print(data[['Player', 'VORP']].head()) 

# print(data[['Player', 'Age', 'MP']].sort_values(by='MP', ascending=False).head())

# data[data['Player'] == 'Tobias Harris']['VORP'].iloc[0]

# print(data.set_index('Player').loc['Tobias Harris']['VORP'])
