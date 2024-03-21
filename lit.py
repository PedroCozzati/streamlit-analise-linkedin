from collections import Counter
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import altair as alt


st.set_page_config(
    page_title="Análise de dados de vagas do linkedin",  # Title of your app
    page_icon=":chart_with_upwards_trend:",  # Icon for your app
    layout="wide",  # Layout mode ("wide" or "centered")
    # initial_sidebar_state="expanded",  # Initial state of the sidebar ("expanded" or "collapsed")
)

conn = sqlite3.connect('dados_analitico.db')

query = "SELECT * FROM vagas;"


# Ler os dados do banco de dados SQLite para um DataFrame do Pandas
dados = pd.read_sql_query(query, conn)

# Fechar a conexão com o banco de dados
conn.close()

dados_nao_nulos = dados
dados_nao_nulos=dados_nao_nulos.drop_duplicates(subset='job_id')

df = dados_nao_nulos[dados_nao_nulos.requisitos != 'Não especificado']

# # Explodir a coluna 'tecnologia'
df = df.assign(requisitos=df['requisitos'].str.split(', ')).explode('requisitos')

# # Contar ocorrências de cada tecnologia
count_tecnologia = df['requisitos'].value_counts()
df_temp = dados_nao_nulos[dados_nao_nulos.requisitos!="Não especificado"]


value_counts_df = df.requisitos.value_counts().reset_index()
value_counts_df.columns = ['requisitos', 'count']  # Rename columns for clarity

st.title('Análise de dados de vagas do Linkedin')

st.subheader('Dataframe')
st.dataframe(dados_nao_nulos)
# Create the Altair chart
c = alt.Chart(data=value_counts_df[:10]).mark_bar().encode(
    x=alt.X('requisitos',sort=None),  # X-axis: the requisitos
    y=alt.Y('count:Q'),  # Y-axis: the count of each requisitos
    color='requisitos',  # Color the bars by the 'site' column
    order=alt.Order(
        # Sort the segments of the bars by this field
        'count',
        sort='descending'
    )
)

st.divider()

data_container = st.container()

with data_container:
    table, plot = st.columns((1, 3),gap='small')
    with table:
        st.dataframe(value_counts_df)
    with plot:
        st.subheader('TOP 10 Tecnologias mais pedidas')
        st.altair_chart(c, use_container_width=True)

# Render the chart using Streamlit

value_counts_df2 = dados_nao_nulos.posicao.value_counts().reset_index()
value_counts_df2.columns = ['posicao', 'count']  

# Create the Altair chart
d = alt.Chart(data=value_counts_df2).mark_bar().encode(
    x=alt.X('posicao',sort=None),  # X-axis: the requisitos
    y=alt.Y('count:Q'),  # Y-axis: the count of each requisitos
    color='posicao',  # Color the bars by the 'site' column
    order=alt.Order(
        # Sort the segments of the bars by this field
        'count',
        sort='descending'
    )
)

st.divider()

data_container = st.container()

with data_container:
    table, plot = st.columns((1, 3),gap='small')
    with table:
        st.dataframe(value_counts_df2)
    with plot:
        st.subheader('Posições mais frequentes nas vagas')
        st.altair_chart(d, use_container_width=True)


value_counts_df3 = dados_nao_nulos.company.value_counts().reset_index()
value_counts_df3.columns = ['company', 'count']  

# Create the Altair chart
e = alt.Chart(data=value_counts_df3[:5]).mark_arc().encode(
    theta='count',
    color='company',  # Color the bars by the 'site' column
    order=alt.Order(
        # Sort the segments of the bars by this field
        'count',
        sort='descending'
    )
)

st.divider()

data_container = st.container()

with data_container:
    table, plot = st.columns((1, 3),gap='small')
    with table:
        st.dataframe(value_counts_df3)
    with plot:
        st.subheader('Empresas ou contratantes mais presentes')
        st.altair_chart(e, use_container_width=True)
