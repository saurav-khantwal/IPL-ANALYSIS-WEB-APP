import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import send


st.set_page_config(page_title=None, page_icon=None, layout='wide', initial_sidebar_state='auto')

st.sidebar.title('IPL ANALYSIS')
user_menu=st.sidebar.radio(
    'select an option',
    ('MATCH STATISTICS','IPL STATISTICS','PLAYER STATISTICS')
)


#*********************************************************************************************************************
                                                # MATCH STATS CODE SECTION
# *********************************************************************************************************************


if(user_menu=='MATCH STATISTICS'):

    col1, col2,col3= st.columns([5,1,2])
    years=send.match_df['season'].sort_values().unique().tolist()
    years.insert(0,'All Time')
    match=send.send_match()
    with col3:
        st.text('')
        st.text('')
        rd_match_type=st.radio('select match type',('All Matches','League Matches','Playoff Matches','Final Matches'))
    with col1:
        sb_season = st.selectbox('Select Season', years)
        sb_match=st.selectbox('Select Match',send.send_filtered_match(match,sb_season,rd_match_type))

    match_id=match[match['Match']==sb_match]['id'].unique()[0]

    # Expander window for the match Summary

    expand_summary=st.expander(label='Show Match Summary')
    try:
        with expand_summary:
            c1,c2,c3=st.columns(3)

            with c1:
                st.subheader(send.get_team_name(match_id,1,'home','batting'))
                st.write((send.get_total(match_id,1,'home')) + ' |  ' +
                         send.get_total_overs(match_id,1))
            with c2:
                pass

            with c3:
                st.subheader(send.get_team_name(match_id,2,'home','batting'))
                st.write((send.get_total(match_id,2,'home')) + ' |  ' +
                         send.get_total_overs(match_id,2))

            st.subheader(send.get_result(match_id))
            st.write(send.get_mom(match_id))

    except:
        st.header("Sorry can't fetch data")



    # Window for the scorecard

    # Expander window for batting card

    expand_batting_card = st.expander(label='Show Batting Card')

    try:
        with expand_batting_card:
            st.header('First Innings - ' + send.get_team_name(match_id,1,'inning','batting'))
            st.table(send.get_scorecard(match_id,1,'batting').style.format(subset=['strike_rate'], formatter="{:.1f}"))
            st.header('Second Innings - ' + send.get_team_name(match_id,2,'inning','batting'))
            st.table(send.get_scorecard(match_id,2,'batting').style.format(subset=['strike_rate'], formatter="{:.1f}"))

    except:
        st.header("Sorry can't fetch data")


    #Expander window for bowling card

    expand_bowling_card = st.expander(label='Show Bowling Card')
    try:
        with expand_bowling_card:
            st.header('Bowling - ' + send.get_team_name(match_id,1,'inning','bowling'))
            st.table(send.get_scorecard(match_id, 1,'bowling').style.format(subset=['economy'], formatter="{:.1f}"))
            st.header('Bowling - ' + send.get_team_name(match_id,2,'inning','bowling'))
            st.table(send.get_scorecard(match_id,2,'bowling').style.format(subset=['economy'], formatter="{:.1f}"))

    except:
        st.header("Sorry can't fetch data")


    # Expander window for match analysis

    expand_match_analysis= st.expander(label='Show Match Analysis')
    with expand_match_analysis:

        #*******run contribution of player pie chart

        st.title("Run contribution of players in the Total")
        st.subheader('First Innings - ' + send.get_team_name(match_id, 1, 'inning', 'batting') + ' ' + send.get_total(match_id,1,'inning'))
        fig1=send.get_contribution_plot(match_id,1)
        st.plotly_chart(fig1)

        st.subheader('Second Innings - ' + send.get_team_name(match_id, 2, 'inning', 'batting') + ' ' + send.get_total(match_id,2,'inning'))
        fig2=send.get_contribution_plot(match_id,2)
        st.plotly_chart(fig2)
        st.write('')

        #*******Bar plot teams

        st.title("Bar plot of runs throughout the Innings")
        st.subheader('First Innings - ' + send.get_team_name(match_id, 1, 'inning', 'batting') + ' ' + send.get_total(match_id,1,'inning'))
        fig1=send.get_bar_plot(match_id,1)
        st.plotly_chart(fig1)

        st.subheader('Second Innings - ' + send.get_team_name(match_id, 2, 'inning', 'batting') + ' ' + send.get_total(match_id,2,'inning'))
        fig2=send.get_bar_plot(match_id,2)
        st.plotly_chart(fig2)
        st.write('')

        #********Phase plot of Runs scored

        st.title("Run scored in different Phases")
        st.subheader('First Innings - ' + send.get_team_name(match_id, 1, 'inning', 'batting') + ' ' + send.get_total(match_id,1,'inning'))
        fig1=send.get_phase_plot(match_id,1,'batting')
        st.plotly_chart(fig1)

        st.subheader('Second Innings - ' + send.get_team_name(match_id, 2, 'inning', 'batting') + ' ' + send.get_total(match_id,2,'inning'))
        fig2=send.get_phase_plot(match_id,2,'batting')
        st.plotly_chart(fig2)
        st.write('')

        #********Phase plot of Wickets taken

        st.title("Wickets Taken in different Phases")
        st.subheader('First Innings - ' + send.get_team_name(match_id, 1, 'inning', 'batting') + ' ' + send.get_total(match_id,1,'inning'))
        fig1=send.get_phase_plot(match_id,1,'bowling')
        if(fig1==0):
            st.header('Team did not lose any wicket')
        else:
            st.plotly_chart(fig1)

        st.subheader('Second Innings - ' + send.get_team_name(match_id, 2, 'inning', 'batting') + ' ' + send.get_total(match_id,2,'inning'))
        fig2=send.get_phase_plot(match_id,2,'bowling')
        if (fig2 == 0):
            st.text('Team did not lose any wicket')
        else:
            st.plotly_chart(fig2)
        st.write('')

        #*******Run worm of teams

        st.title("Worm plot")
        fig1 = send.get_worm_plot(match_id)
        st.plotly_chart(fig1)

    #*********************************************************************************************************************
                                                    # OVERALL STATS CODE SECTION
    # *********************************************************************************************************************


if(user_menu=='IPL STATISTICS'):

    col1,col2=st.columns(2)
    with col1:
        years = send.match_df['season'].sort_values().unique().tolist()
        years.insert(0, 'All Time')
        sb_season=st.selectbox('Select Season',years)
    if(sb_season=='All Time'):
        st.header("Overall Run Tally")
    else:
        st.header("Run tally of season " + str(sb_season))
    st.text(' ')
    cb_runs=st.checkbox(label='Show Full Run Tally')
    st.table(send.get_run_tally(cb_runs,sb_season).style.format(subset=['Average','strike_rate'], formatter="{:.1f}"))

    if (sb_season == 'All Time'):
        st.header("Overall Wicket Tally")
    else:
        st.header("Wicket tally of season " + str(sb_season))
    st.text(' ')
    cb_wickets=st.checkbox(label='Show Full Wicket Tally')
    st.table(send.get_wicket_tally(cb_wickets,sb_season).style.format(subset=['economy'], formatter="{:.2f}"))




    #*********************************************************************************************************************
                                                    # PLAYER STATS CODE SECTION
    # *********************************************************************************************************************


if(user_menu=='PLAYER STATISTICS'):
    st.title('Player Analysis')
    col1,col2=st.columns(2)
    with col1:
        sb_player=st.selectbox('Select player',send.get_player_list())
    with col2:
        sb_season=st.selectbox('Select season',send.get_player_season(sb_player))

    expander_batting=st.expander(label='Batting statistics')

    # Batting statistics of a player

    with expander_batting:
        stats = send.get_batting_stats(sb_player, sb_season)
        if(stats.shape[0]==0):
            st.subheader('Did not Bat')
        else:
            col1,col2,col3,col4=st.columns(4)
            with col1:
                st.header('Batsman')
                st.subheader(stats['batsman'].unique()[0])
                st.write(' ')
                st.header('Strike Rate')
                st.subheader(stats['strike_rate'].unique()[0])
            with col2:
                st.header('Innings')
                st.subheader(stats['Innings'].unique()[0])
                st.write(' ')
                st.header('High Score')
                st.subheader(stats['High_score'].unique()[0])
            with col3:
                st.header('Runs')
                st.subheader(stats['batsman_runs'].unique()[0])
                st.write(' ')
                st.header("50's")
                st.subheader(stats['Half_Centuries'].unique()[0])
            with col4:
                st.header('Average')
                st.subheader(stats['Average'].unique()[0])
                st.write(' ')
                st.header("100's")
                st.subheader(stats['Centuries'].unique()[0])

            #***********************batting analysis plots***************************

            st.write(' ')
            st.write(' ')
            st.title('Batting Analysis')
            st.write(' ')

            #***********Performance plot of batsman

            fig1=send.get_performance_batting(sb_player,sb_season)
            if(fig1==0):
                st.title('Insufficient data to show plot')
            else:
                if(sb_season=='Overall'):
                    st.header(f'Runs scored by {sb_player} over the Seasons')
                else:
                    st.header(f'Runs scored by {sb_player} in season ' + str(sb_season))
                st.plotly_chart(fig1)

            # ***********Phase plot of batsman

            fig1=send.get_performance_phase(sb_player,sb_season,'batting')
            if(fig1==0):
                st.title('Insufficient data to show phase plot')
            else:
                if(sb_season=='Overall'):
                    st.header(f'Runs scored in different Phases by {sb_player}')
                else:
                    st.header(f'Runs scored in different Phases by {sb_player} in season ' + str(sb_season))
                st.plotly_chart(fig1)


    expander_bowling=st.expander(label='Bowling statistics')

    # Bowling statistics of a player

    with expander_bowling:
        stats = send.get_bowling_stats(sb_player, sb_season)
        if(stats.shape[0]==0):
            st.subheader('Did not Bowl')
        else:
            col1,col2,col3,col4,col5,col6=st.columns(6)

            with col1:
                st.header('Innings')
                st.subheader(stats['match'].unique()[0])
            with col2:
                st.header('Wickets')
                st.subheader(stats['wickets'].unique()[0])
            with col3:
                st.header('Economy')
                st.subheader(stats['economy'].unique()[0])
            with col4:
                st.header('Best')
                st.subheader(stats['best'].unique()[0])
            with col5:
                st.header('4W')
                st.subheader(stats['4W Hall'].unique()[0])
            with col6:
                st.header('5W')
                st.subheader(stats['5W Hall'].unique()[0])


            # ***********************bowling analysis plots***************************
            st.write(' ')
            st.write(' ')
            st.title("Bowling Analysis")

            # ***********Performance plot of bowler

            fig1 = send.get_performance_bowling(sb_player, sb_season)
            if(fig1==0):
                st.title('Insufficient data to show plot')
            else:
                if (sb_season == 'Overall'):
                    st.header(f'Wickets taken by {sb_player} over the Seasons')
                else:
                    st.header(f'Wickets taken by {sb_player} in ' + str(sb_season))
                st.plotly_chart(fig1)

            # ***********Phase plot of bowler

            fig1=send.get_performance_phase(sb_player,sb_season,'bowling')
            if(fig1==0):
                st.title('Insufficient data to show phase plot')
            else:
                if(sb_season=='Overall'):
                    st.header(f'Wickets Taken in different Phases by {sb_player}')
                else:
                    st.header(f'Wickets Taken in different Phases by {sb_player} in season ' + str(sb_season))
                st.plotly_chart(fig1)
