# MLB Import
from espn_api.baseball import League
import espn_api
import pandas as pd
import warnings
import datetime
import os
today = datetime.date.today()
year = today.year
warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", None)
pd.set_option('display.max_colwidth', None)

# Initializing league
league = League(league_id=929702235, year=2024, swid='5479be06-0e9f-49de-b677-cf8a388a3723', espn_s2='AECG5emtArOlIVusvFSalUmzw1PS5YdPit0EsHfFjMqmVKWmypzFMZ25NYOZ4FDUtj%2B7bVL2s55sZzJW8D7eEoFP4mFWRX9dA65s4DqbT7uKfX%2B7ld5AWgf7pM9qrbVU3PUNnt%2BCb2Aqmwqc%2BiZj8SD5xXAVXXBQuAY5UN6i%2B%2BeMT%2BgfGM3MFI7v2zH7cd85%2BOos82rHMD34i9LUkMpJTftCpsRMwgrG9MZyvxKTSahcI4X7t2%2BJjfcFaD9z7hyastRCz2xBpWvtSVbxNNgyXxbn')

# Previous week
last_full_week = league.currentMatchupPeriod

all_stats = []  # To store all stats for each week

for j in range(last_full_week):
    box = league.box_scores(j + 1)
    for i in range(6):
        # Get home team stats
        home_team = box[i].home_team
        home_stats = pd.DataFrame.from_dict(box[i].home_stats)
        home_stats.insert(0, 'Team', box[i].home_team)
        home_stats.insert(1, 'Opponent', box[i].away_team)
        
        # Get away team stats
        away_team = box[i].away_team
        away_stats = pd.DataFrame.from_dict(box[i].away_stats)
        away_stats.insert(0, 'Team', box[i].away_team)
        away_stats.insert(1, 'Opponent', box[i].home_team)
        
        # Concatenate home and away stats
        df = pd.concat([home_stats, away_stats], ignore_index=False)
        
        # Clean the team names
        df['Opponent'] = df['Opponent'].astype(str)
        df['Team'] = df['Team'].astype(str)
        df['Opponent'] = df['Opponent'].str.replace('Team(', '', regex=False).str.replace(')', '', regex=False)
        df['Team'] = df['Team'].str.replace('Team(', '', regex=False).str.replace(')', '', regex=False)
        
        # Add week information
        df.insert(0, 'Week', j + 1)
        
        # Append to the list
        all_stats.append(df)

# Combine all stats into a single DataFrame
final_df = pd.concat(all_stats, ignore_index=False)

# Assuming 'value' and 'result' columns need to be separated as shown before
stats = final_df.loc['value']
results = final_df.loc['result'].dropna(axis=1)

# Reset indexes
stats.reset_index(drop=True, inplace=True)
results.reset_index(drop=True, inplace=True)

# Combining results and stats

final_df = results
final_df.insert(3, 'HR_val', stats['HR'])
final_df.insert(5, 'WHIP_val', stats['WHIP'])
final_df.insert(7, 'ERA_val', stats['ERA'])
final_df.insert(9, 'K_val', stats['K'])
final_df.insert(11, 'OBP_val', stats['OBP'])
final_df.insert(13, 'SVHD_val', stats['SV']+stats['HLD'])
final_df.insert(15, 'R_val', stats['R'])
final_df.insert(17, 'RBI_val', stats['RBI'])
final_df.insert(19, 'W_val', stats['W'])
final_df.insert(21, 'SB_val', stats['SB'])

# temp = stats[['Team', 'R', 'HR', 'RBI', 'SB', 'K', 'W', 'SVHD']]
# seasonStats = temp.groupby('Team').sum()
# temp = stats[['Team', 'OBP', 'ERA', 'WHIP']]
# mean_stats = temp.groupby('Team').mean()
# seasonStats.insert(3, 'OBP', mean_stats.OBP)
# seasonStats.insert(6, 'ERA', mean_stats.ERA)
# seasonStats.insert(7, 'WHIP', mean_stats.WHIP)

# seasonStats.to_excel('SummaryData.xlsx')

# Gather standings, ranks, rosters up to current day
history = []
rosters = []
records = []
for i in range(2021, year+1):
    league = League(league_id=929702235, year=i, swid='5479be06-0e9f-49de-b677-cf8a388a3723', espn_s2='AECG5emtArOlIVusvFSalUmzw1PS5YdPit0EsHfFjMqmVKWmypzFMZ25NYOZ4FDUtj%2B7bVL2s55sZzJW8D7eEoFP4mFWRX9dA65s4DqbT7uKfX%2B7ld5AWgf7pM9qrbVU3PUNnt%2BCb2Aqmwqc%2BiZj8SD5xXAVXXBQuAY5UN6i%2B%2BeMT%2BgfGM3MFI7v2zH7cd85%2BOos82rHMD34i9LUkMpJTftCpsRMwgrG9MZyvxKTSahcI4X7t2%2BJjfcFaD9z7hyastRCz2xBpWvtSVbxNNgyXxbn')
    standings = league.standings()
    df = pd.DataFrame(standings)
    df2 = pd.DataFrame()
    df.rename(columns={0: "Team"}, inplace=True)
    df['Team'] = df['Team'].astype('str')
    df['Team'] = df['Team'].str.replace('Team(', '', regex=False).str.replace(')', '', regex=False)
    df['Rank'] = range(1,len(league.teams)+1)
    df['Year'] = i
    for j in range(0, len(league.teams)):
        team = league.teams[j]
        df2 = pd.DataFrame(team.roster)
        df2['Year'] = i
        df2['Team'] = team.team_name
        df2['Owner'] = team.owners[0]['firstName'] + " " + team.owners[0]['lastName']
        df2.rename(columns={0: "Player"}, inplace=True)
        df2['Player'] = df2['Player'].astype('str')
        df2['Player'] = df2['Player'].str.replace('Player(', '', regex=False).str.replace(')', '', regex=False)
        rosters.append(df2)

        team = league.teams[j]
        temp = pd.DataFrame({
            'Year': [i],
            'Wins': [team.wins],
            'Losses': [team.losses],
            'Ties': [team.ties],
            'Team': [team.team_name],
            'Owner': [team.owners[0]['firstName'] + " " + team.owners[0]['lastName']]
        }, index=[0])  # Specify an index
        records.append(temp)
        
    history.append(df)

temp1 = pd.concat(history, ignore_index=True)
temp2 = pd.concat(records, ignore_index=True)
final_df2 = pd.merge(temp1, temp2, on=['Team', 'Year'])
final_df2['Points'] = final_df2['Wins'] + (0.5*final_df2['Ties'])
final_df3 = pd.concat(rosters, ignore_index=True)

# Export to Excel
os.chdir('/Users/parkergeis/Library/CloudStorage/OneDrive-WesternGovernorsUniversity/Apps/Microsoft Power Query/Uploaded Files')
with pd.ExcelWriter('FantasyData.xlsx') as writer:  
    final_df.to_excel(writer, sheet_name='WeeklyData', index=False)
    final_df2.to_excel(writer, sheet_name='PreviousStandings', index=False)
    final_df3.to_excel(writer, sheet_name='Rosters', index=False)
os.chdir('/Users/parkergeis/Personal/SportsStats/FantasyBaseball/data')
with pd.ExcelWriter('FantasyData.xlsx') as writer:  
    final_df.to_excel(writer, sheet_name='WeeklyData', index=False)
    final_df2.to_excel(writer, sheet_name='PreviousStandings', index=False)
    final_df3.to_excel(writer, sheet_name='Rosters', index=False)