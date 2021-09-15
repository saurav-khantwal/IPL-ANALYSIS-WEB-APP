import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px



match_df = pd.read_csv('IPL MATCH.csv')
ball_df = pd.read_csv('UPDATED IPL BALL.csv')
scorecard = pd.read_csv('batting_stats_every_match.csv')
bowling_card = pd.read_csv('bowling_stats_every_match.csv')
batting_tally=pd.read_csv('batting_stats .csv')
batting_tally_season=pd.read_csv('batting_stats_season.csv')
bowling_tally=pd.read_csv('bowling_stats.csv')
bowling_tally_season=pd.read_csv('bowling_stats_season.csv')

batting_tally_season.rename(columns={'innings':'Innings','valid_ball':'balls_faced','is_four':'total_fours',
                                     'is_six':'total_sixes','fifty':'Half_Centuries','century':'Centuries',
                                     'high_score':'High_score','average':'Average'},inplace=True)


bowling_tally.rename(columns={'four_wicket':'four','five_wicket':'five'},inplace=True)

#***********************************THIS SECTION WILL RETURN FOR THE MATCH STATS SECTION*********************

def send_match():
    """This function will send the Imputed
    matches for the match select box"""

    x = match_df.sort_values(by=['date', 'id'], ascending=True).reset_index(drop=True)
    x['index'] = x.index + 1
    x['index'] = x['index'].astype(str)
    x['Match'] = x['index'] + ')  ' + x['team1'] + ' VS ' + x['team2']
    return x


def send_filtered_match(df, season, type):
    """This function will send the filtered
    matches to the select box"""

    if (season == 'All Time'):
        if (type == 'All Matches'):
            return df['Match']
        if (type == 'Playoff Matches'):
            return df[df['Playoff'] == 1]['Match']
        if (type == 'Final Matches'):
            return df[df['Final'] == 1]['Match']
        if (type == 'League Matches'):
            return df[(df['Final'] != 1) & (df['Playoff'] != 1)]['Match']

    if (type == 'All Matches'):
        return df[df['season'] == season]['Match']
    if (type == 'Playoff Matches'):
        return df[(df['season'] == season) & (df['Playoff'] == 1)]['Match']
    if (type == 'Final Matches'):
        return df[(df['season'] == season) & (df['Final'] == 1)]['Match']
    if (type == 'League Matches'):
        return df[(df['season'] == season) & ((df['Final'] != 1) & (df['Playoff'] != 1))]['Match']


def get_scorecard(id, inning, type):
    """This Function will return the Scorecard of
     batting of balling"""

    if (type == 'batting'):
        x = scorecard.loc[(scorecard['id'] == id) & (scorecard['inning'] == inning),
                          ['batsman', 'batsman_runs', 'valid_ball', 'strike_rate', 'info']]. \
            sort_values('batsman_runs', ascending=False).reset_index(drop=True)
        x.index = x.index + 1
        return x

    if (type == 'bowling'):
        x = bowling_card.loc[(bowling_card['id'] == id) & (bowling_card['inning'] == inning),
                             ['bowler', "over_bowled", "bowler's_runs", "bowler's_wicket", 'economy']]. \
            sort_values(by=["bowler's_wicket", "over_bowled", 'economy'], ascending=[False, False, True]).reset_index(
            drop=True)
        x_temp=x['over_bowled'].values
        x_temp=[str(int(i)) if int(i) == i else str(i) for i in x_temp]
        x['over_bowled']=x_temp
        x.index = x.index + 1
        return x


def get_team_name(id, inning, home, bat_or_bowl):
    """This function will return the Imputed names
     of the Teams"""

    if (home == 'inning'):
        var = ''
        if (bat_or_bowl == 'batting'):
            var = ball_df.loc[(ball_df['id'] == id) & (ball_df['inning'] == inning), 'batting_team'].unique()[0]
        elif (bat_or_bowl == 'bowling'):
            var = ball_df.loc[(ball_df['id'] == id) & (ball_df['inning'] == inning), 'bowling_team'].unique()[0]
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

    if(home=='home'):
        batting_team = match_df.loc[match_df['id'] == id, ['team1', 'team2']].values[0][inning - 1]

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

    batting_team = match_df.loc[match_df['id'] == id, ['team1', 'team2']].values[0][inning - 1]
    sum = ball_df[(ball_df['id'] == id) & (ball_df['batting_team'] == batting_team)]['valid_ball'].sum()
    sum = (sum // 6) + (sum % 6) / 10
    return str(sum)


def get_result(id):
    """This function will return the
    Final result of the match"""

    temp = ['runs', 'wickets']
    match_temp = match_df[match_df['result'].isin(temp)]
    match_temp['result_margin'] = match_temp['result_margin'].astype(float).astype(int)

    if match_df.loc[match_df['id'] == id, 'result'].unique()[0] == 'tie':
        winner = match_df.loc[match_df['id'] == id, 'winner'].unique()[0]
        return 'Match won by ' + winner + ' in the Super Over'

    elif match_df.loc[match_df['id'] == id, 'result'].unique()[0] == 'Washed Out':
        return 'Match Washed Out'

    else:
        winner = match_temp.loc[match_temp['id'] == id, 'winner'].unique()[0]
        margin = match_temp.loc[match_temp['id'] == id, 'result_margin'].unique()[0]
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




# *****************THIS SECTION WILL RETURN FOR THE PLOTS FOR MATCH STATS*********************************


def get_contribution_plot(id, inning):
    """This function will return a plotly pie chart for
    the runs contribution in total runs"""

    df_scores = ball_df.loc[(ball_df['id'] == id) & (ball_df['inning'] == inning)].groupby(['batsman'])[
        'batsman_runs'].sum().reset_index()
    df_scores=df_scores[df_scores['batsman_runs']!=0]
    extras = {'batsman': 'Extras',
              'batsman_runs': ball_df.loc[(ball_df['id'] == id) & (ball_df['inning'] == inning)]['extra_runs'].sum()}
    df_scores = df_scores.append(extras, ignore_index=True)


    fig = go.Figure(data=[go.Pie(labels=df_scores['batsman'], values=df_scores['batsman_runs'].values, hole=.3,insidetextorientation='radial')])
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(width=800,height=400,margin=dict(t=10,b=20))
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
    fig.update_traces(textposition='outside',marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(width=800, height=400, margin=dict(t=10, b=20))
    return fig


def get_phase_plot(id, inning, bat_or_bowl):
    """This function will return a
    pie chart of runs scored in different phases of a Innings"""

    if(bat_or_bowl=='batting'):
        data = ball_df[(ball_df['id'] == id) & (ball_df['inning'] == inning)].sort_values(by=['over', 'ball']).groupby(
            ['batting_team', 'over'])['total_runs'].sum().reset_index()
        data['over'] = data['over'] + 1

        if (data['over'].max() <= 6):
            x=pd.DataFrame({'Phase': [f"1 - {str(data['over'].max())}"], 'Runs': [data.loc[0:,'total_runs'].sum()]})

        elif (data['over'].max() <= 16):
            x = pd.DataFrame({'Phase': ['1 - 6', f"7 - {str(data['over'].max())}"],
                              'Runs': [data.loc[0:5, 'total_runs'].sum(),data.loc[6:, 'total_runs'].sum()]})

        else:
            x = pd.DataFrame({'Phase': ['1 - 6', '7 - 15', f"16 - {str(data['over'].max())}"], 'Runs': [data.loc[0:5, 'total_runs'].sum()
                    , data.loc[6:14, 'total_runs'].sum(),data.loc[15:,'total_runs'].sum()]})

        fig = go.Figure(data=[go.Pie(labels=x['Phase'], values=x['Runs'], hole=.3)])
        colors = ['rgb(82, 215, 38)', 'rgb(255, 236, 0)', 'rgb(255, 115, 0)']
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)), sort=False)


    else:
        data = ball_df[(ball_df['id'] == id) & (ball_df['inning'] == inning)].sort_values(by=['over', 'ball']).groupby(
            ['bowling_team', 'over'])['is_wicket'].sum().reset_index()
        data['over'] = data['over'] + 1

        if (data['over'].max() <= 6):
            x = pd.DataFrame({'Phase': [f"1 - {str(data['over'].max())}"], 'Wickets': [data.loc[0:, 'is_wicket'].sum()]})

        elif (data['over'].max() <= 16):
            x = pd.DataFrame({'Phase': ['1 - 6', f"7 - {str(data['over'].max())}"],
                              'Wickets': [data.loc[0:5, 'is_wicket'].sum(), data.loc[6:, 'is_wicket'].sum()]})

        else:
            x = pd.DataFrame({'Phase': ['1 - 6', '7 - 15', f"16 - {str(data['over'].max())}"],
                              'Wickets': [data.loc[0:5, 'is_wicket'].sum()
                                  , data.loc[6:14, 'is_wicket'].sum(), data.loc[15:, 'is_wicket'].sum()]})

        if(x['Wickets'].sum()==0):
            return 0
        fig = go.Figure(data=[go.Pie(labels=x['Phase'], values=x['Wickets'], hole=.3)])
        colors = ['rgb(99, 62, 187)', 'rgb(190, 97, 202)', 'rgb(242, 188, 94)']
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)), sort=False)



    fig.update_layout(width=800, height=400, margin=dict(t=10, b=20))
    return fig



def get_worm_plot(id):
    """This function will return
    the worm plot"""

    data = ball_df[ball_df['id'] == id].sort_values(by=['inning', 'over', 'ball']).groupby(
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



#***********************************THIS SECTION WILL RETURN FOR THE OVERALL STATS SECTION*********************


def get_run_tally(cb):
    """This function will return
    the run tally of IPL"""

    x=batting_tally[['batsman','Innings','batsman_runs','Average','strike_rate','High_score','Half_Centuries',
                          'Centuries']].reset_index(drop=True)
    x.index=x.index+1
    if(cb):
        return x
    return x.head(10)


def get_wicket_tally(cb):
    """This function will return
    the Wicket tallly of IPL"""

    bowling_tally.reset_index(drop=True)
    bowling_tally.index=bowling_tally.index+1
    bowling_tally.rename(columns={'four_wicket':'4W_Hall','five_wicket':'5W_Hall'},inplace=True)
    if(cb):
        return bowling_tally
    return bowling_tally.head(10)


#***********************************THIS SECTION WILL RETURN FOR THE PLAYER STATS SECTION*********************


def get_player_list():
    """This function will return
    all IPL players list for the select box"""

    return (batting_tally['batsman'].append(bowling_tally['bowler'])).unique()


def get_player_season(sb):
    """This function will return
    the modified season for the select box according to the player"""

    seasons = list((batting_tally_season.loc[batting_tally_season['batsman']==sb,'season'].
    append(bowling_tally_season.loc[bowling_tally_season['bowler']==sb,'season'])).unique())
    seasons.insert(0,'Overall')
    return seasons

def get_batting_stats(player,season):
    """This function will return
    the batting stats of the player"""

    if(season=='Overall'):
        return batting_tally[batting_tally['batsman']==player]
    else:
        return batting_tally_season[(batting_tally_season['batsman']==player) &
                                    (batting_tally_season['season']==season)]

def get_bowling_stats(player,season):
    """This function will return
    the bowing stats of the player"""

    if (season == 'Overall'):
        return bowling_tally[bowling_tally['bowler'] == player]
    else:
        return bowling_tally_season[(bowling_tally_season['bowler'] == player) &
                                    (bowling_tally_season['season'] == season)]




#*****************************THIS SECTION WILL RETURN PLOTS FOR PLAYER ANALYSIS SECTION*********************


def get_performance_batting(player,season):
    """This function will return
    the plots of batsman performance"""

    if (season != 'Overall'):
        scores = scorecard.loc[(scorecard['batsman'] == player) &
                               (scorecard['season'] == season), 'batsman_runs'].reset_index(drop=True)
        fig = px.histogram(scores, x="batsman_runs")

    else:
        scores = batting_tally_season.loc[
            batting_tally_season['batsman'] == player, ['season', 'batsman_runs','Innings']].set_index('season')
        scores.index = scores.index.astype(str)
        fig = px.line(scores, x=scores.index, y="batsman_runs", markers=True,hover_data=[scores.index, "Innings",'batsman_runs'])
        fig.update_xaxes(showgrid=False)
        # fig.data[0].line.color = 'rgb(255,0,0)'


    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"),width=900, height=400, margin=dict(t=10, b=20))
    return fig


def get_performance_bowling(player,season):
    """This function will return
    the plots of bowler's performance"""

    if (season != 'Overall'):
        scores = bowling_card.loc[(bowling_card['bowler'] == player) &
                               (bowling_card['season'] == season), "bowler's_wicket"].reset_index(drop=True)
        fig = px.histogram(scores, x="bowler's_wicket")

    else:
        scores = bowling_tally_season.loc[
            bowling_tally_season['bowler'] == player, ['season', 'wickets','match']]
        scores.sort_values(by='season',inplace=True)
        scores.season = scores.season.astype(str)
        fig = px.line(scores, x=scores.season, y="wickets", markers=True,hover_data=[scores.season, "match",'wickets'])
        fig.update_xaxes(showgrid=False)
        # fig.data[0].line.color = 'rgb(255,0,0)'


    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"),width=900, height=400, margin=dict(t=10, b=20))
    return fig