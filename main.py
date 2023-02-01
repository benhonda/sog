from datetime import datetime
import pandas as pd
from fake_useragent import UserAgent

season = datetime.now().year if datetime.now().month >= 10 else datetime.now().year - 1


'''
Here we go...
'''

'''

  1. Input: Z Hyman vs NYI

  2. Pull data for NYI

  3. Get data for Z Hyman SOG and Shot Attempts vs. teams that are "similar" to NYI
        What makes two teams "similar"? This is the money criteria I guess...
          Could be...
            Similar blocked shot %
            Similar record
            TBD...

            + any combination of these! Could be all or just a couple!

  4. Want lineup data too... like when McDusty is out of the lineup how does that affect Hyman's SOG?
        So maybe

  5. Want recent performance data too... like what is Hyman's SOG trend?

'''


def get_player_gbg(player_id: int):
    '''
    Get all relevant data for a player, game by game

    Returns a DataFrame
    '''
    # ua = UserAgent()
    # url = 'https://moneypuck.com/moneypuck/playerData/careers/gameByGame/all_teams.csv'
    # data = read_csv(url, storage_options={'User-Agent': ua.firefox})

    df = pd.read_csv('./test/8470638_bergeron_jan_31.csv')

    df = df.loc[(df["season"] == season) & (df["situation"] == 'all')]

    # rm all 'for' columns (we only care about 'against')
    # df.drop(list(df.filter(regex='For')), axis=1, inplace=True)
    df = df[['opposingTeam', 'I_F_shotAttempts', 'I_F_shotsOnGoal']]

    print(df)

    return df


def get_all_teams_gbg_data():
    '''
    Get all relevant data for each team, game by game

    Returns a DataFrame
    '''
    # ua = UserAgent()
    # url = 'https://moneypuck.com/moneypuck/playerData/careers/gameByGame/all_teams.csv'
    # data = read_csv(url, storage_options={'User-Agent': ua.firefox})

    df = pd.read_csv('./test/all_teams_jan_31.csv')

    # rm all 'for' columns (we only care about 'against')
    df.drop(list(df.filter(regex='For')), axis=1, inplace=True)

    df = df.loc[df["season"] == season]

    return df


def get_similar_teams(all_teams_df: pd.DataFrame, target_df: pd.DataFrame):
    '''
    Get teams that share same characteristics as the rival team
    '''

    teams = set(all_teams_df['team'].tolist())
    # remove target team
    teams.remove(target_df['team'].tolist()[0])

    teams_sim = {}

    for team in teams:
        team_gbg_df = all_teams_df.loc[(all_teams_df['team'] == team)]
        # team_gbg_df_mean = team_gbg_df.mean(numeric_only=True)

        target_team_gbg_df_mean = target_df.describe()
        other_team_gbg_df_mean = team_gbg_df.describe()

        # target_team_gbg_df_mean = target_df.mean(numeric_only=True)
        # other_team_gbg_df_mean = team_gbg_df.mean(numeric_only=True)

        # plug-in similarity fn...

        # let's start simple, shall we?
        # we're only gonna use mean and a deviation %

        team_similarities = []

        for col in target_team_gbg_df_mean:
            target_team_val = target_team_gbg_df_mean[col]['mean']
            other_team_val = other_team_gbg_df_mean[col]['mean']

            dev = 0.05
            low = target_team_val - (target_team_val * dev)
            high = target_team_val + (target_team_val * dev)

            # print(other_team_val)

            if min(low, high) < other_team_val < max(low, high):
                # inside
                team_similarities.append(col)

        print(f'{team} - similarities: {len(team_similarities)}')
        teams_sim[f'{team}'] = {
            'sim_cols': team_similarities
        }

    return teams_sim


if __name__ == '__main__':
    rival_team = 'TOR'
    player_id = '8475786' # TODO: will use this later...

    gbg_player_df = get_player_gbg(player_id=player_id)

    gbg_df = get_all_teams_gbg_data()
    rival_gbg_df = gbg_df.loc[(gbg_df['team'] == rival_team) & (gbg_df['season'] == season)]

    teams_sim = get_similar_teams(all_teams_df=gbg_df, target_df=rival_gbg_df)

    teams_to_look_at = []
    for team in teams_sim:
        team_dict = teams_sim[team]
        if len(team_dict['sim_cols']) > 37:
            teams_to_look_at.append(team)

    gbg_player_df = gbg_player_df.loc[gbg_player_df['opposingTeam'].isin(teams_to_look_at)]
    
    print(f'similar teams: {teams_to_look_at}')
    print(gbg_player_df.describe())
    
