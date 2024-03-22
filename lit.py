from collections import Counter
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
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
st.subheader('Quantidade de vagas no banco de dados: '+ str(len(dados_nao_nulos)))
st.subheader('Dataframe')
st.dataframe(dados_nao_nulos[['title', 'register_date','company','applications','location','posicao','requisitos','beneficios','tipo_vaga','link','description']])
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

df3_data = value_counts_df3[:5]

df3_data['percentage'] = (df3_data['count'] / df3_data['count'].sum()) * 100

e = alt.Chart(data=df3_data[:5]).mark_arc().encode(
    alt.Theta('percentage:Q').stack(True),
    alt.Color('company:N'),
    order=alt.Order(
        'count',
        sort='descending'
    ),
    tooltip=['company', 'count', 'percentage']  
)
pie2 = e.mark_arc(outerRadius=100)
text2 = e.mark_text(radius=130, size=18).encode(text=alt.Text('percentage:Q', format='.2f'))

final_chart2=pie2 + text2

value_counts_df4 = dados_nao_nulos.tipo_vaga.value_counts().reset_index()
value_counts_df4.columns = ['tipo_vaga', 'count']  

value_counts_df4['percentage'] = (value_counts_df4['count'] / value_counts_df4['count'].sum()) * 100

f = alt.Chart(data=value_counts_df4).mark_arc().encode(
    alt.Theta('percentage:Q').stack(True),
    alt.Color('tipo_vaga:N'),
    order=alt.Order(
        'count',
        sort='descending'
    ),
    tooltip=['tipo_vaga', 'count', 'percentage']  
)
pie3 = f.mark_arc(outerRadius=100)
text3 = f.mark_text(radius=130, size=18).encode(text=alt.Text('percentage:Q', format='.2f'))

final_chart3=pie3 + text3

st.divider()

data_container = st.container()

with data_container:
    table, plot,table2,plot2 = st.columns((1, 2, 1, 2),gap='small')
    with table:
        st.dataframe(value_counts_df3)
    with plot:
        st.subheader('Empresas ou contratantes mais frequentes')
        st.altair_chart(final_chart2, use_container_width=True)
    with table2:
        st.dataframe(value_counts_df4)
    with plot2:
        st.subheader('Porcentagem de tipos de Vaga')
        st.altair_chart(final_chart3, use_container_width=True)
        
dados_temp2 = dados_nao_nulos

dados_com_beneficio = dados_temp2[dados_temp2['beneficios'] != "Não especificado"]
# dados_com_beneficio.columns = ['title', 'company','location','beneficios','tipo_vaga']  

dados_temp2['tem_beneficio'] = dados_temp2['beneficios'] != "Não especificado"
dados_temp2['tem_beneficio'] = dados_temp2['tem_beneficio'].map({True: 'SIM', False: 'NÃO'})

value_counts_df5 = dados_temp2.tem_beneficio.value_counts().reset_index()
value_counts_df5.columns = ['tem_beneficio', 'count']  

# Create the Altair chart

value_counts_df5['percentage'] = (value_counts_df5['count'] / value_counts_df5['count'].sum()) * 100

# Criar o gráfico de arco
g = alt.Chart(data=value_counts_df5).mark_arc().encode(
    alt.Theta('percentage:Q').stack(True),
    alt.Color('tem_beneficio:N'),
    order=alt.Order(
        # Sort the segments of the bars by this field
        title="TEM BENEFÍCIO ESPECIFICADO?"
        'count',
        sort='descending'
    ),
    tooltip=['tem_beneficio', 'count', 'percentage']  # Adicionar tooltip com informações
)
pie = g.mark_arc(outerRadius=100)
text = g.mark_text(radius=130, size=18).encode(text=alt.Text('percentage:Q', format='.2f'))

final_chart=pie + text

st.divider()

data_container = st.container()

with data_container:
    table, plot,table2= st.columns((1, 2, 3),gap='small')
    with table:
        st.dataframe(value_counts_df5)
    with plot:
        st.subheader('Porcentagem de vagas com benefícios especificados')
        st.altair_chart(final_chart, use_container_width=True)
    with table2:
        st.subheader('Dataframe de vagas com benefícios especificados')
        st.dataframe(dados_com_beneficio[['title', 'company','location','beneficios','tipo_vaga','link']])
    
        