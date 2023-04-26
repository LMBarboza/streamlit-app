import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

st.set_page_config(page_title='Análise de Dívidas Municipais', layout='wide')

df = pd.read_csv('./data/MunicipalDebtAnalysis.csv')


sidebar_options = ['Introdução', 'Análise Exploratória', 'Modelos']
sidebar_selection = st.sidebar.radio('', sidebar_options)

if sidebar_selection == 'Introdução':
    st.title('Análise de Dívidas Municipais')
    st.header('Objetivos e motivação')
    st.write('A análise exploratória de dados (AED) é uma técnica utilizada para entender\
            melhor um conjunto de dados, identificando padrões, tendências e relações entre\
            as variáveis do conjunto de dados. A AED ajuda\
            a explorar as informações contidas nos dados e a obter insights\
            valiosos que podem ser usados para tomar decisões informadas.\
            Neste contexto, realizamos uma AED em um conjunto de dados referentes à cobrança de dívida de 8 municipalidades\
            sul-africanas. O objetivo principal desta análise foi identificar os principais padrões e tendências nos dados.')
    st.header('Detalhes do conjunto de dados')
    st.write('A base usada para essa análise poder ser encontrada no site Kaggle\
            (https://www.kaggle.com/datasets/dmsconsultingsa/municipal-debt-risk-analysis). Ela contém informações\
            sobre os devedores, como, tipo de propriedade, valor e tamanho da propriedade e sobre a dívida, valor total\
            \
            ,total recebido, entre outras. Além disso, há uma classificação binária entre boas e más dívidas.')

elif sidebar_selection == 'Análise Exploratória':
    st.title('Análise Exploratória de Dados')
#explicar cada coluna, numero de dados, dados com registro, dados com classificação, média e outras coisas 
#de colunas que façam sentido, gráficos e matriz de correlação 
    col_options = df.columns.tolist()
    col_selection = st.selectbox('Select a column:', col_options)

    st.subheader(f'Estatísticas de cada coluna {col_selection}')
    st.write(df[col_selection].describe())
    fig, ax = plt.subplots()
    sns.histplot(df[col_selection], ax=ax)
    st.pyplot(fig)

# Correlation page
elif sidebar_selection == 'Modelos':
    st.title('Modelos de classificação')

    # Correlation matrix
    corr = df.corr()

    # Show the correlation matrix as a heatmap
    st.subheader('Correlation Matrix')
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Show the top correlated pairs of columns
    st.subheader('Top Correlated Pairs of Columns')
    k = st.slider('Select the number of top pairs to display:', 1, len(corr), 5, 1)
    corr_pairs = corr.abs().unstack().sort_values(ascending=False).drop_duplicates()
    corr_pairs = corr_pairs[corr_pairs != 1]
    corr_pairs = corr_pairs.reset_index().rename(columns={'level_0': 'Column 1', 'level_1': 'Column 2', 0: 'Correlation'})
    corr_pairs = corr_pairs.head(k)
    st.write(corr_pairs)
