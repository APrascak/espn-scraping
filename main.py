'''
ESPN NBA Web Scraper
Developer: Alex Prascak
* Organizes game information and uploads to Firestore database
* Runs on Google Compute Engine as cron job
'''


# Import Libraries
import re
import requests
from bs4 import BeautifulSoup
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# Pull credentials from service account file
cred = credentials.Certificate('./serviceAccountKey.json')


# Establish firebase admin app and DB reference
firebase_admin.initialize_app(cred)
db = firestore.client()


# Find all script tags from the website
nba_link = 'https://www.espn.com/nba/scoreboard'
page1 = requests.get(nba_link)
nba_soup = BeautifulSoup(page1.text, 'html.parser')
scripts = nba_soup.find_all('script')


# Find and retrieve the script tag containing the game information
i = 0
while (scripts[i].get_text())[0:6] != 'window':
    i += 1
solution = scripts[i].get_text()
needed_data = solution[30:solution.find(';window.espn.scoreboardSettings')]


# Text to JSON conversion
response = json.loads(needed_data)

# Create dict to structure data
# Place timestamp
games = {
    "last_updated": unicode(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")),
    "future_matches": [],
    "current_matches": []
}

# Add game information to dict
for i in range(len(response["events"])):

    if "odds" in response["events"][i]["competitions"][0].keys():
        game = {
            "match_id": response["events"][i]["links"][0]["href"],
            "title": response["events"][i]["name"],
            "date": response["events"][i]["date"],
            "status": response["events"][i]["status"]["type"]["name"],
            "team1": response["events"][i]["competitions"][0]["competitors"][0]["team"]["abbreviation"],
            "team2": response["events"][i]["competitions"][0]["competitors"][1]["team"]["abbreviation"],
            "spread": response["events"][i]["competitions"][0]["odds"][0]["details"]
        }
        games["future_matches"].append(game)

    else:
        game = {
            "match_id": response["events"][i]["links"][0]["href"],
            "title": response["events"][i]["name"],
            "date": response["events"][i]["date"],
            "status": response["events"][i]["status"]["type"]["name"],
            "team1": response["events"][i]["competitions"][0]["competitors"][0]["team"]["abbreviation"],
            "team2": response["events"][i]["competitions"][0]["competitors"][1]["team"]["abbreviation"],
            "team1_score": response["events"][i]["competitions"][0]["competitors"][0]["score"],
            "team2_score": response["events"][i]["competitions"][0]["competitors"][1]["score"],
        }
        games["current_matches"].append(game)


# Convert dict to JSON
doc = json.dumps(games, indent = 4)


# Update Firestore document
doc_ref = db.collection(u'current_matches').document(u'nba')
doc_ref.set(games)





'''
DATA FORMAT:
-----------------------------
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