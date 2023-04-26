import streamlit as st
import pandas as pd
import numpy as np

#import data and write streamlit app
@st.cache
def load_data():
    df = pd.read_csv('data/MunicipalDebtAnalysis.csv')
    return df

df = load_data()

st.title('Análise de Dívida Municipal')
st.write(df)


st.line_chart(df)

st.map(df)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    st.line_chart(chart_data)