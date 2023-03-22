import os
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import requests
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))

def clean_and_refresh():
    ''' Overwrite existing data with new, fresh data from moneypuck.com '''

    # THRESHOLD
    # how fresh do we want/need this data?
    threshold_days = 6

    last_updated_file = os.path.join(path, '../data/last_updated.txt')
    is_already_updated = False

    for _ in (True,):
        with open(last_updated_file) as f:
            last_updated_date = f.readline().strip('\n')

            # if empty
            if len(last_updated_date) < 2:
                break

            if datetime.strptime(last_updated_date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=threshold_days) > datetime.now():
                is_already_updated = True

    # we already have the newest data
    if is_already_updated:
        print(f'Already have the newest data (up to {threshold_days} day(s) old)')
        return

    # else, download the files
    ua = UserAgent()
    for file_url in [
        "https://moneypuck.com/moneypuck/playerData/seasonSummary/2022/regular/skaters.csv",
        "https://moneypuck.com/moneypuck/playerData/seasonSummary/2022/regular/lines.csv",
        "https://moneypuck.com/moneypuck/playerData/seasonSummary/2022/regular/teams.csv",
    ]:
        req = requests.get(file_url, headers={'User-Agent': ua.firefox})
        file_name = file_url.rpartition('/')[-1]
        csv = open(os.path.join(path, f'../data/{file_name}'), 'wb')
        csv.write(req.content)
        csv.close()

    # and update date
    with open(last_updated_file, 'w') as f:
        f.write(f'{datetime.now()}')


    print("Refreshed data successfully.")
    return 


if __name__ == '__main__':

    '''************************
    Compile a list of player game-by-game CSVs to train our model
    ************************'''

    # TODO: (maybe) in the future, try different subsets of players (i.e. by phenotype?)
    # players = [
    #     '8124421' # crosby
    # ]

    # players_data_22_23 = "https://moneypuck.com/moneypuck/playerData/seasonSummary/2022/regular/skaters.csv"
    # lines_data_22_23 = "https://moneypuck.com/moneypuck/playerData/seasonSummary/2022/regular/lines.csv"
    # teams_data_22_23 = "https://moneypuck.com/moneypuck/playerData/seasonSummary/2022/regular/teams.csv"

    # # read csvs
    # df = pd.read_csv('./test/8475786_hyman_jan_31.csv')

    clean_and_refresh()
    pass
