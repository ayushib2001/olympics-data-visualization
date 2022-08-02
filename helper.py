import numpy as np
import pandas as pd


def country_year_list(df) :
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

def fetch_medal_tally(df, year, country) :
    flag = 0
    medal_df = df.drop_duplicates(subset = ['Team', 'NOC', 'Year','City', 'Sport', 'Event', 'Medal'])
    if(year == 'Overall' and country == 'Overall') :
        temp_df = medal_df
        
    if(year == 'Overall' and country != 'Overall') :
        flag=1
        temp_df = medal_df[medal_df['region'] == country]
    
    if(year != 'Overall' and country == 'Overall') :
        temp_df = medal_df[medal_df['Year'] == int(year)]
    
    if(year != 'Overall' and country != 'Overall') :
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
        
    if(flag == 1) :
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index() 
    else :
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Total'] = x['Total'].astype(int)
    return x

def data_over_time(df,col) :
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index' : "Edition", 'Year' : 'No of '+col}, inplace=True)

    return nations_over_time

def no_of_athletes_over_time(df,col) :
    athletes_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    athletes_over_time.rename(columns={'index' : "Edition", 'Year' : 'No of athletes'}, inplace=True)

    return athletes_over_time

def most_successful(df, sport) :
    temp_df = df.dropna(subset = ['Medal'])
    
    if(sport != 'Overall') :
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on= 'index', right_on='Name', 
                    how = 'left')[['index','Name_x','Sport','region']].drop_duplicates('index').reset_index()
    x.drop('level_0',axis=1,inplace=True)
    x.rename(columns={'index' : 'Name', 'Name_x' : 'No. of medals'}, inplace=True)
    return x


def yearwise_medal_tally(df, country) :
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team','NOC','Year', 'City', 'Sport','Event', 'Medal'],inplace=True)
    if(country != 'Overall') :
        temp_df = temp_df[temp_df['region'] == country]
    
    final_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    final_df.rename(columns={'Medal' : 'No of medals'},inplace=True)

    return final_df

def country_event_heatmap(df, country) :
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team','NOC','Year', 'City', 'Sport','Event', 'Medal'],inplace=True)
    if(country != 'Overall') :
        temp_df = temp_df[temp_df['region'] == country]

    pt = temp_df.pivot_table(index = 'Sport', columns='Year', values = 'Medal', aggfunc='count').fillna(0).astype(int)

    return pt

def most_successful_countrywise(df, country) :
    temp_df = df.dropna(subset = ['Medal'])
    
    if(country != 'Overall') :
        temp_df = temp_df[temp_df['region'] == country]
        
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on= 'index', right_on='Name', 
                    how = 'left')[['index','Name_x','Sport','region']].drop_duplicates('index').reset_index()
    x.drop('level_0',axis=1,inplace=True)
    x.rename(columns={'index' : 'Name', 'Name_x' : 'No. of medals'}, inplace=True)
    return x

def male_v_female_overtime(df) :
    new_df = df.drop_duplicates(subset = ['Team', 'Year', 'Name','region'])
    gender_participation = pd.DataFrame(new_df.groupby('Year')['Sex'].value_counts())
    gender_participation.rename(columns={'Sex' : 'No of participants'},inplace = True)
    gender_participation.reset_index(inplace = True)

    return gender_participation


def weight_and_height(df,sport) :
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])
    temp_df = athlete_df
    if (sport != 'Overall') :
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    return temp_df
    