import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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
    st.markdown("""
    A base usada para essa análise poder ser encontrada no site [Kaggle](https://www.kaggle.com/datasets/dmsconsultingsa/municipal-debt-risk-analysis). Ela contém informações\
            sobre os devedores, como, tipo de propriedade, valor e tamanho da propriedade e sobre a dívida, valor total\
            \
            ,total recebido, entre outras. Além disso, há uma classificação binária entre boas e más dívidas.""")

elif sidebar_selection == 'Análise Exploratória':
    st.title('Análise Exploratória de Dados')
    st.header('Conteúdo')
    shape = df.shape
    columns = df.columns.tolist()
    st.markdown("""
                O conjunto de dados possui {} linhas e {} colunas.  

                Essas colunas são:  

                - *AccCategoryID*: (ID da Categoria de Conta) O link numérico no banco de dados para a Categoria de Conta
                - *AccCategory*: (Categoria de Conta) Uma classificação do tipo de conta
                - *AccCategoryAbbr*: (Abreviação da Categoria de Conta) Uma abreviação da classificação
                    do tipo de conta - para ser usada para codificação one-hot
                - *PropertyValue*: (Valor do Imóvel) O valor de mercado da propriedade
                - *PropertySize*: (Tamanho da Propriedade) O tamanho da propriedade em metros quadrados
                - *TotalBilling*: (Total da cobrança) O valor total cobrado para a conta por todos os serviços
                - *AverageBilling*: (Faturamento Médio) O valor médio faturado para a conta por todos os serviços
                - *TotalReceipting*: (Total de Recebimento) O valor total recebido para a conta por todos os serviços
                - *AverageReceipting*: (Recebimento Médio) O valor médio recebido para a conta por todos os serviços
                - *TotalDebt*: (Total de Dívida) A Dívida Total que está em 90 dias ou mais
                - *TotalWriteOff*: (Total de Perda) O montante total da dívida que foi perdida
                - *CollectionRatio*: (Razão de Cobrança) A razão entre o Total de Recebimento e o
                    Total de Faturamento (ou seja, Total de Recebimento / Total de Faturamento)
                - *DebtBillingRatio*: (Razão de Dívida e Cobrança) A razão entre a Dívida Total e o Total cobrado
                    (ou seja, (Dívida Total + Total de Perda) / Total de Faturamento)
                - *TotalElectricityBill*: (Conta de Luz Total) O valor total faturado pela eletricidade.
                    Este campo foi colocado em prática porque é usado como meio de recuperar dívida\
                    - ou seja, se um valor estiver pendente para qualquer serviço, a prefeitura tem
                    o direito de cortar a conexão de eletricidade do consumidor.
                - *HasIDNo*: (Possui Número de Identificação) O consumidor tem um número de identificação.
                    Isso é semelhante a um número de Segurança Social nos EUA e pode ser útil em processos legais.
                    Um consumidor sem nenhum detalhe de ID é muito mais difícil de recuperar dívida.
                    Além disso, este campo indica que a conta é mantida por uma pessoa e não por uma empresa.
                    No entanto, não é muito confiável, pois muitas vezes não é capturado adequadamente ou não
                    é capturado de forma alguma.
                - *BadDebtIndic*: (Indicador de Dívida Incobrável) 1 = É considerado uma Dívida Incobrável,
                0 = Não é considerado uma Dívida Incobrável.
                """.format(shape[0], shape[1]))
    ax = sns.countplot(x = df.baddebt)
    plt.title("Distribuição de dívidas boas e ruins")
    st.pyplot(ax.figure)
    col_options = columns[2:]
    col_selection = st.selectbox('Selecione uma coluna:', col_options)

    st.subheader('Estatísticas de cada coluna')
    st.write(df[col_selection].describe())
    fig, ax = plt.subplots()
    if col_selection ==  'propertyvalue':
        sns.histplot(np.log(df[[col_selection]].replace(0, 0.01)), ax = ax)
    else:
        sns.histplot(df[col_selection], ax = ax)
    st.pyplot(fig)

    corr = df.corr()

    st.header('Matriz de correlação')
    fig, ax = plt.subplots()
    sns.heatmap(corr, cmap = 'coolwarm', annot=True, annot_kws={'fontsize':4, 'rotation':45}, ax = ax)
    st.pyplot(fig)

    st.subheader('Pares de colunas correlacionados')
    k = st.slider('Selecione o número de pares para visualização:', 1, len(corr), 5, 1)
    corr_pairs = corr.abs().unstack().sort_values(ascending=False).drop_duplicates()
    corr_pairs = corr_pairs[corr_pairs != 1]
    corr_pairs = corr_pairs.reset_index().rename(columns={'level_0': 'Column 1', 'level_1': 'Column 2', 0: 'Correlation'})
    corr_pairs = corr_pairs.head(k)
    st.write(corr_pairs)

if sidebar_selection == "Modelos":
    pass
