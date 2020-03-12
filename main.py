# Import Libraries
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import urllib

# Pull in the website's source code
url = 'http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2018/start/1'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

players = soup.find_all('tr', attrs = {'class': re.compile('row player-10-')})

player_stats = {
    "players": []
}

for player in players:
    stats = [stat.get_text() for stat in player.find_all('td')]

    x = {
        "name": stats[1],
        "GA": stats[3],
        "AB": stats[4],
        "R": stats[5],
        "BA": stats[15]
    }

    player_stats["players"].append(x)

y = json.dumps(player_stats, indent=4)


'''
This is where the actual application begins.
Goal: {
    betting_matches: [
        {
            title: Detroit Pistons at Philadelphia 76ers
            date: 2020-03-11T23:30Z
            home_team: PHI
            home_team_spread: -12.0
            away_team: DET
            away_team_spread: +12.0
        }
    ],
    current_matches: [
        {
            title: Detroit Pistons at Philadelphia 76ers
            date: 2020-03-11T23:30Z
            current_time: 3:13 - 2nd Quarter
            home_team: PHI
            home_team_score: 61
            away_team: DET
            away_team_score: 48
        }
    ],
    completed_matches: [
        {
            title: Detroit Pistons at Philadelphia 76ers
            date: 2020-03-11T23:30Z
            winning_team: home_team
            home_team: PHI
            home_team_score: 61
            away_team: DET
            away_team_score: 48
        }
    ]
}
'''

nba = 'https://www.espn.com/nba/scoreboard'
page1 = requests.get(nba)
nba_soup = BeautifulSoup(page1.text, 'html.parser')
test = nba_soup.find_all('script')
# test = nba_soup.find_all('article')
solution = test[13].get_text()
needed_data = solution[30:solution.find(';window.espn.scoreboardSettings')]

# print needed_data
response = json.loads(needed_data)
# print json.dumps(yee["events"], indent=4)
# for key, value in yee["events"][0].items():
    # print key, value

games = {
    "future_matches": [],
    "current_matches": []
}

# Add game statistics to array
for i in range(len(response["events"])):

    # print response["events"][i]["competitions"][0].keys()
    if "odds" in response["events"][i]["competitions"][0].keys():
        game = {
            "title": response["events"][i]["name"],
            "date": response["events"][i]["date"],
            "team1": response["events"][i]["competitions"][0]["competitors"][0]["team"]["abbreviation"],
            "team2": response["events"][i]["competitions"][0]["competitors"][1]["team"]["abbreviation"],
            "spread": response["events"][i]["competitions"][0]["odds"][0]["details"]
        }

        games["future_matches"].append(game)
    else:
        game = {
            "title": response["events"][i]["name"],
            "date": response["events"][i]["date"],
            "team1": response["events"][i]["competitions"][0]["competitors"][0]["team"]["abbreviation"],
            "team2": response["events"][i]["competitions"][0]["competitors"][1]["team"]["abbreviation"],
            "team1_score": response["events"][i]["competitions"][0]["competitors"][0]["score"],
            "team2_score": response["events"][i]["competitions"][0]["competitors"][1]["score"]
        }

        games["current_matches"].append(game)

print needed_data
print json.dumps(games, indent = 4)