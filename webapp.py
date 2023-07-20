import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def main():
    title_placeholder = st.empty()
    title_placeholder.title("Box Office: Top Movies Worldwide All-time")
    df = pd.read_csv('movies_dataset.csv',skiprows=lambda x: x not in range(21))
    df['Votes'] = df['Votes'].str.replace(',', '').astype(int)
    numeric = df.select_dtypes(include=np.number)
    # print(numeric.columns)
    # print(df.dtypes)
    movie_titles = []
    for mov in df['Movie Title']:
        movie_titles.append(mov)

    option = st.sidebar.selectbox(
        'Which movie would you like to select?',
        (['Select']+movie_titles))

    if option != 'Select':
        index = df.index[df['Movie Title'] == option][0]
        title_placeholder.title(option)
        st.write('\n*~~',df['Logline'][index],'~~*\n')
        st.write(option, 'is #<b>' + str(1 + index) + '</b> on the list of highest grossing movies of all time.\n\n', unsafe_allow_html=True)
        graph_var = st.selectbox("What variable do you want to view a graph of?",(numeric.columns))
        fig = px.bar(x=df['Movie Title'],y=df[graph_var], labels=dict(x="Movie", y=graph_var))
        if graph_var == 'Year of Realease':
            fig.update_yaxes(range=[1995, 2023])
        fig.update_traces(marker=dict(color=[px.colors.qualitative.Plotly[3] if x == option else px.colors.qualitative.Plotly[0] for x in df['Movie Title']]))
        fig.update_xaxes(tickangle=45)
        tickformat_str = f"{{:0<10}}"
        fig.update_layout(xaxis_tickformat=tickformat_str)
        st.plotly_chart(fig)




if __name__ == "__main__":
    main()
