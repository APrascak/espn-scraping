# Web-Scraping NBA Game Data (ESPN)
Deployed to Google Compute Engine as Cron Job to update Firestore database with live NBA scores and odds every 5 minutes.
&nbsp;
##### Instructions
* Include your own Firestore credentials
* Update document reference for your database
* Configure as cron job (every 5 minutes should be sufficient)  
* Running cron job on Google Compute Engine: https://youtu.be/5OL7fu2R4M8
* Setting script frequency: https://crontab.guru/
&nbsp;
##### Format
```
data = {
    last_updated: 04/05/2020, 21:00:46,
    current_matches: [
        {
            date: 2020-03-11T23:30Z
            match_id: http://www.espn.com/nba/game?gameId=401161785
            status: STATUS_POSTPONED
            team1: CHA
            team1_score: 0
            team2: ATL
            team2_score: 0
            title: Atlanta Hawks at Charlotte Hornets
        },
        .....
    ],
    future_matches: [
        {
            date: 2020-03-11T23:30Z
            match_id: http://www.espn.com/nba/game?gameId=401161785
            home_team: PHI
            home_team_spread: -12.0
            away_team: DET
            away_team_spread: +12.0
            title: Detroit Pistons at Philadelphia 76ers
        },
        .....
    ]
}
```