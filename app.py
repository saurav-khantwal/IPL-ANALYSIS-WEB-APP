import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import send


st.sidebar.title('IPL ANALYSIS')
user_menu=st.sidebar.radio(
    'select an option',
    ('Match details','Team details','player details')
)


#*********************************************************************************************************************
                                                # MATCH DETAILS CODE SECTION
# *********************************************************************************************************************


if(user_menu=='Match details'):

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

        #********Phase plot of Teams

        st.title("Run scored in different Phases")
        st.subheader('First Innings - ' + send.get_team_name(match_id, 1, 'inning', 'batting') + ' ' + send.get_total(match_id,1,'inning'))
        fig1=send.get_phase_plot(match_id,1)
        st.plotly_chart(fig1)

        st.subheader('Second Innings - ' + send.get_team_name(match_id, 2, 'inning', 'batting') + ' ' + send.get_total(match_id,2,'inning'))
        fig2=send.get_phase_plot(match_id,2)
        st.plotly_chart(fig2)
        st.write('')

        #*******Run worm of teams

        st.title("Worm plot")
        fig1 = send.get_worm_plot(match_id)
        st.plotly_chart(fig1)

    #*********************************************************************************************************************
                                                    # TEAM ANALYSIS CODE SECTION
    # *********************************************************************************************************************