import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandasql import sqldf

def get_df():
    # read csv file
    df = pd.read_csv('movies_dataset.csv',skiprows=lambda x: x not in range(21))
    # clean up 
    df = df.drop('Gross',axis=1)
    df=df.rename(columns = {'Year of Realease':'Year of Release'})
    return df

def genre_movies(df,index):
    gs = df['Genre'][index].split(', ')
    for g in gs:
        # Create the query
        query = '''
            SELECT "Movie Title"
            FROM df
            WHERE "Genre" LIKE '%{}%'
        '''.format(g)
        # add expander option for user
        with st.expander(g + ' Movies'):
            result_df = sqldf(query)
            for movie in result_df['Movie Title']:
                st.write(movie)
            
def graph(df,option):
    # make columns numeric
    df['Worldwide LT Gross'] = df['Worldwide LT Gross'].str.replace(',', '')
    df['Worldwide LT Gross'] = df['Worldwide LT Gross'].str.replace('$', '').astype(int)
    df['Votes'] = df['Votes'].str.replace(',', '').astype(int)
    numeric = df.select_dtypes(include=np.number)
    # create dicstionary for units of columns
    units = {'Votes':'','Worldwide LT Gross':'($)','Year of Release':'','Movie Rating':'(/10)','Metascore':'(/100)','Duration':'(min)'}

    # allow user to select attribute for graph
    graph_var = st.selectbox("Select attribute",(numeric.columns))
    # descending order
    df.sort_values(by=graph_var, ascending=False, inplace=True)
    fig = px.bar(x=df['Movie Title'],y=df[graph_var], labels=dict(x="Movie", y=graph_var+' '+units[graph_var]))
    # scale y axis for year
    if graph_var == 'Year of Release':
        fig.update_yaxes(range=[1995, 2023])
    # make current movie a different bar colour
    fig.update_traces(marker=dict(color=[px.colors.qualitative.Plotly[3] if x == option else px.colors.qualitative.Plotly[0] for x in df['Movie Title']]))
    # display movie names diagonally
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

def movie_selected(df,title_placeholder,option):
    # search through datset to find which row of csv the selected movie is in
    index = df.index[df['Movie Title'] == option][0]
    # change title
    title_placeholder.title(option)
    # add a space after comma
    df['Genre'] = df['Genre'].str.replace(',', ', ')
    # write genre and logline
    st.write(df['Genre'][index],'\n*~',df['Logline'][index]+'*\n')
    # write gross    
    st.write('With a worldwide gross of',df['Worldwide LT Gross'][index]+',',option, 'is #<b>' + str(1 + index) + '</b> on the list of highest grossing movies of all time.\n\n', unsafe_allow_html=True)
    # add other movies of the same genre
    genre_movies(df,index)
    # graph
    graph(df,option)

def main():
    # set an adjustable title
    title_placeholder = st.empty()
    title_placeholder.title("Box Office: Top Movies Worldwide All-time")
    # get df
    df = get_df()

    # get list of movie names to use in selectbox
    movie_titles = []
    for mov in df['Movie Title']:
        movie_titles.append(mov)
    # create selectbox
    option = st.sidebar.selectbox(
        'Which movie would you like to select?',
        (['Select']+movie_titles))

    # if user picks a movie
    if option != 'Select':
        movie_selected(df,title_placeholder,option)
    # if user doesn't
    else:
        st.write(df)

if __name__ == "__main__":
    main()
