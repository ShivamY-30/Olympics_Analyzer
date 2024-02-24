import helper as helper
import streamlit as st
import pandas as pd
import preprocessor , helper
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('Resources/athlete_events.csv')
region_df = pd.read_csv('Resources/noc_regions.csv')

df = preprocessor.preprocessor(df ,region_df)
st.sidebar.header("Olympics Data Analysis")
st.sidebar.image('Resources/pngf.jpg' , width=200)
crieteria = st.sidebar.radio("Select Crieteria",
                                 ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athelete-Wise Analysis'))




if crieteria == 'Medal Tally':
    medal_telly = helper.medal_tell(df)
    country , year = helper.get_yeras_Countries(df)
    Country = st.sidebar.selectbox("Select Country" , (country))
    Year = st.sidebar.selectbox("Select Year" , (year))
    # st.dataframe(medal_telly)
    if Country == 'Overall' and Year == 'Overall':
        st.title("Overall Study")
    if Country != 'Overall' and Year == 'Overall':
        st.title("Overall Performance of  " + Country)
    if Country == 'Overall' and Year != 'Overall':
        st.title("Performance of Overall Countries in " + str(Year) )
    if Country != 'Overall' and Year != 'Overall':
        st.title("Performance of "+ Country +" in " + str(Year) )
    x = helper.fetch_medal_tally(df , Year, Country)
    st.table(x)

if crieteria == 'Overall Analysis':
    years , city , events, participants,nations , sports= helper.overall_analysis(df)
    st.title("Overall Analysis")
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(years)
    with col2:
        st.header("Countries")
        st.title(nations)
    with col3:
        st.header("Participants")
        st.header(participants)
    st.markdown("---")
    col4 , col5 , col6 = st.columns(3)
    with col4:
        st.header("Sports")
        st.title(sports)
    with col5:
        st.header("Hosts")
        st.title(city)
    with col6:
        st.header("Events")
        st.title(events)
    st.markdown("---")

    region = helper.data_over_time(df ,"region")
    st.title("Over the Years Participation of Countries")
    fig = px.line(region , x = "Edition", y = "region" )
    st.plotly_chart(fig)


    Event = helper.data_over_time(df ,"Event")
    st.title("Over the Years Addition of Events")
    fig = px.line(Event , x = "Edition", y = "Event" )
    st.plotly_chart(fig)




    Name = helper.data_over_time(df ,"Name")
    st.title("Over the Years Participation of Atheletes")
    fig = px.line(Name , x = "Edition", y = "Name" )
    st.plotly_chart(fig)


    Sport = helper.data_over_time(df ,"Sport")
    st.title("Over the Years Changes in No of Sports")
    fig = px.line(Sport , x = "Edition", y = "Sport" )
    st.plotly_chart(fig)



    st.title("Top Players Based on Medal Winss")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0 , "overall")
    selected_Sport = st.selectbox("Select Name of Participant" , sport_list)

    df_result = helper.top_players_by_sport(df, selected_Sport, top_n=10)
    st.table(df_result)


if crieteria == 'Country-Wise Analysis':
    st.title("Find The Graph for Yearly wise winning of the countries in Olympics")
    country_list = np.unique(df['region'].dropna().values).tolist()
    country_list.sort()
    selected_Country = st.selectbox("Select Name of Country" , country_list)
    click = st.button("Analyze")
    if click:
        graph = helper.year_county(df , selected_Country)
        st.dataframe(graph)
        st.title("Graph Chart Analysis")
        fig = px.line(graph , x = "Year", y = "Medal" )
        st.plotly_chart(fig)

        try:
            pt = helper.county_heatmap(df , selected_Country)
            fig , ax = plt.subplots(figsize = (20 ,20))
            st.title("HeatMap Analysis Each countries best Sport")
            ax = sns.heatmap(pt, annot= True)
            st.pyplot(fig)
        except:
            st.header("Selected country has not won any Olympics medal so far..")

if crieteria == 'Athelete-Wise Analysis':
    ##################################################
    # Athelete wise analysis
    st.title("Age wise Analysis of winning Probability")
    fig = helper.age_winning_analysis(df)
    st.plotly_chart(fig)



    st.title("Gender Wise Analysis")
    fig1 = helper.gender_analysis(df)
    st.plotly_chart(fig1)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: rgb(14, 17, 23);;
color: white;
text-align: center;

}
p , a{
text-align:center;
color: white;
}
</style>
<div class="footer">
<hr>
<p>Developed by :  <a style=' text-align: center;' href="http://myiportfolio.000webhostapp.com/index.php" target="_blank">Shivam Yadav</a></p>
<p>Contact for details and discussion :  <a style='text-align: center;' target="_blank">yadavshivamp90671@gmail.com</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)





