import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Análise de Dívidas Municipais', layout='wide')

df = pd.read_csv('./data/MunicipalDebtAnalysis.csv')

sidebar_options = ['Análise Exploratória', 'Colunas', 'Correlação']
sidebar_selection = st.sidebar.radio('Escolha uma opção:', sidebar_options)

if sidebar_selection == 'Análise Exploratória':
    st.title('Análise Exploratória')
    st.write("Para este estudo, \
         foi utilizada uma base de dados de dívidas municipais de \
         8 cidades Sul-Africanas, disponível no site Kaggle.")
    st.write(df.head())

    # Show the distribution of numerical columns
    st.subheader('Distribuição das colunas numéricas')
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    for col in num_cols:
        fig, ax = plt.subplots()
        sns.histplot(df[col], ax=ax)
        st.pyplot(fig)

# Columns page
elif sidebar_selection == 'Colunas':
    st.title('Colunas')

    # Column selection
    col_options = df.columns.tolist()
    col_selection = st.selectbox('Select a column:', col_options)

    # Show column statistics
    st.subheader(f'Estatísticas de cada coluna {col_selection}')
    st.write(df[col_selection].describe())

    # Show a histogram of the column
    fig, ax = plt.subplots()
    sns.histplot(df[col_selection], ax=ax)
    st.pyplot(fig)

# Correlation page
elif sidebar_selection == 'Correlação':
    st.title('Análise de Correlação')

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
