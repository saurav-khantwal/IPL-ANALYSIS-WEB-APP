import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

match_df = pd.read_csv('IPL MATCH.csv')
ball_df = pd.read_csv('UPDATED IPL BALL.csv')
scorecard = pd.read_csv('batting_stats_every_match.csv')
bowling_card = pd.read_csv('bowling_stats_every_match.csv')
batting_tally = pd.read_csv('batting_stats.csv')
batting_tally_season = pd.read_csv('batting_stats_season.csv')
bowling_tally = pd.read_csv('bowling_stats.csv')
bowling_tally_season = pd.read_csv('bowling_stats_season.csv')
bowling_opposition = pd.read_csv('bowling_performance_opposition.csv')
bowling_opposition_season = pd.read_csv(
    'bowling_performance_opposition_season.csv')
batting_opposition = pd.read_csv('batsman_performance_opposition.csv')
batting_opposition_season = pd.read_csv(
    'batsman_performance_opposition_season.csv')


batting_tally_season.rename(columns={'high_score': 'High_score'}, inplace=True)

# ***********************************THIS SECTION WILL RETURN FOR THE MATCH STATS SECTION*********************
# ************************************************************************************************************
# ************************************************************************************************************
# TEST


def get_filtered_match(season, type):
    """This function will send the filtered
    matches to the select box"""

    x = None
    if (season == 'All Time'):
        if (type == 'All Matches'):
            x = match_df
        elif (type == 'Playoff Matches'):
            x = match_df[match_df['Playoff'] == 1]
        elif (type == 'Final Matches'):
            x = match_df[match_df['Final'] == 1]
        else:
            x = match_df[(match_df['Final'] != 1) & (match_df['Playoff'] != 1)]

    else:
        if (type == 'All Matches'):
            x = match_df[match_df['season'] == season]
        elif (type == 'Playoff Matches'):
            x = match_df[(match_df['season'] == season)
                         & (match_df['Playoff'] == 1)]
        elif (type == 'Final Matches'):
            x = match_df[(match_df['season'] == season)
                         & (match_df['Final'] == 1)]
        else:
            x = match_df[(match_df['season'] == season) & (
                (match_df['Final'] != 1) & (match_df['Playoff'] != 1))]

    x = x.reset_index(drop=True)
    x['index'] = x.index + 1
    x['index'] = x['index'].astype(str)
    x['Match'] = x['index'] + ')  ' + x['team1'] + ' VS ' + x['team2']
    return x


def get_scorecard(id, inning, type):
    """This Function will return the Scorecard of
     batting of balling"""

    if (type == 'batting'):
        x = scorecard.loc[(scorecard['id'] == id) & (scorecard['inning'] == inning),
                          ['batsman', 'batsman_runs', 'valid_ball', 'strike_rate', 'info']].reset_index(drop=True)
        x.index = x.index + 1
        return x

    if (type == 'bowling'):
        x = bowling_card.loc[(bowling_card['id'] == id) & (bowling_card['inning'] == inning),
                             ['bowler', "over_bowled", "bowler's_runs", "bowler's_wicket", 'economy']]. \
            reset_index(drop=True)
        x_temp = x['over_bowled'].values
        x_temp = [str(int(i)) if int(i) == i else str(i) for i in x_temp]
        x['over_bowled'] = x_temp
        x.index = x.index + 1
        return x


def get_team_name(id, inning, home, bat_or_bowl):
    """This function will return the Imputed names
     of the Teams"""

    if (home == 'inning'):
        var = ''
        if (bat_or_bowl == 'batting'):
            var = ball_df.loc[(ball_df['id'] == id) & (
                ball_df['inning'] == inning), 'batting_team'].unique()[0]
        elif (bat_or_bowl == 'bowling'):
            var = ball_df.loc[(ball_df['id'] == id) & (
                ball_df['inning'] == inning), 'bowling_team'].unique()[0]
        if (var == 'Sunrisers Hyderabad'):
            return 'SRH'
        words = var.split()
        letters = [word[0] for word in words]
        return "".join(letters).upper()

    else:
        var = ''
        if inning == 1:
            var = match_df.loc[match_df['id'] == id, 'team1'].values[0]
        if inning == 2:
            var = match_df.loc[match_df['id'] == id, 'team2'].values[0]

        if (var == 'Sunrisers Hyderabad'):
            return 'SRH'
        words = var.split()
        letters = [word[0] for word in words]
        return "".join(letters).upper()


def get_total(id, inning, home):
    """This function will Return the total
     of the teams with wickets"""

    if (home == 'home'):
        batting_team = match_df.loc[match_df['id'] == id, [
            'team1', 'team2']].values[0][inning - 1]

        x = ball_df[(ball_df['id'] == id) & (ball_df['batting_team'] == batting_team)][
            ['total_runs', 'is_wicket']].sum().values
        total = str(x[0]) + '/' + str(x[1])
        return total

    else:
        x = ball_df[(ball_df['id'] == id) & (ball_df['inning'] == inning)][
            ['total_runs', 'is_wicket']].sum().values
        total = str(x[0]) + '/' + str(x[1])
        return total


def get_total_overs(id, inning):
    """This function will return the
    total overs played by the team"""

    batting_team = match_df.loc[match_df['id'] ==
                                id, ['team1', 'team2']].values[0][inning - 1]
    sum = ball_df[(ball_df['id'] == id) & (
        ball_df['batting_team'] == batting_team)]['valid_ball'].sum()
    sum = (sum // 6) + (sum % 6) / 10
    return str(sum)


def get_result(id):
    """This function will return the
    Final result of the match"""

    temp = ['runs', 'wickets']
    match_temp = match_df[match_df['result'].isin(temp)]
    match_temp['result_margin'] = match_temp['result_margin'].astype(
        float).astype(int)

    if match_df.loc[match_df['id'] == id, 'result'].unique()[0] == 'tie':
        winner = match_df.loc[match_df['id'] == id, 'winner'].unique()[0]
        return 'Match won by ' + winner + ' in the Super Over'

    elif match_df.loc[match_df['id'] == id, 'result'].unique()[0] == 'Washed Out':
        return 'Match Washed Out'

    else:
        winner = match_temp.loc[match_temp['id'] == id, 'winner'].unique()[0]
        margin = match_temp.loc[match_temp['id'] == id, 'result_margin'].unique()[
            0]
        if match_temp.loc[match_temp['id'] == id, 'result'].unique()[0] == 'runs':
            if (margin == 1):
                return winner + ' Won the match by ' + str(margin) + ' run'
            return winner + ' Won the match by ' + str(margin) + ' runs'
        if (margin == 1):
            return winner + ' Won the match by ' + str(margin) + ' wicket'
        return winner + ' Won the match by ' + str(margin) + ' wickets'


def get_mom(id):
    """This function will return
    the Man of the Match"""

    if match_df.loc[match_df['id'] == id, 'result'].unique()[0] == 'Washed Out':
        return ''
    else:
        return 'Man of the Match - ' + match_df.loc[match_df['id'] == id, 'player_of_match'].unique()[0]


# **********************THIS SECTION WILL RETURN FOR THE PLOTS FOR MATCH STATS*******************************


def get_contribution_plot(id, inning):
    """This function will return a plotly pie chart for
    the runs contribution in total runs"""

    df_scores = ball_df.loc[(ball_df['id'] == id) & (ball_df['inning'] == inning)].groupby(['batsman'])[
        'batsman_runs'].sum().reset_index()
    df_scores = df_scores[df_scores['batsman_runs'] != 0]
    extras = {'batsman': 'Extras',
              'batsman_runs': ball_df.loc[(ball_df['id'] == id) & (ball_df['inning'] == inning)]['extra_runs'].sum()}
    df_scores = df_scores.append(extras, ignore_index=True)

    fig = go.Figure(data=[go.Pie(labels=df_scores['batsman'], values=df_scores['batsman_runs'].values,
                                 hole=.5, insidetextorientation='radial')])
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(width=800, height=400, margin=dict(t=10, b=20))
    return fig


def get_bar_plot(id, inning):
    """This function will return
    the bar plot for runs per over"""

    data = ball_df[(ball_df['id'] == id) & (ball_df['inning'] == inning)].groupby(['over'])[
        'total_runs'].sum().reset_index().rename(columns={'total_runs': 'Runs', 'over': 'Over'})
    data['Over'] = data['Over'] + 1
    data['color'] = 'red'
    data['Over'] = data['Over'].astype(str)
    fig = px.bar(data, y='Runs', x='Over', text='Runs')
    fig.update_traces(textposition='outside', marker=dict(
        line=dict(color='#000000', width=2)))
    fig.update_layout(width=800, height=400, margin=dict(t=10, b=20))
    return fig


def get_phase_plot(id, inning, bat_or_bowl):
    """This function will return a
    pie chart of runs scored in different phases of a Innings"""

    phase1 = phase2 = phase3 = 0

    if (bat_or_bowl == 'batting'):
        data = ball_df[(ball_df['id'] == id) & (ball_df['inning'] == inning)].groupby(
            ['over'])['total_runs'].sum().reset_index()
        data['over'] = data['over'] + 1

        for x in data['over'].values:
            if x <= 6:
                phase1 = phase1 + \
                    data.loc[data['over'] == x, 'total_runs'].values[0]
            elif (x >= 7) and (x <= 15):
                phase2 = phase2 + \
                    data.loc[data['over'] == x, 'total_runs'].values[0]
            else:
                phase3 = phase3 + \
                    data.loc[data['over'] == x, 'total_runs'].values[0]

        x = pd.DataFrame(
            {'Phase': ['1 - 6', '7 - 15', f"16 - 20"], 'Runs': [phase1, phase2, phase3]})

        fig = go.Figure(
            data=[go.Pie(labels=x['Phase'], values=x['Runs'], hole=.5)])
        colors = ['rgb(82, 215, 38)', 'rgb(255, 236, 0)', 'rgb(255, 115, 0)']
        fig.update_traces(marker=dict(colors=colors, line=dict(
            color='#000000', width=2)), sort=False)

    else:
        data = ball_df[(ball_df['id'] == id) & (ball_df['inning'] == inning)].groupby(
            ['over'])['is_wicket'].sum().reset_index()
        data['over'] = data['over'] + 1

        for x in data['over'].values:
            if x <= 6:
                phase1 = phase1 + \
                    data.loc[data['over'] == x, "is_wicket"].values[0]
            elif (x >= 7) and (x <= 15):
                phase2 = phase2 + \
                    data.loc[data['over'] == x, "is_wicket"].values[0]
            else:
                phase3 = phase3 + \
                    data.loc[data['over'] == x, "is_wicket"].values[0]

        x = pd.DataFrame(
            {'Phase': ['1 - 6', '7 - 15', f"16 - 20"], 'Wickets': [phase1, phase2, phase3]})

        fig = go.Figure(
            data=[go.Pie(labels=x['Phase'], values=x['Wickets'], hole=.5)])
        colors = ['rgb(99, 62, 187)', 'rgb(190, 97, 202)', 'rgb(242, 188, 94)']
        fig.update_traces(marker=dict(colors=colors, line=dict(
            color='#000000', width=2)), sort=False)

    fig.update_layout(width=800, height=400, margin=dict(t=10, b=20))
    return fig


def get_boundaries_bar(id):
    """This function will return the bar
    plot of boundaries scored by both teams"""

    boundaries = ball_df[ball_df['id'] == id].groupby(
        ['batting_team'])[['is_four', 'is_six']].sum().reset_index()
    fig = px.bar(boundaries, x='batting_team', y=[
                 'is_four', 'is_six'], barmode='group')
    fig.update_traces(textposition='outside', marker=dict(
        line=dict(color='#000000', width=2)))
    fig.update_layout(width=800, height=400, margin=dict(t=10, b=20))
    return fig


def get_worm_plot(id):
    """This function will return
    the worm plot"""

    data = ball_df[ball_df['id'] == id].groupby(
        ['batting_team', 'inning', 'over'])['total_runs'].sum().reset_index()
    data['over'] = data['over'] + 1
    data.sort_values(by=['inning', 'over'], inplace=True)
    a1 = data[data['inning'] == 1]['total_runs'].values
    a2 = data[data['inning'] == 2]['total_runs'].values

    for i in range(1, len(a1)):
        a1[i] = a1[i] + a1[i - 1]

    for i in range(1, len(a2)):
        a2[i] = a2[i] + a2[i - 1]

    a1 = np.append(a1, a2)
    data['total_runs'] = a1

    fig = px.line(data, x="over", y="total_runs", color='batting_team')
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(width=900, height=400, margin=dict(t=10, b=20))
    return fig


# ***********************************THIS SECTION WILL RETURN FOR THE OVERALL STATS SECTION*********************
# **************************************************************************************************************
# **************************************************************************************************************


def get_run_tally(cb, season):
    """This function will return
    the run tally of IPL"""
    if (season == 'All Time'):
        x = batting_tally[['batsman', 'Innings', 'batsman_runs', 'Average',
                           'strike_rate', 'High_score', 'Half_Centuries', 'Centuries']].reset_index(drop=True)
    else:
        x = batting_tally_season.loc[batting_tally_season['season'] == season, ['batsman', 'Innings', 'batsman_runs',
                                                                                'Average', 'strike_rate', 'High_score',
                                                                                'Half_Centuries',
                                                                                'Centuries']].reset_index(drop=True)
    x.index = x.index + 1
    if (cb):
        return x
    return x.head(5)


def get_wicket_tally(cb, season):
    """This function will return
    the Wicket tally of IPL"""

    if (season == 'All Time'):
        x = bowling_tally.reset_index(drop=True)
    else:
        x = bowling_tally_season.loc[bowling_tally_season['season'] == season].reset_index(
            drop=True)

    x = x[['bowler', 'match', 'wickets', 'economy', 'best', '4W Hall', '5W Hall']]

    x.index = x.index + 1
    if (cb):
        return x
    return x.head(5)


def get_boundaries_tally(cb, season):

    if(season == 'All Time'):
        x = batting_tally[['batsman', 'total_sixes', 'total_fours']].sort_values(
            by=['total_sixes'], ascending=False).reset_index(drop=True)
    else:
        x = batting_tally_season.loc[batting_tally_season['season'] == season, ['batsman', 'total_sixes', 'total_fours']]\
            .sort_values(by=['total_sixes'], ascending=False).reset_index(drop=True)
    x.index = x.index + 1
    if (cb):
        return x
    return x.head(5)


def get_catches_tally(cb, season):

    if(season == 'All Time'):
        x = scorecard.loc[scorecard['dismissal_kind'].isin(['caught', 'caught and bowled']), 'fielder'].\
            value_counts().sort_values(ascending=False).reset_index()
    else:
        x = scorecard.loc[(scorecard['dismissal_kind'].isin(['caught', 'caught and bowled'])) &
                          (scorecard['season'] == season), 'fielder'].\
            value_counts().sort_values(ascending=False).reset_index()
    x.rename(columns={'index': 'Fielder', 'fielder': 'Catches'}, inplace=True)
    x.index = x.index + 1
    if (cb):
        return x
    return x.head(5)


# ***********************************THIS SECTION WILL RETURN FOR THE PLAYER STATS SECTION*********************
# *************************************************************************************************************
# *************************************************************************************************************


def get_player_list():
    """This function will return
    all IPL players list for the select box"""

    return (batting_tally['batsman'].append(bowling_tally['bowler'])).unique()


def get_player_season(sb):
    """This function will return
    the modified season for the select box according to the player"""

    seasons = (batting_tally_season.loc[batting_tally_season['batsman'] == sb, 'season']
               .append(bowling_tally_season.loc[bowling_tally_season['bowler'] == sb, 'season'])).unique()
    seasons = -np.sort(-seasons)
    seasons = list(seasons)
    seasons.insert(0, 'Overall')
    return seasons


def get_batting_stats(player, season):
    """This function will return
    the batting stats of the player"""

    if (season == 'Overall'):
        return batting_tally[batting_tally['batsman'] == player]
    else:
        return batting_tally_season[(batting_tally_season['batsman'] == player) &
                                    (batting_tally_season['season'] == season)]


def get_bowling_stats(player, season):
    """This function will return
    the bowing stats of the player"""

    if (season == 'Overall'):
        return bowling_tally[bowling_tally['bowler'] == player]
    else:
        return bowling_tally_season[(bowling_tally_season['bowler'] == player) &
                                    (bowling_tally_season['season'] == season)]


# ******************************THIS SECTION WILL RETURN PLOTS FOR PLAYER ANALYSIS SECTION*********************


def get_performance_batting(player, season, type):
    """This function will return
    the plots of batsman performance"""

    if (season != 'Overall'):
        scores = scorecard.loc[(scorecard['batsman'] == player) &
                               (scorecard['season'] == season), type].reset_index(drop=True)
        if (sum(scores.values) == 0):
            return None
        fig = px.histogram(scores, x=type)

    else:
        scores = batting_tally_season.loc[
            batting_tally_season['batsman'] == player, ['season', type, 'Innings']].set_index('season')
        scores.index = scores.index.astype(str)
        if (scores[type].sum() == 0):
            return None
        if ((type == 'batsman_runs') or (type == 'Average')):
            fig = px.bar(scores, x=scores.index, y=type,
                         hover_data=[scores.index, "Innings", type])
        else:
            fig = px.line(scores, x=scores.index, markers=True,
                          y=type, hover_data=[scores.index, "Innings", type])
        fig.update_xaxes(showgrid=False)
        # fig.data[0].line.color = 'rgb(255,0,0)'

    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"), width=900, height=400, margin=dict(t=10, b=20))
    return fig


def get_performance_bowling(player, season):
    """This function will return
    the plots of bowler's performance"""

    if (season != 'Overall'):
        temp = ball_df.groupby(['id', 'bowler', 'season'])[
            "bowler's_wicket"].sum().reset_index()
        scores = temp.loc[(temp['bowler'] == player) &
                          (temp['season'] == season), "bowler's_wicket"].reset_index(drop=True)
        if (sum(scores.values) == 0):
            return None
        fig = px.histogram(scores, x="bowler's_wicket")

    else:
        scores = bowling_tally_season.loc[
            bowling_tally_season['bowler'] == player, ['season', 'wickets', 'match']]
        # scores.sort_values(by='season',inplace=True)
        scores.season = scores.season.astype(str)
        if (scores['wickets'].sum() == 0):
            return None
        fig = px.bar(scores, x=scores.season, y="wickets",
                     hover_data=[scores.season, "match", 'wickets'])
        fig.update_xaxes(showgrid=False)
        # fig.data[0].line.color = 'rgb(255,0,0)'

    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"), width=900, height=400, margin=dict(t=10, b=20))
    return fig


def get_performance_line(player, season, type):
    """This will return
    the line plot runs scored or the wickets taken in each match"""

    if (type == 'batsman_runs'):
        scores = scorecard.loc[(scorecard['batsman'] == player) &
                               (scorecard['season'] == season), ["batsman_runs"]].reset_index(drop=True)
        scores.index = (scores.index + 1).astype(str)
        fig = px.line(scores, x=scores.index, y="batsman_runs", markers=True,
                      labels={'batsman_runs': 'Runs', 'index': 'match'})

    else:
        temp = ball_df.groupby(['id', 'bowler', 'season'])[
            "bowler's_wicket"].sum().reset_index()
        scores = temp.loc[(temp['bowler'] == player) &
                          (temp['season'] == season), "bowler's_wicket"].reset_index(drop=True)
        scores.index = (scores.index + 1).astype(str)
        fig = px.line(scores, x=scores.index, y="bowler's_wicket", markers=True,
                      labels={"bowler's_wicket": 'Wickets', "index": 'match'})

    if (sum(scores.values) == 0):
        return None
    fig.update_xaxes(showgrid=False)
    # fig.data[0].line.color = 'rgb(255,0,0)'
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"), width=900, height=400, margin=dict(t=10, b=20))
    return fig


def get_bowling_economy(player, season):
    """This function will return 
    the line plot for economy of the player"""

    if (season != 'Overall'):
        scores = bowling_card.loc[(bowling_card['bowler'] == player) &
                                  (bowling_card['season'] == season), "economy"].reset_index(drop=True)
        if (sum(scores.values) == 0):
            return None
        fig = px.histogram(scores, x="economy")

    else:
        scores = bowling_tally_season.loc[
            bowling_tally_season['bowler'] == player, ['season', 'economy', 'match']]
        # scores.sort_values(by='season',inplace=True)
        scores.season = scores.season.astype(str)
        if (scores['economy'].sum() == 0):
            return None
        fig = px.line(scores, x=scores.season, y="economy", markers=True,
                      hover_data=[scores.season, "match", 'economy'])
        fig.update_xaxes(showgrid=False)
        # fig.data[0].line.color = 'rgb(255,0,0)'

    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"), width=900, height=400, margin=dict(t=10, b=20))
    return fig


def get_performance_phase(player, season, type):
    """This function will return
    the phase plot for the runs scored and wickets taken in different phases by players"""

    phase1 = phase2 = phase3 = 0

    if (type == 'batting'):

        if (season == 'Overall'):
            data = ball_df[(ball_df['batsman'] == player)].groupby(
                ['over'])['batsman_runs'].sum().reset_index()
        else:
            data = ball_df[(ball_df['batsman'] == player) & (ball_df['season'] == season)].groupby(
                ['over'])['batsman_runs'].sum().reset_index()

        data['over'] = data['over'] + 1

        for x in data['over'].values:
            if x <= 6:
                phase1 = phase1 + data.loc[data['over']
                                           == x, 'batsman_runs'].values[0]
            elif (x >= 7) and (x <= 15):
                phase2 = phase2 + data.loc[data['over']
                                           == x, 'batsman_runs'].values[0]
            else:
                phase3 = phase3 + data.loc[data['over']
                                           == x, 'batsman_runs'].values[0]

        x = pd.DataFrame(
            {'Phase': ['1 - 6', '7 - 15', f"16 - 20"], 'Runs': [phase1, phase2, phase3]})

        fig = go.Figure(
            data=[go.Pie(labels=x['Phase'], values=x['Runs'], hole=.5)])
        colors = ['rgb(82, 215, 38)', 'rgb(255, 236, 0)', 'rgb(255, 115, 0)']
        fig.update_traces(marker=dict(colors=colors, line=dict(
            color='#000000', width=2)), sort=False)

    else:

        if (season == 'Overall'):
            data = ball_df[(ball_df['bowler'] == player)].groupby(
                ['over'])["bowler's_wicket"].sum().reset_index()
        else:
            data = ball_df[(ball_df['bowler'] == player) & (ball_df['season'] == season)].groupby(
                ['over'])["bowler's_wicket"].sum().reset_index()

        data['over'] = data['over'] + 1

        for x in data['over'].values:
            if x <= 6:
                phase1 = phase1 + data.loc[data['over']
                                           == x, "bowler's_wicket"].values[0]
            elif (x >= 7) and (x <= 15):
                phase2 = phase2 + data.loc[data['over']
                                           == x, "bowler's_wicket"].values[0]
            else:
                phase3 = phase3 + data.loc[data['over']
                                           == x, "bowler's_wicket"].values[0]

        x = pd.DataFrame(
            {'Phase': ['1 - 6', '7 - 15', f"16 - 20"], 'Wickets': [phase1, phase2, phase3]})

        fig = go.Figure(
            data=[go.Pie(labels=x['Phase'], values=x["Wickets"], hole=.5)])
        colors = ['rgb(99, 62, 187)', 'rgb(190, 97, 202)', 'rgb(242, 188, 94)']
        fig.update_traces(marker=dict(colors=colors, line=dict(
            color='#000000', width=2)), sort=False)

    if (phase1 == 0 and phase2 == 0 and phase3 == 0):
        return None

    fig.update_layout(width=800, height=400, margin=dict(t=10, b=20))
    return fig


def get_performance_box(player, season, type):
    """This function will return
    the box plot of the player performance"""

    if (type == 'batting'):
        if (season != 'Overall'):
            scores = scorecard.loc[(scorecard['batsman'] == player) &
                                   (scorecard['season'] == season), 'batsman_runs'].reset_index(drop=True)
            if (sum(scores.values) == 0):
                return None
            fig = px.box(scores, y=scores.values, points="all",
                         notched=False, labels={'y': 'Runs'})

        else:
            scores = scorecard.loc[
                scorecard['batsman'] == player, ['season', 'batsman_runs']]
            if (scores['batsman_runs'].sum() == 0):
                return None
            fig = px.box(scores, color='season',
                         y='batsman_runs', notched=False)

    else:
        if (season != 'Overall'):
            temp = ball_df.groupby(['id', 'bowler', 'season'])[
                "bowler's_wicket"].sum().reset_index()
            scores = temp.loc[(temp['bowler'] == player) &
                              (temp['season'] == season), "bowler's_wicket"].reset_index(drop=True)
            if (sum(scores.values) == 0):
                return None
            fig = px.box(scores, y=scores.values, points="all",
                         notched=False, labels={'y': 'Wicket'})

        else:
            temp = ball_df.groupby(['id', 'bowler', 'season'])[
                "bowler's_wicket"].sum().reset_index()
            scores = temp.loc[temp['bowler'] ==
                              player, ['season', "bowler's_wicket"]]
            scores.season = scores.season.astype(str)
            if (scores["bowler's_wicket"].sum() == 0):
                return None
            fig = px.box(scores, color='season',
                         y="bowler's_wicket", notched=False)

    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(width=900, height=450,
                      margin=dict(t=10, b=20), boxgap=0.1)
    return fig


def get_player_boundaries(player, season):
    if (season == 'Overall'):
        boundaries = ball_df[ball_df['batsman'] == player].groupby(
            ['batsman'])[['is_six', 'is_four']].sum()
    else:
        boundaries = ball_df[(ball_df['batsman'] == player) & (ball_df['season'] == season)].groupby(['batsman'])[
            ['is_six', 'is_four']].sum()
    if (boundaries['is_six'].sum() == 0) and (boundaries['is_four'].sum() == 0):
        return None
    fig = px.bar(boundaries, x=['batsman'], y=[
                 'is_four', 'is_six'], barmode='group')
    fig.update_traces(textposition='outside', marker=dict(
        line=dict(color='#000000', width=2)))
    fig.update_layout(width=925, height=400, margin=dict(t=10, b=20))
    return fig


def get_performance_against_opposition(player, season, type):
    if (type == 'batting'):
        if (season == 'Overall'):
            data = batting_opposition[batting_opposition['batsman'] == player]
            if (data['batsman_runs'].sum() == 0):
                return None
            fig = px.bar(data, x='Bowling Team', y='batsman_runs',
                         hover_data=['batsman_runs', 'Innings', 'not outs', 'Average', 'Strike Rate'])
        else:
            data = batting_opposition_season[(batting_opposition_season['batsman'] == player) &
                                             (batting_opposition_season['season'] == season)]
            if (data['batsman_runs'].sum() == 0):
                return None
            fig = px.bar(data, x='Bowling Team', y='batsman_runs',
                         hover_data=['batsman_runs', 'Innings', 'not outs', 'Average', 'Strike Rate'])

    else:
        if (season == 'Overall'):
            data = bowling_opposition[bowling_opposition['bowler'] == player]
            if(data["bowler's_wicket"].sum() == 0):
                return None
            fig = px.bar(data, x='batting_team', y="bowler's_wicket", hover_data=[
                         "bowler's_wicket", 'Innings', 'economy'])
        else:
            data = bowling_opposition_season[(bowling_opposition_season['bowler'] == player) &
                                             (bowling_opposition_season['season'] == season)]
            if(data["bowler's_wicket"].sum() == 0):
                return None
            fig = px.bar(data, x='batting_team', y="bowler's_wicket",
                         hover_data=["bowler's_wicket", 'Innings', 'economy'])

    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(width=925, height=400, margin=dict(t=10, b=20))
    return fig


# ***********************************THIS SECTION WILL RETURN FOR THE TEAM STATS SECTION*********************
# *************************************************************************************************************
# *************************************************************************************************************


def get_average(x):
    if(x['id'] == x['not outs']):
        return x['batsman_runs']
    else:
        return x['batsman_runs']/(x['id']-x['not outs'])


def get_top_run_scorers(team,season,cb):

    if(season == 'All Time'):
        team_scorers = ball_df[ball_df['batting_team'] == team].groupby(['batsman']).agg(
            {'id': 'nunique', 'batsman_runs': 'sum', 'valid_ball': 'sum', 'is_four': 'sum',
             'is_six': 'sum'}).reset_index().sort_values(by=['batsman_runs'], ascending=False)

        team_not_outs = \
        scorecard[(scorecard['batting_team'] == team) & (scorecard['info'] == 'not out')].groupby(['batsman'])[
            'info'].count().to_dict()

    else:
        team_scorers = ball_df[(ball_df['batting_team'] == team) & (ball_df['season']==season)].groupby(['batsman']).agg(
            {'id': 'nunique', 'batsman_runs': 'sum', 'valid_ball': 'sum', 'is_four': 'sum',
             'is_six': 'sum'}).reset_index().sort_values(by=['batsman_runs'], ascending=False)

        team_not_outs =scorecard[(scorecard['batting_team'] == team) & (scorecard['info'] == 'not out')
        & (scorecard['season'] == season)].groupby(['batsman'])[
            'info'].count().to_dict()

    team_scorers['not outs'] = team_scorers.batsman.map(team_not_outs).fillna(0).astype(int)
    team_scorers['strike_rate'] = (team_scorers['batsman_runs'] / team_scorers['valid_ball']) * 100
    team_scorers['Average'] = team_scorers.apply(get_average, axis=1)

    team_scorers['strike_rate'] = [float(f"{x:.2f}") for x in team_scorers['strike_rate'].values]
    team_scorers['Average'] = [float(f"{x:.2f}") for x in team_scorers['Average'].values]
    team_scorers.rename(columns={'id':'match'}, inplace=True)

    if(cb):
        team_scorers = team_scorers.reset_index(drop=True)
    else:
        team_scorers = team_scorers.head(5).reset_index(drop=True)
    team_scorers.index = team_scorers.index+1

    return team_scorers


def get_top_wicket_takers(team,season,cb):

    if(season == 'All Time'):
        team_wicket=ball_df[ball_df['bowling_team']==team].groupby(['bowler']).agg({'id':'nunique','bowler\'s_wicket':'sum','valid_ball':'sum','bowler\'s_runs':'sum'}).\
            reset_index().sort_values(by=["bowler\'s_wicket"],ascending=False)

    else:
        team_wicket=ball_df[(ball_df['bowling_team']==team) & (ball_df['season'] == season)].groupby(['bowler']).agg({'id':'nunique','bowler\'s_wicket':'sum','valid_ball':'sum','bowler\'s_runs':'sum'}).\
            reset_index().sort_values(by=["bowler\'s_wicket"],ascending=False)

    team_wicket['overs_bowled'] = (team_wicket['valid_ball'] // 6) + (team_wicket['valid_ball'] % 6) / 10
    team_wicket['economy'] = team_wicket["bowler's_runs"] / team_wicket['overs_bowled']
    team_wicket['economy'] = [float(f"{x:.2f}") for x in team_wicket['economy'].values]
    team_wicket.rename(columns={'id':'match'}, inplace=True)

    if(cb):
        team_wicket = team_wicket.reset_index(drop=True)
    team_wicket = team_wicket.head(5).reset_index(drop=True)

    team_wicket.index = team_wicket.index+1
    return team_wicket[['bowler','match','bowler\'s_wicket','economy']]


def get_team_performance(team, season):

    if(season == 'All Time'):
        mum = match_df[((match_df['team1'] == team) | (match_df['team2'] == team))]
    else:
        mum = match_df[((match_df['team1'] == team) | (match_df['team2'] == team)) & (
                    match_df['season'] == season)]

    mum_stats = mum['team1'].value_counts().reset_index().merge(mum['team2'].value_counts().reset_index(), on=['index'],how='outer'). \
        merge(mum[mum['winner'] != team]['winner'].value_counts().reset_index().rename(columns={'winner': 'win_opposition'}), on=['index'], how='outer')
    mum_stats = mum_stats[~(mum_stats['index'] == team)]

    mum_stats.fillna(0, inplace=True)
    mum_stats[['team1', 'team2', 'win_opposition']] = mum_stats[['team1', 'team2', 'win_opposition']].astype(int)

    mum_stats['total_matches'] = mum_stats['team1'] + mum_stats['team2']
    mum_stats['wins'] = mum_stats['total_matches'] - mum_stats['win_opposition']
    mum_stats['win_percentage'] = (mum_stats['wins'] / mum_stats['total_matches']) * 100
    mum_stats['win_percentage'] = [float(f"{x:.2f}") for x in mum_stats['win_percentage'].values]
    mum_stats.rename(columns = {'index':'opposition'}, inplace = True)
    # fig = px.bar(mum_stats, x = 'opposition', y = 'win_percentage', hover_data=['total_matches', 'wins', 'win_percentage'])
    fig = px.funnel(mum_stats, x = 'wins', y = 'opposition', hover_data=['total_matches', 'wins', 'win_opposition', 'win_percentage'])
    fig.update_layout(width=1000, height=500, margin=dict(t=10, b=20))
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    return fig