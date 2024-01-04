import streamlit as st
import pandas as pd
import pygsheets as pg
from datetime import date

credencial = pg.authorize(service_file="cred.json")
arquivo_googleSheets = "https://docs.google.com/spreadsheets/d/1EmVJJ7U2RkUSH402SN4b8UaobZhmiqsQdtOnqPFf5Hs/"
excel = credencial.open_by_url(arquivo_googleSheets)
aba = excel.worksheet_by_title("Sheet1")

data = aba.get_all_values()

with st.form(key='Ticket'):
    st.title('Cadastro de Ticket')
    st.write('Felipe Florenziano')
    
    ticket, tempo_conversao = st.columns(2)
    with ticket:
        ticket = st.text_input(label='N Ticket', placeholder='Informe o Numero do Ticket')
    with tempo_conversao:
        tempo_conversao = st.text_input(label='Tempo Conversao', placeholder='Tempo para Finalizar')
    
    company_name, cnpj = st.columns(2)
    with company_name:
        company_name = st.text_input(label='Company_name', placeholder='Nome da Empresa')
    with cnpj:
        cnpj = st.text_input(label='CNPJ', placeholder='CNPJ da Empresa')
    
    tipo, database = st.columns(2)
    with tipo:
        tipo = st.selectbox(label='OSD / WKM', options=['OSD', 'WKM'], index=None, placeholder='Escolha uma Opção')
    with database:
        database = st.multiselect(label='Database', options=['FDB','MySQL','Excel','DBF','SQL Server'], placeholder='Tipo do Banco de Dados')

    data_entrada, data_saida = st.columns(2)
    with data_entrada:
        data_entrada = st.date_input(label='Entrada', key='data_entrada')
    with data_saida:
        data_saida = st.date_input(label='Saida', key='data_saida')

    servico, valor = st.columns(2)
    with servico:
        servico = st.selectbox(label='Servico', options=['Extracao de Dados','Conversao de Dados'], index=None, placeholder='Tipo de Servico')
    with valor:
        valor = st.text_input(label='Valor do Servico', placeholder='Informe o Valor do Servico')

    observ = st.text_area('Observacao')
    st.markdown('')
    
    # Centraliza e estiliza o botão de envio
    button = st.form_submit_button('Enviar')
    if button:
        incluir = {
            "Ticket": [ticket],
            "Data_Entrada": [data_entrada.strftime("%Y-%m-%d")],
            "Data_Saida": [data_saida.strftime("%Y-%m-%d")],
            "OSD/WKM": [tipo],
            "Database": [", ".join(database)],  # Converte a lista para uma string
            "Tipo_Servico": [servico],
            "Tempo_Conversao": [tempo_conversao],
            "Valor_Servico": [valor],
            "Company_Name": [company_name],
            "CNPJ": [cnpj],
            "Observ": [observ]
        }

        commit = pd.DataFrame(incluir)

        # Adiciona os dados ao final da planilha
        aba.append_table(commit.values.tolist(), start='A2', end=None, dimension='ROWS', overwrite=False)

        st.success('Informacoes adicionadas no Google Sheets')
