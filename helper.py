import numpy as np
import streamlit
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px


def medal_tell(df):
    medal_telly = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # Group by based on NOC
    medal_telly = medal_telly.groupby('region').sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",
                                                                                                ascending=False).reset_index()
    medal_telly['total'] = medal_telly['Gold'] + medal_telly['Silver'] + medal_telly['Bronze']

    return medal_telly


def get_yeras_Countries(df):
    # Extract all countries and all years
    county = np.unique(df['region'].dropna().values).tolist()
    county.sort()
    county.insert(0, 'Overall')
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    return county, years


def fetch_medal_tally(df, year, country):
    global temp_df
    medal_telly1 = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_telly1
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_telly1[medal_telly1['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_telly1[medal_telly1['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_telly1[(medal_telly1['Year'] == year) & (medal_telly1['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[["Gold", "Silver", "Bronze"]].sort_values("Year").reset_index()

    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def overall_analysis(df):
    years = df['Year'].unique().shape[0] - 1
    city = df['City'].unique().shape
    events = df['Event'].unique().shape
    participants = df['Name'].unique().shape
    nations = df['region'].unique().shape
    sports = df['Sport'].unique().shape

    return years, city[0], events[0], participants[0], nations[0], sports[0]


def draw_year_nation_plot(df, second):
    listt = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    listt.rename(columns={'count': 'Number Of countries', 'Year': "Edition"}, inplace=True)
    return listt


def data_over_time(df, value):
    list2 = df.drop_duplicates(['Year', value])['Year'].value_counts().reset_index().sort_values('Year')
    list2.rename(columns={'count': value, 'Year': "Edition"}, inplace=True)
    list2.head(1)

    return list2


def most_successful(df, sport):
    temp_dff = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_dff = temp_dff[temp_dff['Sport'] == sport]

    x = temp_dff['Name'].value_counts().reset_index().head(15).merge(df, left_on='count', right_on='Name', how='left')[
        ['count', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'count': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def top_players_by_sport(df, target_sport, top_n=10):
    medal_weights = {'Gold': 1, 'Silver': 1, 'Bronze': 1}

    df['Total_Medals'] = df['Medal'].map(medal_weights).fillna(0)

    if target_sport.lower() == 'overall':
        top_players = df.groupby('Name')['Total_Medals'].sum().reset_index().sort_values(by=['Total_Medals'],
                                                                                         ascending=False).head(top_n)
        top_players['Total_Medals'] = top_players['Total_Medals'].astype('int')
    else:

        sport_df = df.loc[df['Sport'] == target_sport]

        if sport_df.empty:
            print(f"No data available for the sport '{target_sport}'.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is available

        top_players = sport_df.groupby(['Sport', 'Name'])['Total_Medals'].sum().reset_index().sort_values(
            by=['Total_Medals'], ascending=False).head(top_n)
        top_players['Total_Medals'] = top_players['Total_Medals'].astype('int')
    return top_players.reset_index(drop=True)


def year_county(df, country_name):
    temp_df = df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country_name]
    temp = new_df.groupby("Year").count()["Medal"]
    return temp.reset_index()

def county_heatmap(df , county):
    temp_df = df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == county]
    pt = new_df.pivot_table(index = 'Sport' , columns = 'Year' ,values = 'Medal' , aggfunc='count').fillna(0)
    return pt


def age_winning_analysis(df):
    athelete = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelete['Age'].dropna()
    x2 = athelete[athelete['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete[athelete['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete[athelete['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1 , x2,x3,x4], ['Overall Age' , 'Gold Medalist' , 'Silver Medalist' , 'Bronze Medalist'] , show_hist=False , show_rug=False)
    return fig


def gender_analysis(df):
    # Men vs Women winning
    athelete = df.drop_duplicates(subset=['Name', 'region'])
    men = athelete[athelete['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athelete[athelete['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women , on ='Year', how ='left')
    final.fillna(0 , inplace=True)
    final.rename(columns={"Name_x":'Male', "Name_y" : 'Female'} , inplace=True)
    fig = px.line(final , x = 'Year' , y= ['Male' , 'Female'])
    return fig

