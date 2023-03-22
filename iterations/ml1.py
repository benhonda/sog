from datetime import datetime
import pandas as pd
from fake_useragent import UserAgent
import matplotlib.pyplot as plt

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.feature_selection import SequentialFeatureSelector as SFS

season = datetime.now().year if datetime.now().month >= 10 else datetime.now().year - 1


'''
Here we go...
'''

'''

  a. We use all of Hyman's career games to train the model (may limit in the future)
  b. We pull in stats that we want from all the opp. teams and include them for each row (each game that Hyman's played)
  c. Every column (stat) becomes an input neuron and the output neurons are SOG between 0 and 16

'''


def show_heatmap(data: pd.DataFrame):
    ''' This heat map shows the correlation between different features. '''
    plt.matshow(data.corr())
    plt.xticks(range(data.shape[1]), data.columns, fontsize=4, rotation=90)
    plt.gca().xaxis.tick_bottom()
    plt.yticks(range(data.shape[1]), data.columns, fontsize=4)

    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title("Feat correlation heater", fontsize=14)
    plt.show()


if __name__ == '__main__':
    '''

    I think maybe we start with like 10 players

    For each player,
        get team-for and team-against related features and merge onto row

    This attempt:
      Tabular (Not time series)




    Eventually... want to try line combos

    '''

    rival_team = 'NYI'

    # get player df
    # df = pd.read_csv('./test/8470638_bergeron_jan_31.csv')
    # player_df = player_df.loc[(player_df["situation"] == 'all')]

    # player_df = pd.read_csv('./test/8475786_hyman_jan_31.csv')
    # player_df = player_df.query('situation == "all" and icetime > 1000')

    # TODO:
    #   somehow take into account icetime .... either extrapolate low ice time games (i.e. early career) or remove

    '''
    Data prep

    options/ideas:
      - average the game-by-game (GBG) data ourselves, use that in the prediction of the next SOG value
          |----------------------------------------------------------------------------|
          |   Should we treat this as a time series problem then? Probably!            |
          |----------------------------------------------------------------------------|
      -


        Data can be found here (directory)!
            https://moneypuck.com/moneypuck/playerData/



      some things (questions) we may want to consider:

        - how many shots did hero have last game? last 2 games? last 10 games? is there a trend?

        - who is hero playing with tonight (line)? historically, how does that affect hero's SOG?

        - who is hero playing against tonight (team)? historically, how does that affect hero's SOG?
              - can we group teams into categories based on ranking, blocked shots, +other stats?
                      then ask: how does hero play against teams from group X?

                      

          Relative percieved importance (RPI) - Stat
          *** - TOI
          *** - PP TOI
          *** - Zone starts - More offensive zone starts generally lead to more shot attempts for;
          *** - Quality of competition 
          *** - Quality of teammates
          **  - Takeways
          *   - PK TOI
          *   - Giveaways

        |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|
        |  all these "expected" stats are their own time series, right??
        |
        |   logically, these stats will have some effect
        |   on hero's SOG.
        |
        |       TODO: keep building this "expected" list!
        |
        |------------------------------------------------------------------|

      then with this data answered and transformed to numeric, we can run feature selection to tell us which of these features
      are the most predictive of hero's SOG... this could be different from player to player, who knows?

      ---------------------------------------------------------------
      | Consider this:
      |
      |  What if we ran feature selection on the original
      |  player + team df to find the features that were most
      |  predictive of hero's SOG? I.e., in the first pass, 
      |  treat this as a tabular problem, not a time series problem.
      |  
      |   then use those to build the "expected" features list (as in
      |   the example above), which we will apply to the time-series
      |   problem of "how many SOG will X have against team X tonight?
      |
      | update:
      |   this is often called "two-stage feature selection"
      |    (when we use these features in a second model)
      |
      ---------------------------------------------------------------



      First pass (LOL)
        Training accuracy: 11.940298507462686
        Test accuracy: 5.970149253731343
      Using
        - all features (except strings, excl. home/away)
        - KNN regression
      Update: 
        Sike... this was looking checking accuracy for a classification problem


    
      ********************************************************************************
      *
      *   update Mar 7 2023.
            This isn't really a time-series problem.
            Time series asks, "based on previous performance, how many SOGs will player X have?
            But that (assumably) can be answered by averaging previous stats... 
      *
      *
      ********************************************************************************


      Here is the plan (for now)
        We'll look at 5 main things: TOI, PP TOI, zone starts, quality of competition, quality of teammates
          * each of these may require many "features"

        - TOI
          * we train the model, giving it the line that the player is on (because we will know this when it comes time to predict)
              * we can calculate if line is 1st, 2nd, 3rd, etc. by comparing "ice_time" to other lines for that game_id
              * again, we will know this information during predict time via something like dailyfaceoff.com
              * note, there are related stats to ice_time that we could use instead, such as I_F_shifts. Will have to 
                test to see how it affects the results!
        - PP TOI
          * we get this directly from player_data. I don't know how not knowing the exact PP line combo will affect things, 
            but we're gonna try this for now.
        - ZONE STARTS
          * we get this directly from player_data, using stats such as I_F_oZoneShiftStarts, I_F_dZoneShiftStarts, etc.
        - QUALITY OF COMPETITION
          * 
        - QUALITY OF TEAMMATES

        
        xTOI
            extrapolated from Line #{1,2,3,4}

        xPPTOI
            -
    '''

    # read CSV
    df = pd.read_csv('./test/8475786_hyman_jan_31.csv')

    # filter
    df = df.query('situation == "all" and icetime > 1000')

    # drop some cols
    # drop invalid(?) ones
    df = df.drop(['name', 'playerTeam', 'opposingTeam', 'position', 'situation'], axis=1)
    # drop not-possibly-related-to-sog ones
    df = df.drop(['playerId', 'gameId', 'gameDate', 'season'], axis=1)
    # drop ones we find
    df = df.drop([
        'I_F_playContinuedOutsideZone', # as a result of SOG
        'I_F_unblockedShotAttempts',
        'xGoalsForAfterShifts',
        'xGoalsAgainstAfterShifts',
        'corsiForAfterShifts',
        'corsiAgainstAfterShifts',
        'I_F_xPlayStopped',
        'I_F_playContinuedInZone', # as a result of SOG
        'I_F_xPlayContinuedInZone', # as a result of SOG
        'I_F_savedShotsOnGoal', # directly correlated
        'I_F_scoreAdjustedShotsAttempts', # directly correlated
        'OffIce_A_shotAttempts', # not even sure how this relates...
        'fenwickForAfterShifts', # not even sure how this relates...
    ], axis=1)

    # mapping strings to numerics
    df['home_or_away'] = df['home_or_away'].map({'AWAY': 0, 'HOME': 1})

    y = df.loc[:, 'I_F_shotsOnGoal']
    X = df.loc[:, df.columns != 'I_F_shotsOnGoal']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    sc = StandardScaler()
    X_train_std = sc.fit_transform(X_train)
    X_test_std = sc.transform(X_test)

    n_neighbors = 5

    for i, weights in enumerate(["uniform", "distance"]):
        model = KNeighborsRegressor(n_neighbors=n_neighbors, weights=weights)
        y_ = model.fit(X_train_std, y_train).predict(X_test_std)

        plt.subplot(2, 1, i + 1)
        plt.scatter(X_train_std, y_train, color="darkorange", label="data")
        plt.plot(X_test_std, y_, color="navy", label="prediction")
        plt.axis("tight")
        plt.legend()
        plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (n_neighbors, weights))

    plt.tight_layout()
    plt.show()


    # print('Training accuracy:', np.mean(model.predict(X_train_std) == y_train) * 100)
    # print('Test accuracy:', np.mean(model.predict(X_test_std) == y_test) * 100)

    # sfs2 = SFS(model, n_features_to_select=8, direction='forward', n_jobs=-1, cv=5)
    # sfs2 = sfs2.fit(X_train_std, y_train)

    # print('Selected Features:', np.arange(X.shape[1])[sfs2.support_])
    # selected = np.arange(X.shape[1])[sfs2.support_]
    # for i in selected:
    #     print(df.columns[i])

    # merge in team FOR and AGAINST features
    # df =

    # removing features
    #  - icetime: we'll use icetimerank instead
    #  -
    # df = df.drop(['icetime'], axis=1)

    # standardize
    # ...

    # LASSO regression
    # ...

    # Sequential feature selection
    # ...

    # Need Nested CV somewhere in here too...

    # print(df.info())

    # get df for all teams
    # allteams_df = pd.read_csv('./test/all_teams_jan_31.csv')
    # allteams_df = allteams_df.loc[(allteams_df["situation"] == 'all')]

    # only get the games that the player played in
    # merged_df = pd.merge(player_df, allteams_df, left_on=['gameId', 'playerTeam'], right_on=['gameId', 'team'])

    # show_heatmap(merged_df)

    # print(merged_df.var())

    # print(merged_df.head())
    # print(merged_df.I_F_shotsOnGoal)
