import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandasql import sqldf

def main():
    title_placeholder = st.empty()
    title_placeholder.title("Box Office: Top Movies Worldwide All-time")
    df = pd.read_csv('movies_dataset.csv',skiprows=lambda x: x not in range(21))
    df = df.drop('Gross',axis=1)
    df=df.rename(columns = {'Year of Realease':'Year of Release'})
    movie_titles = []
    for mov in df['Movie Title']:
        movie_titles.append(mov)

    split_genres_df = df.assign(Genre=df['Genre'].str.split(',')).explode('Genre').reset_index(drop=True)
    
    # Write the SQL query to group movie titles by genres
    query = """
        SELECT
            Genre,
            "Movie Title"
        FROM
            split_genres_df
    """
    # Execute the SQL query and store the result in a new df
    result_df = sqldf(query)
    # Group movie titles by genre and store them in a dictionary
    genres = result_df.groupby('Genre')['Movie Title'].apply(list).to_dict()
    
    option = st.sidebar.selectbox(
        'Which movie would you like to select?',
        (['Select']+movie_titles))

    if option != 'Select':
        index = df.index[df['Movie Title'] == option][0]
        title_placeholder.title(option)
        gs = df['Genre'][index].split(',')
        genre = df['Genre'][index]
        g = ", ".join(genre.split(','))
        st.write(g,'\n*~',df['Logline'][index]+'*\n')
        
        st.write('With a worldwide gross of',df['Worldwide LT Gross'][index]+',',option, 'is #<b>' + str(1 + index) + '</b> on the list of highest grossing movies of all time.\n\n', unsafe_allow_html=True)
        for g in gs:
            with st.expander(g+' Movies'):
                for movie in genres[g]:
                    st.write(movie)
        # graph
        df['Worldwide LT Gross'] = df['Worldwide LT Gross'].str.replace(',', '')
        df['Worldwide LT Gross'] = df['Worldwide LT Gross'].str.replace('$', '').astype(int)
        df['Votes'] = df['Votes'].str.replace(',', '').astype(int)
       
        numeric = df.select_dtypes(include=np.number)

        graph_var = st.selectbox("Select attribute?",(numeric.columns))
        df.sort_values(by=graph_var, ascending=False, inplace=True)
        units = {'Votes':'','Worldwide LT Gross':'($)','Year of Release':'','Movie Rating':'(/10)','Metascore':'(/100)','Duration':'(min)'}
        fig = px.bar(x=df['Movie Title'],y=df[graph_var], labels=dict(x="Movie", y=graph_var+' '+units[graph_var]))
        if graph_var == 'Year of Release':
            fig.update_yaxes(range=[1995, 2023])
        fig.update_traces(marker=dict(color=[px.colors.qualitative.Plotly[3] if x == option else px.colors.qualitative.Plotly[0] for x in df['Movie Title']]))
        fig.update_xaxes(tickangle=45)
        tickformat_str = f"{{:0<10}}"
        fig.update_layout(xaxis_tickformat=tickformat_str)
        st.plotly_chart(fig)
    else:
        st.write(df)




if __name__ == "__main__":
    main()
