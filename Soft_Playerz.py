import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
#from PIL import image
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import plotly.express as px
import io
import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar


#CABEÇALHO DO FORM
st.markdown("<h1 style='text-align: center;'>Ranking de Jogadores de Futebol</h1>", unsafe_allow_html=True)
#st.markdown("<h2 style='text-align: center;'>Qual a contribuição do seu clube?</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>app by @JAmerico1898</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>A análise contempla +40.000 jogadores atuando em 62 ligas, em 22 funções diferentes<br> e +900 minutos em campo nas 3 últimas temporadas. Dados do Wyscout.<br>Atualizado em 10Dez2023.</h6>", unsafe_allow_html=True)
#st.markdown("<h6 style='text-align: center;'>Os resultados obtidos são BEM DIFERENTES daqueles que utilizam o critério de audiência da LIBRA</h6>", unsafe_allow_html=True)
st.markdown("---")

df = pd.read_excel("jogadores.xlsx")
df1 = pd.read_excel("jogador.xlsx")
df2 = pd.read_excel("Funções.xlsx")
df5 = pd.read_excel("ligas.xlsx")
df6 = pd.read_excel("Posições.xlsx")
df7 = pd.read_excel("temporadas.xlsx")
df8 = pd.read_excel("nacionalidades.xlsx")
df9 = pd.read_excel("contratos.xlsx")

with st.sidebar:

    jogadores = df1["Atleta"]
    #temporadas = df["Versão_Temporada"]
    #posições = df["Posição"]
    #funções = ("Goleiro", "Goleiro_Líbero", "Lateral_Defensivo", "Lateral_Ofensivo", "Lateral_Equilibrado", "Zagueiro_Defensivo",
    #           "Zagueiro_Construtor", "Zagueiro_Equilibrado", "Primeiro_Volante_Defensivo", "Primeiro_Volante_Construtor",
    #           "Primeiro_Volante_Equilibrado", "Segundo_Volante_Box_to_Box", "Segundo_Volante_Organizador", "Segundo_Volante_Equilibrado",
    #           "Meia_Organizador", "Meia_Atacante", "Extremo_Organizador", "Extremo_Tático", "Extremo_Agudo", "Atacante_Referência",
    #           "Atacante_Móvel", "Segundo_Atacante")

    choose = option_menu("Galeria de Apps", ["Ranking de Jogadores", "10 Melhores da Liga", "Nacionais pelo Mundo", "Free Agents pelo Mundo", "Histórico do Jogador", "Sobre o APP"],
                         icons=['graph-up-arrow', 'sort-numeric-down', 'magic', 'search', 'mortarboard', 'book'],
                         menu_icon="app-indicator", default_index=0, 
                         styles={
                         "container": {"padding": "5!important", "background-color": "#fafafa"},
                         "icon": {"color": "orange", "font-size": "25px"},
                         "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                         "nav-link-selected": {"background-color": "#02ab21"},    
                         }
                         )
#    button = st.form_submit_button("Comparar!")
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
if choose == "Histórico do Jogador":
    nacionalidades = df8["Nacionalidade"]
    jogadores = st.selectbox("Escolha o Jogador", options=jogadores)
    nacionalidade = st.selectbox("Escolha a Nacionalidade do Atleta", options=nacionalidades)
    if jogadores and nacionalidade:
        st.markdown("<h4 style='text-align: center;'>Histórico do Jogador<br>Temporadas 2021/2022/2023<br>ou<br>Temporadas 2020-21/2021-22/2022-23</b></h4>", unsafe_allow_html=True)
        historico = pd.read_excel("base_bruta.xlsx")
        historico = historico.loc[(historico['Atleta']==jogadores)&(historico['Nacionalidade']==nacionalidade)]
        historico = historico.iloc[:, np.r_[0, 2, 9, 10, 13, 15, 16]]
        st.dataframe(historico, use_container_width=True, hide_index=True)
        #0, 2, 17, 9, 10, 14, 15
###############################################################################################################################
###############################################################################################################################

if choose == "10 Melhores da Liga":
    ligas = df5["Liga"]
    posições = df6["Posição"]
    temporadas = df7["Versão_Temporada"]
    liga = st.selectbox("Escolha a Liga", options=ligas)
    posição = st.selectbox("Escolha a posição", options=posições)
    temporada = st.selectbox("Escolha a janela de análise", options=temporadas)

    if liga and temporada:
        if posição == "Goleiro":
            st.markdown("<h4 style='text-align: center;'>10 Goleiros Clássicos Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_3 = pd.read_excel("1_Role_Goleiro.xlsx")
            tabela_3 = tabela_3[(tabela_3['Liga']==liga)&(tabela_3['Versão_Temporada']==temporada)]
            tabela_3 = tabela_3.iloc[:, np.r_[1, 30, 3, 4, 7, 8:12, 15, 18:27]]
            tabela_3 = tabela_3.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise', 'Interceptações.1':'Interceptações'})
            tabela_3 = tabela_3.head(10)
            st.dataframe(tabela_3, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Goleiros Líberos Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_4 = pd.read_excel("2_Role_Goleiro_Líbero.xlsx")
            tabela_4 = tabela_4[(tabela_4['Liga']==liga)&(tabela_4['Versão_Temporada']==temporada)]
            tabela_4 = tabela_4.iloc[:, np.r_[1, 33, 3, 4, 7, 8:12, 15, 18:28]]
            tabela_4 = tabela_4.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise', 'Interceptações.1':'Interceptações'})
            tabela_4 = tabela_4.head(10)
            st.dataframe(tabela_4, use_container_width=True, hide_index=True)

        elif posição == "Lateral":
            st.markdown("<h4 style='text-align: center;'>10 Laterais Defensivos Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_3 = pd.read_excel("3_Role_Lateral_Defensivo.xlsx")
            tabela_3 = tabela_3[(tabela_3['Liga']==liga)&(tabela_3['Versão_Temporada']==temporada)]
            tabela_3 = tabela_3.iloc[:, np.r_[1, 29, 3, 4, 7, 8:12, 15, 18:23]]
            tabela_3 = tabela_3.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_3 = tabela_3.head(10)
            st.dataframe(tabela_3, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Laterais Ofensivos Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_4 = pd.read_excel("4_Role_Lateral_Ofensivo.xlsx")
            tabela_4 = tabela_4[(tabela_4['Liga']==liga)&(tabela_4['Versão_Temporada']==temporada)]
            tabela_4 = tabela_4.iloc[:, np.r_[1, 38, 3, 4, 7, 8:12, 15, 18:33]]
            tabela_4 = tabela_4.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_4 = tabela_4.head(10)
            st.dataframe(tabela_4, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Laterais Equilibrados Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_5 = pd.read_excel("5_Role_Lateral_Equilibrado.xlsx")
            tabela_5 = tabela_5[(tabela_5['Liga']==liga)&(tabela_5['Versão_Temporada']==temporada)]
            tabela_5 = tabela_5.iloc[:, np.r_[1, 41, 3, 4, 7, 8:12, 15, 18:35]]
            tabela_5 = tabela_5.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_5 = tabela_5.head(10)
            st.dataframe(tabela_5, use_container_width=True, hide_index=True)

        elif posição == "Zagueiro":
            st.markdown("<h4 style='text-align: center;'>10 Zagueiros Clássicos Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_6 = pd.read_excel("6_Role_Zagueiro_Defensivo.xlsx")
            tabela_6 = tabela_6[(tabela_6['Liga']==liga)&(tabela_6['Versão_Temporada']==temporada)]
            tabela_6 = tabela_6.iloc[:, np.r_[1, 29, 3, 4, 7, 8:12, 15, 18:23]]
            tabela_6 = tabela_6.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_6 = tabela_6.head(10)
            st.dataframe(tabela_6, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Zagueiros Construtores Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_7 = pd.read_excel("7_Role_Zagueiro_Construtor.xlsx")
            tabela_7 = tabela_7[(tabela_7['Liga']==liga)&(tabela_7['Versão_Temporada']==temporada)]
            tabela_7 = tabela_7.iloc[:, np.r_[1, 33, 3, 4, 7, 8:12, 15, 18:28]]
            tabela_7 = tabela_7.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_7 = tabela_7.head(10)
            st.dataframe(tabela_7, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Zagueiros Equilibrados Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_8 = pd.read_excel("8_Role_Zagueiro_Equilibrado.xlsx")
            tabela_8 = tabela_8[(tabela_8['Liga']==liga)&(tabela_8['Versão_Temporada']==temporada)]
            tabela_8 = tabela_8.iloc[:, np.r_[1, 36, 3, 4, 7, 8:12, 15, 18:32]]
            tabela_8 = tabela_8.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_8 = tabela_8.head(10)
            st.dataframe(tabela_8, use_container_width=True, hide_index=True)

        elif posição == "Primeiro Volante":
            st.markdown("<h4 style='text-align: center;'>10 Primeiros Volantes Defensivos Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_12 = pd.read_excel("9_Role_Volante_Defensivo.xlsx")
            tabela_12 = tabela_12[(tabela_12['Liga']==liga)&(tabela_12['Versão_Temporada']==temporada)]
            tabela_12 = tabela_12.iloc[:, np.r_[1, 27, 3, 4, 7, 8:12, 15, 18:22]]
            tabela_12 = tabela_12.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_12 = tabela_12.head(10)
            st.dataframe(tabela_12, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Primeiros Volantes Construtores Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_13 = pd.read_excel("10_Role_Volante_Construtor.xlsx")
            tabela_13 = tabela_13[(tabela_13['Liga']==liga)&(tabela_13['Versão_Temporada']==temporada)]
            tabela_13 = tabela_13.iloc[:, np.r_[1, 32, 3, 4, 7, 8:12, 15, 18:27]]
            tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_13 = tabela_13.head(10)
            st.dataframe(tabela_13, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Primeiros Volantes Equilibrados Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_14 = pd.read_excel("11_Role_Volante_Equilibrado.xlsx")
            tabela_14 = tabela_14[(tabela_14['Liga']==liga)&(tabela_14['Versão_Temporada']==temporada)]
            tabela_14 = tabela_14.iloc[:, np.r_[1, 34, 3, 4, 7, 8:12, 15, 18:29]]
            tabela_14 = tabela_14.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_14 = tabela_14.head(10)
            st.dataframe(tabela_14, use_container_width=True, hide_index=True)

        elif posição == "Segundo Volante":
            st.markdown("<h4 style='text-align: center;'>10 Segundos Volantes Box-to-Box Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_12 = pd.read_excel("12_Role_Segundo_Volante_Box_to_Box.xlsx")
            tabela_12 = tabela_12[(tabela_12['Liga']==liga)&(tabela_12['Versão_Temporada']==temporada)]
            tabela_12 = tabela_12.iloc[:, np.r_[1, 36, 3, 4, 7, 8:12, 15, 18:31]]
            tabela_12 = tabela_12.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_12 = tabela_12.head(10)
            st.dataframe(tabela_12, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Segundos Volantes Organizadores Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_13 = pd.read_excel("13_Role_Segundo_Volante_Organizador.xlsx")
            tabela_13 = tabela_13[(tabela_13['Liga']==liga)&(tabela_13['Versão_Temporada']==temporada)]
            tabela_13 = tabela_13.iloc[:, np.r_[1, 33, 3, 4, 7, 8:12, 15, 18:28]]
            tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_13 = tabela_13.head(10)
            st.dataframe(tabela_13, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Segundos Volantes Equilibrados Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_14 = pd.read_excel("14_Role_Segundo_Volante_Equilibrado.xlsx")
            tabela_14 = tabela_14[(tabela_14['Liga']==liga)&(tabela_14['Versão_Temporada']==temporada)]
            tabela_14 = tabela_14.iloc[:, np.r_[1, 36, 3, 4, 7, 8:12, 15, 18:31]]
            tabela_14 = tabela_14.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_14 = tabela_14.head(10)
            st.dataframe(tabela_14, use_container_width=True, hide_index=True)

        elif posição == "Meia":
            st.markdown("<h4 style='text-align: center;'>10 Meias Organizadores Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_15 = pd.read_excel("15_Role_Meia_Organizador.xlsx")
            tabela_15 = tabela_15[(tabela_15['Liga']==liga)&(tabela_15['Versão_Temporada']==temporada)]
            tabela_15 = tabela_15.iloc[:, np.r_[1, 33, 3, 4, 7, 8:12, 15, 18:28]]
            tabela_15 = tabela_15.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_15 = tabela_15.head(10)
            st.dataframe(tabela_15, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Meias Atacantes Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_16 = pd.read_excel("16_Role_Meia_Atacante.xlsx")
            tabela_16 = tabela_16[(tabela_16['Liga']==liga)&(tabela_16['Versão_Temporada']==temporada)]
            tabela_16 = tabela_16.iloc[:, np.r_[1, 40, 3, 4, 7, 8:12, 15, 18:35]]
            tabela_16 = tabela_16.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_16 = tabela_16.head(10)
            st.dataframe(tabela_16, use_container_width=True, hide_index=True)

        elif posição == "Extremo":
            st.markdown("<h4 style='text-align: center;'>10 Extremos Organizadores Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_17 = pd.read_excel("17_Role_Extremo_Organizador.xlsx")
            tabela_17 = tabela_17[(tabela_17['Liga']==liga)&(tabela_17['Versão_Temporada']==temporada)]
            tabela_17 = tabela_17.iloc[:, np.r_[1, 36, 3, 4, 7, 8:12, 15, 18:31]]
            tabela_17 = tabela_17.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_17 = tabela_17.head(10)
            st.dataframe(tabela_17, use_container_width=True, hide_index=True)
            
            st.markdown("<h4 style='text-align: center;'>10 Extremos Táticos Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_18 = pd.read_excel("18_Role_Extremo_Tático.xlsx")
            tabela_18 = tabela_18[(tabela_18['Liga']==liga)&(tabela_18['Versão_Temporada']==temporada)]
            tabela_18 = tabela_18.iloc[:, np.r_[1, 30, 3, 4, 7, 8:12, 15, 18:25]]
            tabela_18 = tabela_18.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_18 = tabela_18.head(10)
            st.dataframe(tabela_18, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Extremos Agudos Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_19 = pd.read_excel("19_Role_Extremo_Agudo.xlsx")
            tabela_19 = tabela_19[(tabela_19['Liga']==liga)&(tabela_19['Versão_Temporada']==temporada)]
            tabela_19 = tabela_19.iloc[:, np.r_[1, 36, 3, 4, 7, 8:12, 15, 18:31]]
            tabela_19 = tabela_19.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_19 = tabela_19.head(10)
            st.dataframe(tabela_19, use_container_width=True, hide_index=True)

        else:
            st.markdown("<h4 style='text-align: center;'>10 Atacantes Referências Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_17 = pd.read_excel("20_Role_Atacante_Referência.xlsx")
            tabela_17 = tabela_17[(tabela_17['Liga']==liga)&(tabela_17['Versão_Temporada']==temporada)]
            tabela_17 = tabela_17.iloc[:, np.r_[1, 33, 3, 4, 7, 8:12, 15, 18:27]]
            tabela_17 = tabela_17.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_17 = tabela_17.head(10)
            st.dataframe(tabela_17, use_container_width=True, hide_index=True)
            
            st.markdown("<h4 style='text-align: center;'>10 Atacantes Móveis Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_18 = pd.read_excel("21_Role_Atacante_Móvel.xlsx")
            tabela_18 = tabela_18[(tabela_18['Liga']==liga)&(tabela_18['Versão_Temporada']==temporada)]
            tabela_18 = tabela_18.iloc[:, np.r_[1, 32, 3, 4, 7, 8:12, 15, 18:27]]
            tabela_18 = tabela_18.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_18 = tabela_18.head(10)
            st.dataframe(tabela_18, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>10 Segundos Atacantes Mais Bem Ranqueados</b></h4>", unsafe_allow_html=True)
            tabela_19 = pd.read_excel("22_Role_Segundo_Atacante.xlsx")
            tabela_19 = tabela_19[(tabela_19['Liga']==liga)&(tabela_19['Versão_Temporada']==temporada)]
            tabela_19 = tabela_19.iloc[:, np.r_[1, 36, 3, 4, 7, 8:12, 15, 18:31]]
            tabela_19 = tabela_19.rename(columns={'Equipe_Janela_Análise':'Equipe'})
            tabela_19 = tabela_19.head(10)
            st.dataframe(tabela_19, use_container_width=True, hide_index=True)



###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
if choose == "Nacionais pelo Mundo":
    nacionalidades = df8["Nacionalidade"]
    posições = df6["Posição"]
    temporadas = df7["Versão_Temporada"]
    mundo_options = ['ENG1', 'ENG2', 'FRA1', 'FRA2', 'SPA1', 'SPA2', 'ITA1', 'ITA2', 'GER1', 'GER2', 'POR1', 'POR2', 'SWZ', 'CZH', 'CRO', 'SER', 'RUS', 'UKR', 'BEL1', 'BEL2', 'CHN',
             'DEN', 'GRE', 'HOL', 'JAP', 'MEX', 'SAUD', 'SCT', 'TUR', 'UAE', 'USA', 'BUL', 'AUT', 'QAT']
    nacionalidade = st.selectbox("Escolha a Nacionalidade do Atleta", options=nacionalidades)
    posição = st.selectbox("Escolha a posição", options=posições)
    temporada = 2023
    

    if nacionalidade and temporada:
        if posição == "Goleiro":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Goleiros Clássicos</b></h4>", unsafe_allow_html=True)
            tabela_5 = pd.read_excel("1_Role_Goleiro_Full.xlsx")
            tabela_5 = tabela_5[(tabela_5['Nacionalidade']==nacionalidade)&(tabela_5['Versão_Temporada']==temporada)]
            tabela_5 = tabela_5.iloc[:, np.r_[1, 25, 30, 3, 4, 7, 9:12, 15, 18:25]]
            tabela_5 = tabela_5.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise', 'Interceptações.1':'Interceptações'})
            tabela_5 = tabela_5[(tabela_5['Liga'] == 'ENG1') | (tabela_5['Liga'] == 'ENG2') | (tabela_5['Liga'] == 'FRA1') | (tabela_5['Liga'] == 'FRA2') 
                                | (tabela_5['Liga'] == 'SPA1') | (tabela_5['Liga'] == 'ITA1') | (tabela_5['Liga'] == 'GER1') | (tabela_5['Liga'] == 'POR1') 
                                | (tabela_5['Liga'] == 'SWZ') | (tabela_5['Liga'] == 'RUS') | (tabela_5['Liga'] == 'UKR') | (tabela_5['Liga'] == 'BEL1') 
                                | (tabela_5['Liga'] == 'CHN') | (tabela_5['Liga'] == 'DEN') | (tabela_5['Liga'] == 'GRE') | (tabela_5['Liga'] == 'HOL') 
                                | (tabela_5['Liga'] == 'JAP') | (tabela_5['Liga'] == 'MEX') | (tabela_5['Liga'] == 'SAUD') | (tabela_5['Liga'] == 'TUR') 
                                | (tabela_5['Liga'] == 'UAE') | (tabela_5['Liga'] == 'USA') | (tabela_5['Liga'] == 'ITA2') | (tabela_5['Liga'] == 'GER2') 
                                | (tabela_5['Liga'] == 'POR2') | (tabela_5['Liga'] == 'BUL') | (tabela_5['Liga'] == 'AUT') | (tabela_5['Liga'] == 'QAT')]
            tabela_5 = tabela_5.head(15)
            st.dataframe(tabela_5, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Goleiros Líberos</b></h4>", unsafe_allow_html=True)
            tabela_6 = pd.read_excel("2_Role_Goleiro_Líbero_Full.xlsx")
            tabela_6 = tabela_6[(tabela_6['Nacionalidade']==nacionalidade)&(tabela_6['Versão_Temporada']==temporada)]
            tabela_6 = tabela_6.iloc[:, np.r_[1, 28, 33, 3, 4, 7, 9:12, 15, 18:28]]
            tabela_6 = tabela_6.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise', 'Interceptações.1':'Interceptações'})
            tabela_6 = tabela_6[(tabela_6['Liga'] == 'ENG1') | (tabela_6['Liga'] == 'ENG2') | (tabela_6['Liga'] == 'FRA1') | (tabela_6['Liga'] == 'FRA2') 
                                | (tabela_6['Liga'] == 'SPA1') | (tabela_6['Liga'] == 'ITA1') | (tabela_6['Liga'] == 'GER1') | (tabela_6['Liga'] == 'POR1') 
                                | (tabela_6['Liga'] == 'SWZ') | (tabela_6['Liga'] == 'RUS') | (tabela_6['Liga'] == 'UKR') | (tabela_6['Liga'] == 'BEL1') 
                                | (tabela_6['Liga'] == 'CHN') | (tabela_6['Liga'] == 'DEN') | (tabela_6['Liga'] == 'GRE') | (tabela_6['Liga'] == 'HOL') 
                                | (tabela_6['Liga'] == 'JAP') | (tabela_6['Liga'] == 'MEX') | (tabela_6['Liga'] == 'SAUD') | (tabela_6['Liga'] == 'TUR') 
                                | (tabela_6['Liga'] == 'UAE') | (tabela_6['Liga'] == 'USA') | (tabela_6['Liga'] == 'ITA2') | (tabela_6['Liga'] == 'GER2') 
                                | (tabela_6['Liga'] == 'POR2') | (tabela_6['Liga'] == 'BUL') | (tabela_6['Liga'] == 'AUT') | (tabela_6['Liga'] == 'QAT')]
            tabela_6 = tabela_6.head(15)
            st.dataframe(tabela_6, use_container_width=True, hide_index=True)


        elif posição == "Lateral":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Laterais Defensivos</b></h4>", unsafe_allow_html=True)
            tabela_5 = pd.read_excel("3_Role_Lateral_Defensivo_Full.xlsx")
            tabela_5 = tabela_5[(tabela_5['Nacionalidade']==nacionalidade)&(tabela_5['Versão_Temporada']==temporada)]
            tabela_5 = tabela_5.iloc[:, np.r_[1, 24, 29, 3, 4, 7, 9:12, 15, 18:24]]
            tabela_5 = tabela_5.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_5 = tabela_5[(tabela_5['Liga'] == 'ENG1') | (tabela_5['Liga'] == 'ENG2') | (tabela_5['Liga'] == 'FRA1') | (tabela_5['Liga'] == 'FRA2') 
                                | (tabela_5['Liga'] == 'SPA1') | (tabela_5['Liga'] == 'ITA1') | (tabela_5['Liga'] == 'GER1') | (tabela_5['Liga'] == 'POR1') 
                                | (tabela_5['Liga'] == 'SWZ') | (tabela_5['Liga'] == 'RUS') | (tabela_5['Liga'] == 'UKR') | (tabela_5['Liga'] == 'BEL1') 
                                | (tabela_5['Liga'] == 'CHN') | (tabela_5['Liga'] == 'DEN') | (tabela_5['Liga'] == 'GRE') | (tabela_5['Liga'] == 'HOL') 
                                | (tabela_5['Liga'] == 'JAP') | (tabela_5['Liga'] == 'MEX') | (tabela_5['Liga'] == 'SAUD') | (tabela_5['Liga'] == 'TUR') 
                                | (tabela_5['Liga'] == 'UAE') | (tabela_5['Liga'] == 'USA') | (tabela_5['Liga'] == 'ITA2') | (tabela_5['Liga'] == 'GER2') 
                                | (tabela_5['Liga'] == 'POR2') | (tabela_5['Liga'] == 'BUL') | (tabela_5['Liga'] == 'AUT') | (tabela_5['Liga'] == 'QAT')]
            tabela_5 = tabela_5.head(15)
            st.dataframe(tabela_5, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Laterais Ofensivos</b></h4>", unsafe_allow_html=True)
            tabela_6 = pd.read_excel("4_Role_Lateral_Ofensivo_Full.xlsx")
            tabela_6 = tabela_6[(tabela_6['Nacionalidade']==nacionalidade)&(tabela_6['Versão_Temporada']==temporada)]
            tabela_6 = tabela_6.iloc[:, np.r_[1, 33, 38, 3, 4, 7, 9:12, 15, 18:33]]
            tabela_6 = tabela_6.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_6 = tabela_6[(tabela_6['Liga'] == 'ENG1') | (tabela_6['Liga'] == 'ENG2') | (tabela_6['Liga'] == 'FRA1') | (tabela_6['Liga'] == 'FRA2') 
                                | (tabela_6['Liga'] == 'SPA1') | (tabela_6['Liga'] == 'ITA1') | (tabela_6['Liga'] == 'GER1') | (tabela_6['Liga'] == 'POR1') 
                                | (tabela_6['Liga'] == 'SWZ') | (tabela_6['Liga'] == 'RUS') | (tabela_6['Liga'] == 'UKR') | (tabela_6['Liga'] == 'BEL1') 
                                | (tabela_6['Liga'] == 'CHN') | (tabela_6['Liga'] == 'DEN') | (tabela_6['Liga'] == 'GRE') | (tabela_6['Liga'] == 'HOL') 
                                | (tabela_6['Liga'] == 'JAP') | (tabela_6['Liga'] == 'MEX') | (tabela_6['Liga'] == 'SAUD') | (tabela_6['Liga'] == 'TUR') 
                                | (tabela_6['Liga'] == 'UAE') | (tabela_6['Liga'] == 'USA') | (tabela_6['Liga'] == 'ITA2') | (tabela_6['Liga'] == 'GER2') 
                                | (tabela_6['Liga'] == 'POR2') | (tabela_6['Liga'] == 'BUL') | (tabela_6['Liga'] == 'AUT') | (tabela_6['Liga'] == 'QAT')]
            tabela_6 = tabela_6.head(15)
            st.dataframe(tabela_6, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Laterais Equilibrados</b></h4>", unsafe_allow_html=True)
            tabela_7 = pd.read_excel("5_Role_Lateral_Equilibrado_Full.xlsx")
            tabela_7 = tabela_7[(tabela_7['Nacionalidade']==nacionalidade)&(tabela_7['Versão_Temporada']==temporada)]
            tabela_7 = tabela_7.iloc[:, np.r_[1, 36, 41, 3, 4, 7, 9:12, 15, 18:36]]
            tabela_7 = tabela_7.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_7 = tabela_7[(tabela_7['Liga'] == 'ENG1') | (tabela_7['Liga'] == 'ENG2') | (tabela_7['Liga'] == 'FRA1') | (tabela_7['Liga'] == 'FRA2') 
                                | (tabela_7['Liga'] == 'SPA1') | (tabela_7['Liga'] == 'ITA1') | (tabela_7['Liga'] == 'GER1') | (tabela_7['Liga'] == 'POR1') 
                                | (tabela_7['Liga'] == 'SWZ') | (tabela_7['Liga'] == 'RUS') | (tabela_7['Liga'] == 'UKR') | (tabela_7['Liga'] == 'BEL1') 
                                | (tabela_7['Liga'] == 'CHN') | (tabela_7['Liga'] == 'DEN') | (tabela_7['Liga'] == 'GRE') | (tabela_7['Liga'] == 'HOL') 
                                | (tabela_7['Liga'] == 'JAP') | (tabela_7['Liga'] == 'MEX') | (tabela_7['Liga'] == 'SAUD') | (tabela_7['Liga'] == 'TUR') 
                                | (tabela_7['Liga'] == 'UAE') | (tabela_7['Liga'] == 'USA') | (tabela_7['Liga'] == 'ITA2') | (tabela_7['Liga'] == 'GER2') 
                                | (tabela_7['Liga'] == 'POR2') | (tabela_7['Liga'] == 'BUL') | (tabela_7['Liga'] == 'AUT') | (tabela_7['Liga'] == 'QAT')]
            tabela_7 = tabela_7.head(15)
            st.dataframe(tabela_7, use_container_width=True, hide_index=True)

        elif posição == "Zagueiro":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Zagueiros Clássicos</b></h4>", unsafe_allow_html=True)
            tabela_8 = pd.read_excel("6_Role_Zagueiro_Defensivo_Full.xlsx")
            tabela_8 = tabela_8[(tabela_8['Nacionalidade']==nacionalidade)&(tabela_8['Versão_Temporada']==temporada)]
            tabela_8 = tabela_8.iloc[:, np.r_[1, 24, 29, 3, 4, 7, 9:12, 15, 18:24]]
            tabela_8 = tabela_8.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_8 = tabela_8[(tabela_8['Liga'] == 'ENG1') | (tabela_8['Liga'] == 'ENG2') | (tabela_8['Liga'] == 'FRA1') | (tabela_8['Liga'] == 'FRA2') 
                                | (tabela_8['Liga'] == 'SPA1') | (tabela_8['Liga'] == 'ITA1') | (tabela_8['Liga'] == 'GER1') | (tabela_8['Liga'] == 'POR1') 
                                | (tabela_8['Liga'] == 'SWZ') | (tabela_8['Liga'] == 'RUS') | (tabela_8['Liga'] == 'UKR') | (tabela_8['Liga'] == 'BEL1') 
                                | (tabela_8['Liga'] == 'CHN') | (tabela_8['Liga'] == 'DEN') | (tabela_8['Liga'] == 'GRE') | (tabela_8['Liga'] == 'HOL') 
                                | (tabela_8['Liga'] == 'JAP') | (tabela_8['Liga'] == 'MEX') | (tabela_8['Liga'] == 'SAUD') | (tabela_8['Liga'] == 'TUR') 
                                | (tabela_8['Liga'] == 'UAE') | (tabela_8['Liga'] == 'USA') | (tabela_8['Liga'] == 'ITA2') | (tabela_8['Liga'] == 'GER2') 
                                | (tabela_8['Liga'] == 'POR2') | (tabela_8['Liga'] == 'BUL') | (tabela_8['Liga'] == 'AUT') | (tabela_8['Liga'] == 'QAT')]
            tabela_8 = tabela_8.head(15)
            st.dataframe(tabela_8, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Zagueiros Construtores</b></h4>", unsafe_allow_html=True)
            tabela_9 = pd.read_excel("7_Role_Zagueiro_Construtor_Full.xlsx")
            tabela_9 = tabela_9[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Versão_Temporada']==temporada)]
            tabela_9 = tabela_9.iloc[:, np.r_[1, 28, 33, 3, 4, 7, 9:12, 15, 18:28]]
            tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
                                | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
                                | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
                                | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
                                | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
                                | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
                                | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT')]
            tabela_9 = tabela_9.head(15)
            st.dataframe(tabela_9, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Zagueiros Equilibrados</b></h4>", unsafe_allow_html=True)
            tabela_10 = pd.read_excel("8_Role_Zagueiro_Equilibrado_Full.xlsx")
            tabela_10 = tabela_10[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Versão_Temporada']==temporada)]
            tabela_10 = tabela_10.iloc[:, np.r_[1, 31, 36, 3, 4, 7, 9:12, 15, 18:31]]
            tabela_10 = tabela_10.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
                                | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
                                | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
                                | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
                                | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
                                | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
                                | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT')]
            tabela_10 = tabela_10.head(15)
            st.dataframe(tabela_10, use_container_width=True, hide_index=True)

        elif posição == "Primeiro Volante":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Primeiros Volantes Defensivos</b></h4>", unsafe_allow_html=True)
            tabela_11 = pd.read_excel("9_Role_Volante_Defensivo_Full.xlsx")
            tabela_11 = tabela_11[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Versão_Temporada']==temporada)]
            tabela_11 = tabela_11.iloc[:, np.r_[1, 22, 27, 3, 4, 7, 9:12, 15, 18:22]]
            tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
                                | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
                                | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
                                | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
                                | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
                                | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
                                | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT')]
            tabela_11 = tabela_11.head(15)
            st.dataframe(tabela_11, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Primeiros Volantes Construtores</b></h4>", unsafe_allow_html=True)
            tabela_12 = pd.read_excel("10_Role_Volante_Construtor_Full.xlsx")
            tabela_12 = tabela_12[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Versão_Temporada']==temporada)]
            tabela_12 = tabela_12.iloc[:, np.r_[1, 27, 32, 3, 4, 7, 9:12, 15, 18:27]]
            tabela_12 = tabela_12.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
                                | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
                                | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
                                | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
                                | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
                                | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
                                | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT')]
            tabela_12 = tabela_12.head(15)
            st.dataframe(tabela_12, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Primeiros Volantes Equilibrados</b></h4>", unsafe_allow_html=True)
            tabela_13 = pd.read_excel("11_Role_Volante_Equilibrado_Full.xlsx")
            tabela_13 = tabela_13[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Versão_Temporada']==temporada)]
            tabela_13 = tabela_13.iloc[:, np.r_[1, 29, 34, 3, 4, 7, 9:12, 15, 18:29]]
            tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
                                | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
                                | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
                                | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
                                | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
                                | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
                                | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT')]
            tabela_13 = tabela_13.head(15)
            st.dataframe(tabela_13, use_container_width=True, hide_index=True)

        elif posição == "Segundo Volante":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Segundos Volantes Box-to-Box</b></h4>", unsafe_allow_html=True)
            tabela_11 = pd.read_excel("12_Role_Segundo_Volante_Box_to_Box_Full.xlsx")
            tabela_11 = tabela_11[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Versão_Temporada']==temporada)]
            tabela_11 = tabela_11.iloc[:, np.r_[1, 31, 36, 3, 4, 7, 9:12, 15, 18:31]]
            tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
                                | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
                                | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
                                | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
                                | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
                                | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
                                | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT')]
            tabela_11 = tabela_11.head(15)
            st.dataframe(tabela_11, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Segundos Volantes Organizadores</b></h4>", unsafe_allow_html=True)
            tabela_12 = pd.read_excel("13_Role_Segundo_Volante_Organizador_Full.xlsx")
            tabela_12 = tabela_12[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Versão_Temporada']==temporada)]
            tabela_12 = tabela_12.iloc[:, np.r_[1, 28, 33, 3, 4, 7, 9:12, 15, 18:28]]
            tabela_12 = tabela_12.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
                                | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
                                | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
                                | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
                                | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
                                | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
                                | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT')]
            tabela_12 = tabela_12.head(15)
            st.dataframe(tabela_12, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Segundos Volantes Equilibrados</b></h4>", unsafe_allow_html=True)
            tabela_13 = pd.read_excel("14_Role_Segundo_Volante_Equilibrado_Full.xlsx")
            tabela_13 = tabela_13[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Versão_Temporada']==temporada)]
            tabela_13 = tabela_13.iloc[:, np.r_[1, 31, 36, 3, 4, 7, 9:12, 15, 18:31]]
            tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
                                | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
                                | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
                                | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
                                | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
                                | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
                                | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT')]
            tabela_13 = tabela_13.head(15)
            st.dataframe(tabela_13, use_container_width=True, hide_index=True)

        elif posição == "Meia":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Meias Organizadores </b></h4>", unsafe_allow_html=True)
            tabela_14 = pd.read_excel("15_Role_Meia_Organizador_Full.xlsx")
            tabela_14 = tabela_14[(tabela_14['Nacionalidade']==nacionalidade)&(tabela_14['Versão_Temporada']==temporada)]
            tabela_14 = tabela_14.iloc[:, np.r_[1, 28, 33, 3, 4, 7, 9:12, 15, 18:28]]
            tabela_14 = tabela_14.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_14 = tabela_14[(tabela_14['Liga'] == 'ENG1') | (tabela_14['Liga'] == 'ENG2') | (tabela_14['Liga'] == 'FRA1') | (tabela_14['Liga'] == 'FRA2') 
                                | (tabela_14['Liga'] == 'SPA1') | (tabela_14['Liga'] == 'ITA1') | (tabela_14['Liga'] == 'GER1') | (tabela_14['Liga'] == 'POR1') 
                                | (tabela_14['Liga'] == 'SWZ') | (tabela_14['Liga'] == 'RUS') | (tabela_14['Liga'] == 'UKR') | (tabela_14['Liga'] == 'BEL1') 
                                | (tabela_14['Liga'] == 'CHN') | (tabela_14['Liga'] == 'DEN') | (tabela_14['Liga'] == 'GRE') | (tabela_14['Liga'] == 'HOL') 
                                | (tabela_14['Liga'] == 'JAP') | (tabela_14['Liga'] == 'MEX') | (tabela_14['Liga'] == 'SAUD') | (tabela_14['Liga'] == 'TUR') 
                                | (tabela_14['Liga'] == 'UAE') | (tabela_14['Liga'] == 'USA') | (tabela_14['Liga'] == 'ITA2') | (tabela_14['Liga'] == 'GER2') 
                                | (tabela_14['Liga'] == 'POR2') | (tabela_14['Liga'] == 'BUL') | (tabela_14['Liga'] == 'AUT') | (tabela_14['Liga'] == 'QAT')]
            tabela_14 = tabela_14.head(15)
            st.dataframe(tabela_14, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Meias Atacantes</b></h4>", unsafe_allow_html=True)
            tabela_15 = pd.read_excel("16_Role_Meia_Atacante_Full.xlsx")
            tabela_15 = tabela_15[(tabela_15['Nacionalidade']==nacionalidade)&(tabela_15['Versão_Temporada']==temporada)]
            tabela_15 = tabela_15.iloc[:, np.r_[1, 35, 40, 3, 4, 7, 9:12, 15, 18:35]]
            tabela_15 = tabela_15.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_15 = tabela_15[(tabela_15['Liga'] == 'ENG1') | (tabela_15['Liga'] == 'ENG2') | (tabela_15['Liga'] == 'FRA1') | (tabela_15['Liga'] == 'FRA2') 
                                | (tabela_15['Liga'] == 'SPA1') | (tabela_15['Liga'] == 'ITA1') | (tabela_15['Liga'] == 'GER1') | (tabela_15['Liga'] == 'POR1') 
                                | (tabela_15['Liga'] == 'SWZ') | (tabela_15['Liga'] == 'RUS') | (tabela_15['Liga'] == 'UKR') | (tabela_15['Liga'] == 'BEL1') 
                                | (tabela_15['Liga'] == 'CHN') | (tabela_15['Liga'] == 'DEN') | (tabela_15['Liga'] == 'GRE') | (tabela_15['Liga'] == 'HOL') 
                                | (tabela_15['Liga'] == 'JAP') | (tabela_15['Liga'] == 'MEX') | (tabela_15['Liga'] == 'SAUD') | (tabela_15['Liga'] == 'TUR') 
                                | (tabela_15['Liga'] == 'UAE') | (tabela_15['Liga'] == 'USA') | (tabela_15['Liga'] == 'ITA2') | (tabela_15['Liga'] == 'GER2') 
                                | (tabela_15['Liga'] == 'POR2') | (tabela_15['Liga'] == 'BUL') | (tabela_15['Liga'] == 'AUT') | (tabela_15['Liga'] == 'QAT')]
            tabela_15 = tabela_15.head(15)
            st.dataframe(tabela_15, use_container_width=True, hide_index=True)

        elif posição == "Extremo":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Extremos Organizadores</b></h4>", unsafe_allow_html=True)
            tabela_16 = pd.read_excel("17_Role_Extremo_Organizador_Full.xlsx")
            tabela_16 = tabela_16[(tabela_16['Nacionalidade']==nacionalidade)&(tabela_16['Versão_Temporada']==temporada)]
            tabela_16 = tabela_16.iloc[:, np.r_[1, 31, 36, 3, 4, 7, 9:12, 15, 18:31]]
            tabela_16 = tabela_16.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_16 = tabela_16[(tabela_16['Liga'] == 'ENG1') | (tabela_16['Liga'] == 'ENG2') | (tabela_16['Liga'] == 'FRA1') | (tabela_16['Liga'] == 'FRA2') 
                                | (tabela_16['Liga'] == 'SPA1') | (tabela_16['Liga'] == 'ITA1') | (tabela_16['Liga'] == 'GER1') | (tabela_16['Liga'] == 'POR1') 
                                | (tabela_16['Liga'] == 'SWZ') | (tabela_16['Liga'] == 'RUS') | (tabela_16['Liga'] == 'UKR') | (tabela_16['Liga'] == 'BEL1') 
                                | (tabela_16['Liga'] == 'CHN') | (tabela_16['Liga'] == 'DEN') | (tabela_16['Liga'] == 'GRE') | (tabela_16['Liga'] == 'HOL') 
                                | (tabela_16['Liga'] == 'JAP') | (tabela_16['Liga'] == 'MEX') | (tabela_16['Liga'] == 'SAUD') | (tabela_16['Liga'] == 'TUR') 
                                | (tabela_16['Liga'] == 'UAE') | (tabela_16['Liga'] == 'USA') | (tabela_16['Liga'] == 'ITA2') | (tabela_16['Liga'] == 'GER2') 
                                | (tabela_16['Liga'] == 'POR2') | (tabela_16['Liga'] == 'BUL') | (tabela_16['Liga'] == 'AUT') | (tabela_16['Liga'] == 'QAT')]
            tabela_16 = tabela_16.head(15)
            st.dataframe(tabela_16, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Extremos Táticos</b></h4>", unsafe_allow_html=True)
            tabela_17 = pd.read_excel("18_Role_Extremo_Tático_Full.xlsx")
            tabela_17 = tabela_17[(tabela_17['Nacionalidade']==nacionalidade)&(tabela_17['Versão_Temporada']==temporada)]
            tabela_17 = tabela_17.iloc[:, np.r_[1, 25, 30, 3, 4, 7, 9:12, 15, 18:25]]
            tabela_17 = tabela_17.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_17 = tabela_17[(tabela_17['Liga'] == 'ENG1') | (tabela_17['Liga'] == 'ENG2') | (tabela_17['Liga'] == 'FRA1') | (tabela_17['Liga'] == 'FRA2') 
                                | (tabela_17['Liga'] == 'SPA1') | (tabela_17['Liga'] == 'ITA1') | (tabela_17['Liga'] == 'GER1') | (tabela_17['Liga'] == 'POR1') 
                                | (tabela_17['Liga'] == 'SWZ') | (tabela_17['Liga'] == 'RUS') | (tabela_17['Liga'] == 'UKR') | (tabela_17['Liga'] == 'BEL1') 
                                | (tabela_17['Liga'] == 'CHN') | (tabela_17['Liga'] == 'DEN') | (tabela_17['Liga'] == 'GRE') | (tabela_17['Liga'] == 'HOL') 
                                | (tabela_17['Liga'] == 'JAP') | (tabela_17['Liga'] == 'MEX') | (tabela_17['Liga'] == 'SAUD') | (tabela_17['Liga'] == 'TUR') 
                                | (tabela_17['Liga'] == 'UAE') | (tabela_17['Liga'] == 'USA') | (tabela_17['Liga'] == 'ITA2') | (tabela_17['Liga'] == 'GER2') 
                                | (tabela_17['Liga'] == 'POR2') | (tabela_17['Liga'] == 'BUL') | (tabela_17['Liga'] == 'AUT') | (tabela_17['Liga'] == 'QAT')]
            tabela_17 = tabela_17.head(15)
            st.dataframe(tabela_17, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Extremos Agudos</b></h4>", unsafe_allow_html=True)
            tabela_18 = pd.read_excel("19_Role_Extremo_Agudo_Full.xlsx")
            tabela_18 = tabela_18[(tabela_18['Nacionalidade']==nacionalidade)&(tabela_18['Versão_Temporada']==temporada)]
            tabela_18 = tabela_18.iloc[:, np.r_[1, 31, 36, 3, 4, 7, 9:12, 15, 18:31]]
            tabela_18 = tabela_18.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_18 = tabela_18[(tabela_18['Liga'] == 'ENG1') | (tabela_18['Liga'] == 'ENG2') | (tabela_18['Liga'] == 'FRA1') | (tabela_18['Liga'] == 'FRA2') 
                                | (tabela_18['Liga'] == 'SPA1') | (tabela_18['Liga'] == 'ITA1') | (tabela_18['Liga'] == 'GER1') | (tabela_18['Liga'] == 'POR1') 
                                | (tabela_18['Liga'] == 'SWZ') | (tabela_18['Liga'] == 'RUS') | (tabela_18['Liga'] == 'UKR') | (tabela_18['Liga'] == 'BEL1') 
                                | (tabela_18['Liga'] == 'CHN') | (tabela_18['Liga'] == 'DEN') | (tabela_18['Liga'] == 'GRE') | (tabela_18['Liga'] == 'HOL') 
                                | (tabela_18['Liga'] == 'JAP') | (tabela_18['Liga'] == 'MEX') | (tabela_18['Liga'] == 'SAUD') | (tabela_18['Liga'] == 'TUR') 
                                | (tabela_18['Liga'] == 'UAE') | (tabela_18['Liga'] == 'USA') | (tabela_18['Liga'] == 'ITA2') | (tabela_18['Liga'] == 'GER2') 
                                | (tabela_18['Liga'] == 'POR2') | (tabela_18['Liga'] == 'BUL') | (tabela_18['Liga'] == 'AUT') | (tabela_18['Liga'] == 'QAT')]
            tabela_18 = tabela_18.head(15)
            st.dataframe(tabela_18, use_container_width=True, hide_index=True)

        elif posição == "Atacante":
            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Atacantes Referência</b></h4>", unsafe_allow_html=True)
            tabela_19 = pd.read_excel("20_Role_Atacante_Referência_Full.xlsx")
            tabela_19 = tabela_19[(tabela_19['Nacionalidade']==nacionalidade)&(tabela_19['Versão_Temporada']==temporada)]
            tabela_19 = tabela_19.iloc[:, np.r_[1, 28, 33, 3, 4, 7, 9:12, 15, 18:28]]
            tabela_19 = tabela_19.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_19 = tabela_19[(tabela_19['Liga'] == 'ENG1') | (tabela_19['Liga'] == 'ENG2') | (tabela_19['Liga'] == 'FRA1') | (tabela_19['Liga'] == 'FRA2') 
                                | (tabela_19['Liga'] == 'SPA1') | (tabela_19['Liga'] == 'ITA1') | (tabela_19['Liga'] == 'GER1') | (tabela_19['Liga'] == 'POR1') 
                                | (tabela_19['Liga'] == 'SWZ') | (tabela_19['Liga'] == 'RUS') | (tabela_19['Liga'] == 'UKR') | (tabela_19['Liga'] == 'BEL1') 
                                | (tabela_19['Liga'] == 'CHN') | (tabela_19['Liga'] == 'DEN') | (tabela_19['Liga'] == 'GRE') | (tabela_19['Liga'] == 'HOL') 
                                | (tabela_19['Liga'] == 'JAP') | (tabela_19['Liga'] == 'MEX') | (tabela_19['Liga'] == 'SAUD') | (tabela_19['Liga'] == 'TUR') 
                                | (tabela_19['Liga'] == 'UAE') | (tabela_19['Liga'] == 'USA') | (tabela_19['Liga'] == 'ITA2') | (tabela_19['Liga'] == 'GER2') 
                                | (tabela_19['Liga'] == 'POR2') | (tabela_19['Liga'] == 'BUL') | (tabela_19['Liga'] == 'AUT') | (tabela_19['Liga'] == 'QAT')]
            tabela_19 = tabela_19.head(15)
            st.dataframe(tabela_19, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Atacantes Móveis</b></h4>", unsafe_allow_html=True)
            tabela_20 = pd.read_excel("21_Role_Atacante_Móvel_Full.xlsx")
            tabela_20 = tabela_20[(tabela_20['Nacionalidade']==nacionalidade)&(tabela_20['Versão_Temporada']==temporada)]
            tabela_20 = tabela_20.iloc[:, np.r_[1, 27, 32, 3, 4, 7, 9:12, 15, 18:27]]
            tabela_20 = tabela_20.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_20 = tabela_20[(tabela_20['Liga'] == 'ENG1') | (tabela_20['Liga'] == 'ENG2') | (tabela_20['Liga'] == 'FRA1') | (tabela_20['Liga'] == 'FRA2') 
                                | (tabela_20['Liga'] == 'SPA1') | (tabela_20['Liga'] == 'ITA1') | (tabela_20['Liga'] == 'GER1') | (tabela_20['Liga'] == 'POR1') 
                                | (tabela_20['Liga'] == 'SWZ') | (tabela_20['Liga'] == 'RUS') | (tabela_20['Liga'] == 'UKR') | (tabela_20['Liga'] == 'BEL1') 
                                | (tabela_20['Liga'] == 'CHN') | (tabela_20['Liga'] == 'DEN') | (tabela_20['Liga'] == 'GRE') | (tabela_20['Liga'] == 'HOL') 
                                | (tabela_20['Liga'] == 'JAP') | (tabela_20['Liga'] == 'MEX') | (tabela_20['Liga'] == 'SAUD') | (tabela_20['Liga'] == 'TUR') 
                                | (tabela_20['Liga'] == 'UAE') | (tabela_20['Liga'] == 'USA') | (tabela_20['Liga'] == 'ITA2') | (tabela_20['Liga'] == 'GER2') 
                                | (tabela_20['Liga'] == 'POR2') | (tabela_20['Liga'] == 'BUL') | (tabela_20['Liga'] == 'AUT') | (tabela_20['Liga'] == 'QAT')]
            tabela_20 = tabela_20.head(15)
            st.dataframe(tabela_20, use_container_width=True, hide_index=True)

            st.markdown("<h4 style='text-align: center;'>15 Nacionais Mais Bem Ranqueados<br>Segundos Atacantes</b></h4>", unsafe_allow_html=True)
            tabela_21 = pd.read_excel("22_Role_Segundo_Atacante_Full.xlsx")
            tabela_21 = tabela_21[(tabela_21['Nacionalidade']==nacionalidade)&(tabela_21['Versão_Temporada']==temporada)]
            tabela_21 = tabela_21.iloc[:, np.r_[1, 31, 36, 3, 4, 7, 9:12, 15, 18:31]]
            tabela_21 = tabela_21.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Posição_Wyscout':'Posição', 'Versão_Temporada':'Janela de Análise'})
            tabela_21 = tabela_21[(tabela_21['Liga'] == 'ENG1') | (tabela_21['Liga'] == 'ENG2') | (tabela_21['Liga'] == 'FRA1') | (tabela_21['Liga'] == 'FRA2') 
                                | (tabela_21['Liga'] == 'SPA1') | (tabela_21['Liga'] == 'ITA1') | (tabela_21['Liga'] == 'GER1') | (tabela_21['Liga'] == 'POR1') 
                                | (tabela_21['Liga'] == 'SWZ') | (tabela_21['Liga'] == 'RUS') | (tabela_21['Liga'] == 'UKR') | (tabela_21['Liga'] == 'BEL1') 
                                | (tabela_21['Liga'] == 'CHN') | (tabela_21['Liga'] == 'DEN') | (tabela_21['Liga'] == 'GRE') | (tabela_21['Liga'] == 'HOL') 
                                | (tabela_21['Liga'] == 'JAP') | (tabela_21['Liga'] == 'MEX') | (tabela_21['Liga'] == 'SAUD') | (tabela_21['Liga'] == 'TUR') 
                                | (tabela_21['Liga'] == 'UAE') | (tabela_21['Liga'] == 'USA') | (tabela_21['Liga'] == 'ITA2') | (tabela_21['Liga'] == 'GER2') 
                                | (tabela_21['Liga'] == 'POR2') | (tabela_21['Liga'] == 'BUL') | (tabela_21['Liga'] == 'AUT') | (tabela_21['Liga'] == 'QAT')]
            tabela_21 = tabela_21.head(15)
            st.dataframe(tabela_21, use_container_width=True, hide_index=True)

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
if choose == "Free Agents pelo Mundo":
    nacionalidades = df8["Nacionalidade"]
    posições = df6["Posição"]
    funções = df2["Função"]
    contratos = ["2023-12-31", "2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30", "2024-05-31", "2024-06-30"]
    temporada = 2023
    mundo_options = ['ENG1', 'ENG2', 'FRA1', 'FRA2', 'SPA1', 'SPA2', 'ITA1', 'ITA2', 'GER1', 'POR1', 'POR2', 'SWZ', 'CZH', 'CRO', 'SER', 'RUS', 'UKR', 'BEL1', 'BEL2', 'CHN',
             'DEN', 'GRE', 'HOL', 'JAP', 'MEX', 'SAUD', 'SCT', 'TUR', 'UAE', 'USA', 'BUL', 'AUT', 'QAT', 'BRA1', 'ARG1']
    nacionalidade = st.selectbox("Escolha a Nacionalidade do Atleta", options=nacionalidades)
    posição = st.selectbox("Escolha a Posição", options=posições)
    #função = st.selectbox("Escolha a Posição", options=funções)
    contrato = st.selectbox("Escolha a Data de Fim de Contrato", options=contratos)

    if posição == ("Goleiro"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Goleiros</b></h4>", unsafe_allow_html=True)
        tabela_7 = pd.read_excel("1_Role_Goleiro_Full.xlsx")
        tabela_7 = tabela_7.loc[(tabela_7['Nacionalidade']==nacionalidade)&(tabela_7['Fim_Contrato']<=contrato)&(tabela_7['Versão_Temporada']==temporada)]   
        tabela_7 = tabela_7.iloc[:, np.r_[1, 3, 7, 15, 8:12, 25, 26, 27]]
        tabela_7 = tabela_7[(tabela_7['Liga'] == 'ENG1') | (tabela_7['Liga'] == 'ENG2') | (tabela_7['Liga'] == 'FRA1') | (tabela_7['Liga'] == 'FRA2') 
            | (tabela_7['Liga'] == 'SPA1') | (tabela_7['Liga'] == 'ITA1') | (tabela_7['Liga'] == 'GER1') | (tabela_7['Liga'] == 'POR1') 
            | (tabela_7['Liga'] == 'SWZ') | (tabela_7['Liga'] == 'RUS') | (tabela_7['Liga'] == 'UKR') | (tabela_7['Liga'] == 'BEL1') 
            | (tabela_7['Liga'] == 'CHN') | (tabela_7['Liga'] == 'DEN') | (tabela_7['Liga'] == 'GRE') | (tabela_7['Liga'] == 'HOL') 
            | (tabela_7['Liga'] == 'JAP') | (tabela_7['Liga'] == 'MEX') | (tabela_7['Liga'] == 'SAUD') | (tabela_7['Liga'] == 'TUR') 
            | (tabela_7['Liga'] == 'UAE') | (tabela_7['Liga'] == 'USA') | (tabela_7['Liga'] == 'ITA2') | (tabela_7['Liga'] == 'GER2') 
            | (tabela_7['Liga'] == 'POR2') | (tabela_7['Liga'] == 'BUL') | (tabela_7['Liga'] == 'AUT') | (tabela_7['Liga'] == 'QAT')
            | (tabela_7['Liga'] == 'BRA1') | (tabela_7['Liga'] == 'ARG1')]

        tabela_8 = pd.read_excel("PlayerAnalysis_Role_1_Full.xlsx")
        tabela_8 = tabela_8.loc[(tabela_8['Nacionalidade']==nacionalidade)&(tabela_8['Fim_Contrato']<=contrato)&(tabela_8['Versão_Temporada']==temporada)]
        tabela_8 = tabela_8.iloc[:, np.r_[9, 30:34, 26, 28]]
        tabela_8 = tabela_8[(tabela_8['Liga'] == 'ENG1') | (tabela_8['Liga'] == 'ENG2') | (tabela_8['Liga'] == 'FRA1') | (tabela_8['Liga'] == 'FRA2') 
            | (tabela_8['Liga'] == 'SPA1') | (tabela_8['Liga'] == 'ITA1') | (tabela_8['Liga'] == 'GER1') | (tabela_8['Liga'] == 'POR1') 
            | (tabela_8['Liga'] == 'SWZ') | (tabela_8['Liga'] == 'RUS') | (tabela_8['Liga'] == 'UKR') | (tabela_8['Liga'] == 'BEL1') 
            | (tabela_8['Liga'] == 'CHN') | (tabela_8['Liga'] == 'DEN') | (tabela_8['Liga'] == 'GRE') | (tabela_8['Liga'] == 'HOL') 
            | (tabela_8['Liga'] == 'JAP') | (tabela_8['Liga'] == 'MEX') | (tabela_8['Liga'] == 'SAUD') | (tabela_8['Liga'] == 'TUR') 
            | (tabela_8['Liga'] == 'UAE') | (tabela_8['Liga'] == 'USA') | (tabela_8['Liga'] == 'ITA2') | (tabela_8['Liga'] == 'GER2') 
            | (tabela_8['Liga'] == 'POR2') | (tabela_8['Liga'] == 'BUL') | (tabela_8['Liga'] == 'AUT') | (tabela_8['Liga'] == 'QAT') 
            | (tabela_8['Liga'] == 'BRA1') | (tabela_8['Liga'] == 'ARG1')]

        tabela_7 = pd.merge(tabela_7, tabela_8[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_7 = tabela_7.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Goleiros Clássicos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_7, use_container_width=True, hide_index=True)


        tabela_8 = pd.read_excel("2_Role_Goleiro_Líbero_Full.xlsx")
        tabela_8 = tabela_8.loc[(tabela_8['Nacionalidade']==nacionalidade)&(tabela_8['Fim_Contrato']<=contrato)&(tabela_8['Versão_Temporada']==temporada)]   
        tabela_8 = tabela_8.iloc[:, np.r_[1, 3, 7, 15, 8:12, 28, 30]]
        tabela_8 = tabela_8[(tabela_8['Liga'] == 'ENG1') | (tabela_8['Liga'] == 'ENG2') | (tabela_8['Liga'] == 'FRA1') | (tabela_8['Liga'] == 'FRA2') 
            | (tabela_8['Liga'] == 'SPA1') | (tabela_8['Liga'] == 'ITA1') | (tabela_8['Liga'] == 'GER1') | (tabela_8['Liga'] == 'POR1') 
            | (tabela_8['Liga'] == 'SWZ') | (tabela_8['Liga'] == 'RUS') | (tabela_8['Liga'] == 'UKR') | (tabela_8['Liga'] == 'BEL1') 
            | (tabela_8['Liga'] == 'CHN') | (tabela_8['Liga'] == 'DEN') | (tabela_8['Liga'] == 'GRE') | (tabela_8['Liga'] == 'HOL') 
            | (tabela_8['Liga'] == 'JAP') | (tabela_8['Liga'] == 'MEX') | (tabela_8['Liga'] == 'SAUD') | (tabela_8['Liga'] == 'TUR') 
            | (tabela_8['Liga'] == 'UAE') | (tabela_8['Liga'] == 'USA') | (tabela_8['Liga'] == 'ITA2') | (tabela_8['Liga'] == 'GER2') 
            | (tabela_8['Liga'] == 'POR2') | (tabela_8['Liga'] == 'BUL') | (tabela_8['Liga'] == 'AUT') | (tabela_8['Liga'] == 'QAT')
            | (tabela_8['Liga'] == 'BRA1') | (tabela_8['Liga'] == 'ARG1')]

        tabela_9 = pd.read_excel("PlayerAnalysis_Role_2_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]
        tabela_9 = tabela_9.iloc[:, np.r_[12, 33:37, 29, 31]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT') 
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_8 = pd.merge(tabela_8, tabela_9[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_8 = tabela_8.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Goleiros Líberos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_8, use_container_width=True, hide_index=True)


    elif posição == ("Lateral"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Laterais </b></h4>", unsafe_allow_html=True)
        tabela_9 = pd.read_excel("3_Role_Lateral_Defensivo_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]   
        tabela_9 = tabela_9.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 24]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT')
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_10 = pd.read_excel("PlayerAnalysis_Role_3_Full.xlsx")
        tabela_10 = tabela_10.loc[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Fim_Contrato']<=contrato)&(tabela_10['Versão_Temporada']==temporada)]
        tabela_10 = tabela_10.iloc[:, np.r_[8, 25, 29:33]]
        tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
            | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
            | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
            | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
            | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
            | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
            | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT') 
            | (tabela_10['Liga'] == 'BRA1') | (tabela_10['Liga'] == 'ARG1')]

        tabela_9 = pd.merge(tabela_9, tabela_10[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Laterais Defensivos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_9, use_container_width=True, hide_index=True)


        tabela_11 = pd.read_excel("4_Role_Lateral_Ofensivo_Full.xlsx")
        tabela_11 = tabela_11.loc[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Fim_Contrato']<=contrato)&(tabela_11['Versão_Temporada']==temporada)]   
        tabela_11 = tabela_11.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 33]]
        tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
            | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
            | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
            | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
            | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
            | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
            | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT') 
            | (tabela_11['Liga'] == 'BRA1') | (tabela_11['Liga'] == 'ARG1')]

        tabela_12 = pd.read_excel("PlayerAnalysis_Role_4_Full.xlsx")
        tabela_12 = tabela_12.loc[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Fim_Contrato']<=contrato)&(tabela_12['Versão_Temporada']==temporada)]
        tabela_12 = tabela_12.iloc[:, np.r_[17, 34, 38:42]]
        tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
            | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
            | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
            | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
            | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
            | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
            | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT') 
            | (tabela_12['Liga'] == 'BRA1') | (tabela_12['Liga'] == 'ARG1')]

        tabela_11 = pd.merge(tabela_11, tabela_12[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})

        st.markdown("<h4 style='text-align: center;'>Laterais Ofensivos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_11, use_container_width=True, hide_index=True)


        tabela_13 = pd.read_excel("5_Role_Lateral_Equilibrado_Full.xlsx")
        tabela_13 = tabela_13.loc[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Fim_Contrato']<=contrato)&(tabela_13['Versão_Temporada']==temporada)]   
        tabela_13 = tabela_13.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 36]]
        tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
            | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
            | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
            | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
            | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
            | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
            | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT') 
            | (tabela_13['Liga'] == 'BRA1') | (tabela_13['Liga'] == 'ARG1')]

        tabela_14 = pd.read_excel("PlayerAnalysis_Role_5_Full.xlsx")
        tabela_14 = tabela_14.loc[(tabela_14['Nacionalidade']==nacionalidade)&(tabela_14['Fim_Contrato']<=contrato)&(tabela_14['Versão_Temporada']==temporada)]
        tabela_14 = tabela_14.iloc[:, np.r_[20, 37, 41:45]]
        tabela_14 = tabela_14[(tabela_14['Liga'] == 'ENG1') | (tabela_14['Liga'] == 'ENG2') | (tabela_14['Liga'] == 'FRA1') | (tabela_14['Liga'] == 'FRA2') 
            | (tabela_14['Liga'] == 'SPA1') | (tabela_14['Liga'] == 'ITA1') | (tabela_14['Liga'] == 'GER1') | (tabela_14['Liga'] == 'POR1') 
            | (tabela_14['Liga'] == 'SWZ') | (tabela_14['Liga'] == 'RUS') | (tabela_14['Liga'] == 'UKR') | (tabela_14['Liga'] == 'BEL1') 
            | (tabela_14['Liga'] == 'CHN') | (tabela_14['Liga'] == 'DEN') | (tabela_14['Liga'] == 'GRE') | (tabela_14['Liga'] == 'HOL') 
            | (tabela_14['Liga'] == 'JAP') | (tabela_14['Liga'] == 'MEX') | (tabela_14['Liga'] == 'SAUD') | (tabela_14['Liga'] == 'TUR') 
            | (tabela_14['Liga'] == 'UAE') | (tabela_14['Liga'] == 'USA') | (tabela_14['Liga'] == 'ITA2') | (tabela_14['Liga'] == 'GER2') 
            | (tabela_14['Liga'] == 'POR2') | (tabela_14['Liga'] == 'BUL') | (tabela_14['Liga'] == 'AUT') | (tabela_14['Liga'] == 'QAT') 
            | (tabela_14['Liga'] == 'BRA1') | (tabela_14['Liga'] == 'ARG1')]

        tabela_13 = pd.merge(tabela_13, tabela_14[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Laterais Equilibrados </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_13, use_container_width=True, hide_index=True)

    elif posição == ("Zagueiro"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Zagueiros </b></h4>", unsafe_allow_html=True)
        tabela_9 = pd.read_excel("6_Role_Zagueiro_Defensivo_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]   
        tabela_9 = tabela_9.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 24]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT') 
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_10 = pd.read_excel("PlayerAnalysis_Role_6_Full.xlsx")
        tabela_10 = tabela_10.loc[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Fim_Contrato']<=contrato)&(tabela_10['Versão_Temporada']==temporada)]
        tabela_10 = tabela_10.iloc[:, np.r_[8, 25, 29:33]]
        tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
            | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
            | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
            | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
            | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
            | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
            | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT') 
            | (tabela_10['Liga'] == 'BRA1') | (tabela_10['Liga'] == 'ARG1')]

        tabela_9 = pd.merge(tabela_9, tabela_10[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Zagueiros Clássicos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_9, use_container_width=True, hide_index=True)


        tabela_11 = pd.read_excel("7_Role_Zagueiro_Construtor_Full.xlsx")
        tabela_11 = tabela_11.loc[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Fim_Contrato']<=contrato)&(tabela_11['Versão_Temporada']==temporada)]   
        tabela_11 = tabela_11.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 28]]
        tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
            | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
            | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
            | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
            | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
            | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
            | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT') 
            | (tabela_11['Liga'] == 'BRA1') | (tabela_11['Liga'] == 'ARG1')]

        tabela_12 = pd.read_excel("PlayerAnalysis_Role_7_Full.xlsx")
        tabela_12 = tabela_12.loc[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Fim_Contrato']<=contrato)&(tabela_12['Versão_Temporada']==temporada)]
        tabela_12 = tabela_12.iloc[:, np.r_[12, 29, 33:37]]
        tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
            | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
            | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
            | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
            | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
            | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
            | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT') 
            | (tabela_12['Liga'] == 'BRA1') | (tabela_12['Liga'] == 'ARG1')]

        tabela_11 = pd.merge(tabela_11, tabela_12[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})

        st.markdown("<h4 style='text-align: center;'>Zagueiros Construtores </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_11, use_container_width=True, hide_index=True)


        tabela_13 = pd.read_excel("8_Role_Zagueiro_Equilibrado_Full.xlsx")
        tabela_13 = tabela_13.loc[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Fim_Contrato']<=contrato)&(tabela_13['Versão_Temporada']==temporada)]   
        tabela_13 = tabela_13.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 31]]
        tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
            | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
            | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
            | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
            | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
            | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
            | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT') 
            | (tabela_13['Liga'] == 'BRA1') | (tabela_13['Liga'] == 'ARG1')]

        tabela_14 = pd.read_excel("PlayerAnalysis_Role_8_Full.xlsx")
        tabela_14 = tabela_14.loc[(tabela_14['Nacionalidade']==nacionalidade)&(tabela_14['Fim_Contrato']<=contrato)&(tabela_14['Versão_Temporada']==temporada)]
        tabela_14 = tabela_14.iloc[:, np.r_[15, 32, 36:40]]
        tabela_14 = tabela_14[(tabela_14['Liga'] == 'ENG1') | (tabela_14['Liga'] == 'ENG2') | (tabela_14['Liga'] == 'FRA1') | (tabela_14['Liga'] == 'FRA2') 
            | (tabela_14['Liga'] == 'SPA1') | (tabela_14['Liga'] == 'ITA1') | (tabela_14['Liga'] == 'GER1') | (tabela_14['Liga'] == 'POR1') 
            | (tabela_14['Liga'] == 'SWZ') | (tabela_14['Liga'] == 'RUS') | (tabela_14['Liga'] == 'UKR') | (tabela_14['Liga'] == 'BEL1') 
            | (tabela_14['Liga'] == 'CHN') | (tabela_14['Liga'] == 'DEN') | (tabela_14['Liga'] == 'GRE') | (tabela_14['Liga'] == 'HOL') 
            | (tabela_14['Liga'] == 'JAP') | (tabela_14['Liga'] == 'MEX') | (tabela_14['Liga'] == 'SAUD') | (tabela_14['Liga'] == 'TUR') 
            | (tabela_14['Liga'] == 'UAE') | (tabela_14['Liga'] == 'USA') | (tabela_14['Liga'] == 'ITA2') | (tabela_14['Liga'] == 'GER2') 
            | (tabela_14['Liga'] == 'POR2') | (tabela_14['Liga'] == 'BUL') | (tabela_14['Liga'] == 'AUT') | (tabela_14['Liga'] == 'QAT') 
            | (tabela_14['Liga'] == 'BRA1') | (tabela_14['Liga'] == 'ARG1')]

        tabela_13 = pd.merge(tabela_13, tabela_14[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Zagueiros Equilibrados </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_13, use_container_width=True, hide_index=True)

###############################################################################################################################
###############################################################################################################################

    elif posição == ("Primeiro Volante"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Primeiros Volantes </b></h4>", unsafe_allow_html=True)
        tabela_9 = pd.read_excel("9_Role_Volante_Defensivo_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]   
        tabela_9 = tabela_9.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 22]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT')
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_10 = pd.read_excel("PlayerAnalysis_Role_9_Full.xlsx")
        tabela_10 = tabela_10.loc[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Fim_Contrato']<=contrato)&(tabela_10['Versão_Temporada']==temporada)]
        tabela_10 = tabela_10.iloc[:, np.r_[6, 23, 27:31]]
        tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
            | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
            | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
            | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
            | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
            | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
            | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT')
            | (tabela_10['Liga'] == 'BRA1') | (tabela_10['Liga'] == 'ARG1')]

        tabela_9 = pd.merge(tabela_9, tabela_10[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Primeiros Volantes Defensivos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_9, use_container_width=True, hide_index=True)


        tabela_11 = pd.read_excel("10_Role_Volante_Construtor_Full.xlsx")
        tabela_11 = tabela_11.loc[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Fim_Contrato']<=contrato)&(tabela_11['Versão_Temporada']==temporada)]   
        tabela_11 = tabela_11.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 27]]
        tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
            | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
            | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
            | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
            | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
            | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
            | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT')
            | (tabela_11['Liga'] == 'BRA1') | (tabela_11['Liga'] == 'ARG1')]

        tabela_12 = pd.read_excel("PlayerAnalysis_Role_10_Full.xlsx")
        tabela_12 = tabela_12.loc[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Fim_Contrato']<=contrato)&(tabela_12['Versão_Temporada']==temporada)]
        tabela_12 = tabela_12.iloc[:, np.r_[11, 28, 32:36]]
        tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
            | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
            | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
            | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
            | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
            | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
            | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT')
            | (tabela_12['Liga'] == 'BRA1') | (tabela_12['Liga'] == 'ARG1')]

        tabela_11 = pd.merge(tabela_11, tabela_12[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})

        st.markdown("<h4 style='text-align: center;'>Primeiros Volantes Construtores </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_11, use_container_width=True, hide_index=True)


        tabela_13 = pd.read_excel("11_Role_Volante_Equilibrado_Full.xlsx")
        tabela_13 = tabela_13.loc[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Fim_Contrato']<=contrato)&(tabela_13['Versão_Temporada']==temporada)]   
        tabela_13 = tabela_13.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 29]]
        tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
            | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
            | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
            | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
            | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
            | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
            | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT')
            | (tabela_13['Liga'] == 'BRA1') | (tabela_13['Liga'] == 'ARG1')]

        tabela_14 = pd.read_excel("PlayerAnalysis_Role_11_Full.xlsx")
        tabela_14 = tabela_14.loc[(tabela_14['Nacionalidade']==nacionalidade)&(tabela_14['Fim_Contrato']<=contrato)&(tabela_14['Versão_Temporada']==temporada)]
        tabela_14 = tabela_14.iloc[:, np.r_[13, 30, 34:38]]
        tabela_14 = tabela_14[(tabela_14['Liga'] == 'ENG1') | (tabela_14['Liga'] == 'ENG2') | (tabela_14['Liga'] == 'FRA1') | (tabela_14['Liga'] == 'FRA2') 
            | (tabela_14['Liga'] == 'SPA1') | (tabela_14['Liga'] == 'ITA1') | (tabela_14['Liga'] == 'GER1') | (tabela_14['Liga'] == 'POR1') 
            | (tabela_14['Liga'] == 'SWZ') | (tabela_14['Liga'] == 'RUS') | (tabela_14['Liga'] == 'UKR') | (tabela_14['Liga'] == 'BEL1') 
            | (tabela_14['Liga'] == 'CHN') | (tabela_14['Liga'] == 'DEN') | (tabela_14['Liga'] == 'GRE') | (tabela_14['Liga'] == 'HOL') 
            | (tabela_14['Liga'] == 'JAP') | (tabela_14['Liga'] == 'MEX') | (tabela_14['Liga'] == 'SAUD') | (tabela_14['Liga'] == 'TUR') 
            | (tabela_14['Liga'] == 'UAE') | (tabela_14['Liga'] == 'USA') | (tabela_14['Liga'] == 'ITA2') | (tabela_14['Liga'] == 'GER2') 
            | (tabela_14['Liga'] == 'POR2') | (tabela_14['Liga'] == 'BUL') | (tabela_14['Liga'] == 'AUT') | (tabela_14['Liga'] == 'QAT')
            | (tabela_14['Liga'] == 'BRA1') | (tabela_14['Liga'] == 'ARG1')]

        tabela_13 = pd.merge(tabela_13, tabela_14[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Primeiros Volantes Equilibrados </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_13, use_container_width=True, hide_index=True)

###############################################################################################################################
###############################################################################################################################

    elif posição == ("Segundo Volante"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Segundos Volantes </b></h4>", unsafe_allow_html=True)
        tabela_9 = pd.read_excel("12_Role_Segundo_Volante_Box_to_Box_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]   
        tabela_9 = tabela_9.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 31]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT')
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_10 = pd.read_excel("PlayerAnalysis_Role_12_Full.xlsx")
        tabela_10 = tabela_10.loc[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Fim_Contrato']<=contrato)&(tabela_10['Versão_Temporada']==temporada)]
        tabela_10 = tabela_10.iloc[:, np.r_[15, 32, 36:40]]
        tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
            | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
            | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
            | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
            | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
            | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
            | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT')
            | (tabela_10['Liga'] == 'BRA1') | (tabela_10['Liga'] == 'ARG1')]

        tabela_9 = pd.merge(tabela_9, tabela_10[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Segundos Volantes Box-to-Box </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_9, use_container_width=True, hide_index=True)


        tabela_11 = pd.read_excel("13_Role_Segundo_Volante_Organizador_Full.xlsx")
        tabela_11 = tabela_11.loc[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Fim_Contrato']<=contrato)&(tabela_11['Versão_Temporada']==temporada)]   
        tabela_11 = tabela_11.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 28]]
        tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
            | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
            | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
            | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
            | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
            | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
            | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT') 
            | (tabela_11['Liga'] == 'BRA1') | (tabela_11['Liga'] == 'ARG1')]

        tabela_12 = pd.read_excel("PlayerAnalysis_Role_13_Full.xlsx")
        tabela_12 = tabela_12.loc[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Fim_Contrato']<=contrato)&(tabela_12['Versão_Temporada']==temporada)]
        tabela_12 = tabela_12.iloc[:, np.r_[12, 29, 33:37]]
        tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
            | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
            | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
            | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
            | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
            | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
            | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT') 
            | (tabela_12['Liga'] == 'BRA1') | (tabela_12['Liga'] == 'ARG1')]

        tabela_11 = pd.merge(tabela_11, tabela_12[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})

        st.markdown("<h4 style='text-align: center;'>Segundos Volantes Organizadores </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_11, use_container_width=True, hide_index=True)


        tabela_13 = pd.read_excel("14_Role_Segundo_Volante_Equilibrado_Full.xlsx")
        tabela_13 = tabela_13.loc[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Fim_Contrato']<=contrato)&(tabela_13['Versão_Temporada']==temporada)]   
        tabela_13 = tabela_13.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 31]]
        tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
            | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
            | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
            | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
            | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
            | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
            | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT') 
            | (tabela_13['Liga'] == 'BRA1') | (tabela_13['Liga'] == 'ARG1')]

        tabela_14 = pd.read_excel("PlayerAnalysis_Role_14_Full.xlsx")
        tabela_14 = tabela_14.loc[(tabela_14['Nacionalidade']==nacionalidade)&(tabela_14['Fim_Contrato']<=contrato)&(tabela_14['Versão_Temporada']==temporada)]
        tabela_14 = tabela_14.iloc[:, np.r_[15, 32, 36:40]]
        tabela_14 = tabela_14[(tabela_14['Liga'] == 'ENG1') | (tabela_14['Liga'] == 'ENG2') | (tabela_14['Liga'] == 'FRA1') | (tabela_14['Liga'] == 'FRA2') 
            | (tabela_14['Liga'] == 'SPA1') | (tabela_14['Liga'] == 'ITA1') | (tabela_14['Liga'] == 'GER1') | (tabela_14['Liga'] == 'POR1') 
            | (tabela_14['Liga'] == 'SWZ') | (tabela_14['Liga'] == 'RUS') | (tabela_14['Liga'] == 'UKR') | (tabela_14['Liga'] == 'BEL1') 
            | (tabela_14['Liga'] == 'CHN') | (tabela_14['Liga'] == 'DEN') | (tabela_14['Liga'] == 'GRE') | (tabela_14['Liga'] == 'HOL') 
            | (tabela_14['Liga'] == 'JAP') | (tabela_14['Liga'] == 'MEX') | (tabela_14['Liga'] == 'SAUD') | (tabela_14['Liga'] == 'TUR') 
            | (tabela_14['Liga'] == 'UAE') | (tabela_14['Liga'] == 'USA') | (tabela_14['Liga'] == 'ITA2') | (tabela_14['Liga'] == 'GER2') 
            | (tabela_14['Liga'] == 'POR2') | (tabela_14['Liga'] == 'BUL') | (tabela_14['Liga'] == 'AUT') | (tabela_14['Liga'] == 'QAT') 
            | (tabela_14['Liga'] == 'BRA1') | (tabela_14['Liga'] == 'ARG1')]

        tabela_13 = pd.merge(tabela_13, tabela_14[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Segundos Volantes Equilibrados </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_13, use_container_width=True, hide_index=True)

###############################################################################################################################
###############################################################################################################################

    elif posição == ("Meia"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Meias </b></h4>", unsafe_allow_html=True)
        tabela_9 = pd.read_excel("15_Role_Meia_Organizador_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]   
        tabela_9 = tabela_9.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 28]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT') 
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_10 = pd.read_excel("PlayerAnalysis_Role_15_Full.xlsx")
        tabela_10 = tabela_10.loc[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Fim_Contrato']<=contrato)&(tabela_10['Versão_Temporada']==temporada)]
        tabela_10 = tabela_10.iloc[:, np.r_[12, 29, 33:37]]
        tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
            | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
            | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
            | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
            | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
            | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
            | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT') 
            | (tabela_10['Liga'] == 'BRA1') | (tabela_10['Liga'] == 'ARG1')]

        tabela_9 = pd.merge(tabela_9, tabela_10[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Meias Organizadores </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_9, use_container_width=True, hide_index=True)


        tabela_11 = pd.read_excel("16_Role_Meia_Atacante_Full.xlsx")
        tabela_11 = tabela_11.loc[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Fim_Contrato']<=contrato)&(tabela_11['Versão_Temporada']==temporada)]   
        tabela_11 = tabela_11.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 35]]
        tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
            | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
            | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
            | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
            | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
            | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
            | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT') 
            | (tabela_11['Liga'] == 'BRA1') | (tabela_11['Liga'] == 'ARG1')]

        tabela_12 = pd.read_excel("PlayerAnalysis_Role_16_Full.xlsx")
        tabela_12 = tabela_12.loc[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Fim_Contrato']<=contrato)&(tabela_12['Versão_Temporada']==temporada)]
        tabela_12 = tabela_12.iloc[:, np.r_[19, 36, 40:44]]
        tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
            | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
            | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
            | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
            | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
            | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
            | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT') 
            | (tabela_12['Liga'] == 'BRA1') | (tabela_12['Liga'] == 'ARG1')]

        tabela_11 = pd.merge(tabela_11, tabela_12[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})

        st.markdown("<h4 style='text-align: center;'>Meias Atacantes </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_11, use_container_width=True, hide_index=True)


###############################################################################################################################
###############################################################################################################################

    elif posição == ("Extremo"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Extremos </b></h4>", unsafe_allow_html=True)
        tabela_9 = pd.read_excel("17_Role_Extremo_Organizador_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]   
        tabela_9 = tabela_9.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 31]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT') 
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_10 = pd.read_excel("PlayerAnalysis_Role_17_Full.xlsx")
        tabela_10 = tabela_10.loc[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Fim_Contrato']<=contrato)&(tabela_10['Versão_Temporada']==temporada)]
        tabela_10 = tabela_10.iloc[:, np.r_[15, 32, 36:40]]
        tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
            | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
            | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
            | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
            | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
            | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
            | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT') 
            | (tabela_10['Liga'] == 'BRA1') | (tabela_10['Liga'] == 'ARG1')]

        tabela_9 = pd.merge(tabela_9, tabela_10[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Extremos Organizadores </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_9, use_container_width=True, hide_index=True)


        tabela_11 = pd.read_excel("18_Role_Extremo_Tático_Full.xlsx")
        tabela_11 = tabela_11.loc[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Fim_Contrato']<=contrato)&(tabela_11['Versão_Temporada']==temporada)]   
        tabela_11 = tabela_11.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 25]]
        tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
            | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
            | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
            | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
            | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
            | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
            | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT') 
            | (tabela_11['Liga'] == 'BRA1') | (tabela_11['Liga'] == 'ARG1')]

        tabela_12 = pd.read_excel("PlayerAnalysis_Role_18_Full.xlsx")
        tabela_12 = tabela_12.loc[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Fim_Contrato']<=contrato)&(tabela_12['Versão_Temporada']==temporada)]
        tabela_12 = tabela_12.iloc[:, np.r_[9, 26, 30:34]]
        tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
            | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
            | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
            | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
            | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
            | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
            | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT')
            | (tabela_12['Liga'] == 'BRA1') | (tabela_12['Liga'] == 'ARG1')]

        tabela_11 = pd.merge(tabela_11, tabela_12[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})

        st.markdown("<h4 style='text-align: center;'>Extremos Táticos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_11, use_container_width=True, hide_index=True)


        tabela_13 = pd.read_excel("19_Role_Extremo_Agudo_Full.xlsx")
        tabela_13 = tabela_13.loc[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Fim_Contrato']<=contrato)&(tabela_13['Versão_Temporada']==temporada)]   
        tabela_13 = tabela_13.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 31]]
        tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
            | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
            | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
            | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
            | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
            | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
            | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT')
            | (tabela_13['Liga'] == 'BRA1') | (tabela_13['Liga'] == 'ARG1')]

        tabela_14 = pd.read_excel("PlayerAnalysis_Role_19_Full.xlsx")
        tabela_14 = tabela_14.loc[(tabela_14['Nacionalidade']==nacionalidade)&(tabela_14['Fim_Contrato']<=contrato)&(tabela_14['Versão_Temporada']==temporada)]
        tabela_14 = tabela_14.iloc[:, np.r_[15, 32, 36:40]]
        tabela_14 = tabela_14[(tabela_14['Liga'] == 'ENG1') | (tabela_14['Liga'] == 'ENG2') | (tabela_14['Liga'] == 'FRA1') | (tabela_14['Liga'] == 'FRA2') 
            | (tabela_14['Liga'] == 'SPA1') | (tabela_14['Liga'] == 'ITA1') | (tabela_14['Liga'] == 'GER1') | (tabela_14['Liga'] == 'POR1') 
            | (tabela_14['Liga'] == 'SWZ') | (tabela_14['Liga'] == 'RUS') | (tabela_14['Liga'] == 'UKR') | (tabela_14['Liga'] == 'BEL1') 
            | (tabela_14['Liga'] == 'CHN') | (tabela_14['Liga'] == 'DEN') | (tabela_14['Liga'] == 'GRE') | (tabela_14['Liga'] == 'HOL') 
            | (tabela_14['Liga'] == 'JAP') | (tabela_14['Liga'] == 'MEX') | (tabela_14['Liga'] == 'SAUD') | (tabela_14['Liga'] == 'TUR') 
            | (tabela_14['Liga'] == 'UAE') | (tabela_14['Liga'] == 'USA') | (tabela_14['Liga'] == 'ITA2') | (tabela_14['Liga'] == 'GER2') 
            | (tabela_14['Liga'] == 'POR2') | (tabela_14['Liga'] == 'BUL') | (tabela_14['Liga'] == 'AUT') | (tabela_14['Liga'] == 'QAT') 
            | (tabela_14['Liga'] == 'BRA1') | (tabela_14['Liga'] == 'ARG1')]

        tabela_13 = pd.merge(tabela_13, tabela_14[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Extremos Agudos </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_13, use_container_width=True, hide_index=True)

###############################################################################################################################
###############################################################################################################################

    elif posição == ("Atacante"):
        st.markdown("<h4 style='text-align: center;'>Free Agents Nacionais Mais Bem Ranqueados<br>Atacantes </b></h4>", unsafe_allow_html=True)
        tabela_9 = pd.read_excel("20_Role_Atacante_Referência_Full.xlsx")
        tabela_9 = tabela_9.loc[(tabela_9['Nacionalidade']==nacionalidade)&(tabela_9['Fim_Contrato']<=contrato)&(tabela_9['Versão_Temporada']==temporada)]   
        tabela_9 = tabela_9.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 28]]
        tabela_9 = tabela_9[(tabela_9['Liga'] == 'ENG1') | (tabela_9['Liga'] == 'ENG2') | (tabela_9['Liga'] == 'FRA1') | (tabela_9['Liga'] == 'FRA2') 
            | (tabela_9['Liga'] == 'SPA1') | (tabela_9['Liga'] == 'ITA1') | (tabela_9['Liga'] == 'GER1') | (tabela_9['Liga'] == 'POR1') 
            | (tabela_9['Liga'] == 'SWZ') | (tabela_9['Liga'] == 'RUS') | (tabela_9['Liga'] == 'UKR') | (tabela_9['Liga'] == 'BEL1') 
            | (tabela_9['Liga'] == 'CHN') | (tabela_9['Liga'] == 'DEN') | (tabela_9['Liga'] == 'GRE') | (tabela_9['Liga'] == 'HOL') 
            | (tabela_9['Liga'] == 'JAP') | (tabela_9['Liga'] == 'MEX') | (tabela_9['Liga'] == 'SAUD') | (tabela_9['Liga'] == 'TUR') 
            | (tabela_9['Liga'] == 'UAE') | (tabela_9['Liga'] == 'USA') | (tabela_9['Liga'] == 'ITA2') | (tabela_9['Liga'] == 'GER2') 
            | (tabela_9['Liga'] == 'POR2') | (tabela_9['Liga'] == 'BUL') | (tabela_9['Liga'] == 'AUT') | (tabela_9['Liga'] == 'QAT') 
            | (tabela_9['Liga'] == 'BRA1') | (tabela_9['Liga'] == 'ARG1')]

        tabela_10 = pd.read_excel("PlayerAnalysis_Role_20_Full.xlsx")
        tabela_10 = tabela_10.loc[(tabela_10['Nacionalidade']==nacionalidade)&(tabela_10['Fim_Contrato']<=contrato)&(tabela_10['Versão_Temporada']==temporada)]
        tabela_10 = tabela_10.iloc[:, np.r_[12, 29, 33:37]]
        tabela_10 = tabela_10[(tabela_10['Liga'] == 'ENG1') | (tabela_10['Liga'] == 'ENG2') | (tabela_10['Liga'] == 'FRA1') | (tabela_10['Liga'] == 'FRA2') 
            | (tabela_10['Liga'] == 'SPA1') | (tabela_10['Liga'] == 'ITA1') | (tabela_10['Liga'] == 'GER1') | (tabela_10['Liga'] == 'POR1') 
            | (tabela_10['Liga'] == 'SWZ') | (tabela_10['Liga'] == 'RUS') | (tabela_10['Liga'] == 'UKR') | (tabela_10['Liga'] == 'BEL1') 
            | (tabela_10['Liga'] == 'CHN') | (tabela_10['Liga'] == 'DEN') | (tabela_10['Liga'] == 'GRE') | (tabela_10['Liga'] == 'HOL') 
            | (tabela_10['Liga'] == 'JAP') | (tabela_10['Liga'] == 'MEX') | (tabela_10['Liga'] == 'SAUD') | (tabela_10['Liga'] == 'TUR') 
            | (tabela_10['Liga'] == 'UAE') | (tabela_10['Liga'] == 'USA') | (tabela_10['Liga'] == 'ITA2') | (tabela_10['Liga'] == 'GER2') 
            | (tabela_10['Liga'] == 'POR2') | (tabela_10['Liga'] == 'BUL') | (tabela_10['Liga'] == 'AUT') | (tabela_10['Liga'] == 'QAT') 
            | (tabela_10['Liga'] == 'BRA1') | (tabela_10['Liga'] == 'ARG1')]

        tabela_9 = pd.merge(tabela_9, tabela_10[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_9 = tabela_9.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Atacantes Referência </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_9, use_container_width=True, hide_index=True)


        tabela_11 = pd.read_excel("21_Role_Atacante_Móvel_Full.xlsx")
        tabela_11 = tabela_11.loc[(tabela_11['Nacionalidade']==nacionalidade)&(tabela_11['Fim_Contrato']<=contrato)&(tabela_11['Versão_Temporada']==temporada)]   
        tabela_11 = tabela_11.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 27]]
        tabela_11 = tabela_11[(tabela_11['Liga'] == 'ENG1') | (tabela_11['Liga'] == 'ENG2') | (tabela_11['Liga'] == 'FRA1') | (tabela_11['Liga'] == 'FRA2') 
            | (tabela_11['Liga'] == 'SPA1') | (tabela_11['Liga'] == 'ITA1') | (tabela_11['Liga'] == 'GER1') | (tabela_11['Liga'] == 'POR1') 
            | (tabela_11['Liga'] == 'SWZ') | (tabela_11['Liga'] == 'RUS') | (tabela_11['Liga'] == 'UKR') | (tabela_11['Liga'] == 'BEL1') 
            | (tabela_11['Liga'] == 'CHN') | (tabela_11['Liga'] == 'DEN') | (tabela_11['Liga'] == 'GRE') | (tabela_11['Liga'] == 'HOL') 
            | (tabela_11['Liga'] == 'JAP') | (tabela_11['Liga'] == 'MEX') | (tabela_11['Liga'] == 'SAUD') | (tabela_11['Liga'] == 'TUR') 
            | (tabela_11['Liga'] == 'UAE') | (tabela_11['Liga'] == 'USA') | (tabela_11['Liga'] == 'ITA2') | (tabela_11['Liga'] == 'GER2') 
            | (tabela_11['Liga'] == 'POR2') | (tabela_11['Liga'] == 'BUL') | (tabela_11['Liga'] == 'AUT') | (tabela_11['Liga'] == 'QAT') 
            | (tabela_11['Liga'] == 'BRA1') | (tabela_11['Liga'] == 'ARG1')]

        tabela_12 = pd.read_excel("PlayerAnalysis_Role_21_Full.xlsx")
        tabela_12 = tabela_12.loc[(tabela_12['Nacionalidade']==nacionalidade)&(tabela_12['Fim_Contrato']<=contrato)&(tabela_12['Versão_Temporada']==temporada)]
        tabela_12 = tabela_12.iloc[:, np.r_[11, 28, 32:36]]
        tabela_12 = tabela_12[(tabela_12['Liga'] == 'ENG1') | (tabela_12['Liga'] == 'ENG2') | (tabela_12['Liga'] == 'FRA1') | (tabela_12['Liga'] == 'FRA2') 
            | (tabela_12['Liga'] == 'SPA1') | (tabela_12['Liga'] == 'ITA1') | (tabela_12['Liga'] == 'GER1') | (tabela_12['Liga'] == 'POR1') 
            | (tabela_12['Liga'] == 'SWZ') | (tabela_12['Liga'] == 'RUS') | (tabela_12['Liga'] == 'UKR') | (tabela_12['Liga'] == 'BEL1') 
            | (tabela_12['Liga'] == 'CHN') | (tabela_12['Liga'] == 'DEN') | (tabela_12['Liga'] == 'GRE') | (tabela_12['Liga'] == 'HOL') 
            | (tabela_12['Liga'] == 'JAP') | (tabela_12['Liga'] == 'MEX') | (tabela_12['Liga'] == 'SAUD') | (tabela_12['Liga'] == 'TUR') 
            | (tabela_12['Liga'] == 'UAE') | (tabela_12['Liga'] == 'USA') | (tabela_12['Liga'] == 'ITA2') | (tabela_12['Liga'] == 'GER2') 
            | (tabela_12['Liga'] == 'POR2') | (tabela_12['Liga'] == 'BUL') | (tabela_12['Liga'] == 'AUT') | (tabela_12['Liga'] == 'QAT') 
            | (tabela_12['Liga'] == 'BRA1') | (tabela_12['Liga'] == 'ARG1')]

        tabela_11 = pd.merge(tabela_11, tabela_12[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_11 = tabela_11.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})

        st.markdown("<h4 style='text-align: center;'>Atacantes Móveis </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_11, use_container_width=True, hide_index=True)


        tabela_13 = pd.read_excel("22_Role_Segundo_Atacante_Full.xlsx")
        tabela_13 = tabela_13.loc[(tabela_13['Nacionalidade']==nacionalidade)&(tabela_13['Fim_Contrato']<=contrato)&(tabela_13['Versão_Temporada']==temporada)]   
        tabela_13 = tabela_13.iloc[:, np.r_[1, 3, 4, 7, 15, 8:12, 31]]
        tabela_13 = tabela_13[(tabela_13['Liga'] == 'ENG1') | (tabela_13['Liga'] == 'ENG2') | (tabela_13['Liga'] == 'FRA1') | (tabela_13['Liga'] == 'FRA2') 
            | (tabela_13['Liga'] == 'SPA1') | (tabela_13['Liga'] == 'ITA1') | (tabela_13['Liga'] == 'GER1') | (tabela_13['Liga'] == 'POR1') 
            | (tabela_13['Liga'] == 'SWZ') | (tabela_13['Liga'] == 'RUS') | (tabela_13['Liga'] == 'UKR') | (tabela_13['Liga'] == 'BEL1') 
            | (tabela_13['Liga'] == 'CHN') | (tabela_13['Liga'] == 'DEN') | (tabela_13['Liga'] == 'GRE') | (tabela_13['Liga'] == 'HOL') 
            | (tabela_13['Liga'] == 'JAP') | (tabela_13['Liga'] == 'MEX') | (tabela_13['Liga'] == 'SAUD') | (tabela_13['Liga'] == 'TUR') 
            | (tabela_13['Liga'] == 'UAE') | (tabela_13['Liga'] == 'USA') | (tabela_13['Liga'] == 'ITA2') | (tabela_13['Liga'] == 'GER2') 
            | (tabela_13['Liga'] == 'POR2') | (tabela_13['Liga'] == 'BUL') | (tabela_13['Liga'] == 'AUT') | (tabela_13['Liga'] == 'QAT') 
            | (tabela_13['Liga'] == 'BRA1') | (tabela_13['Liga'] == 'ARG1')]

        tabela_14 = pd.read_excel("PlayerAnalysis_Role_22_Full.xlsx")
        tabela_14 = tabela_14.loc[(tabela_14['Nacionalidade']==nacionalidade)&(tabela_14['Fim_Contrato']<=contrato)&(tabela_14['Versão_Temporada']==temporada)]
        tabela_14 = tabela_14.iloc[:, np.r_[15, 32, 36:40]]
        tabela_14 = tabela_14[(tabela_14['Liga'] == 'ENG1') | (tabela_14['Liga'] == 'ENG2') | (tabela_14['Liga'] == 'FRA1') | (tabela_14['Liga'] == 'FRA2') 
            | (tabela_14['Liga'] == 'SPA1') | (tabela_14['Liga'] == 'ITA1') | (tabela_14['Liga'] == 'GER1') | (tabela_14['Liga'] == 'POR1') 
            | (tabela_14['Liga'] == 'SWZ') | (tabela_14['Liga'] == 'RUS') | (tabela_14['Liga'] == 'UKR') | (tabela_14['Liga'] == 'BEL1') 
            | (tabela_14['Liga'] == 'CHN') | (tabela_14['Liga'] == 'DEN') | (tabela_14['Liga'] == 'GRE') | (tabela_14['Liga'] == 'HOL') 
            | (tabela_14['Liga'] == 'JAP') | (tabela_14['Liga'] == 'MEX') | (tabela_14['Liga'] == 'SAUD') | (tabela_14['Liga'] == 'TUR') 
            | (tabela_14['Liga'] == 'UAE') | (tabela_14['Liga'] == 'USA') | (tabela_14['Liga'] == 'ITA2') | (tabela_14['Liga'] == 'GER2') 
            | (tabela_14['Liga'] == 'POR2') | (tabela_14['Liga'] == 'BUL') | (tabela_14['Liga'] == 'AUT') | (tabela_14['Liga'] == 'QAT')
            | (tabela_14['Liga'] == 'BRA1') | (tabela_14['Liga'] == 'ARG1')]

        tabela_13 = pd.merge(tabela_13, tabela_14[['Atleta', 'L_Rating', 'L_Ranking', 'L_Percentil', 'Size']], on="Atleta", how="left")
        tabela_13 = tabela_13.rename(columns={'Equipe_Janela_Análise':'Equipe', 'Versão_Temporada':'Janela de Análise', 
                                            'L_Rating':'Rating', 'L_Ranking':'Ranking', 'L_Percentil':'Percentil', 'Size':'Qtde Atletas'})
        st.markdown("<h4 style='text-align: center;'>Segundos Atacantes </b></h4>", unsafe_allow_html=True)
        st.dataframe(tabela_13, use_container_width=True, hide_index=True)

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
if choose == "Ranking de Jogadores":
    jogadores = st.selectbox("Escolha o Jogador", options=jogadores)
    if jogadores:
        #Determinar Temporada
        df3 = df.loc[(df['Atleta']==jogadores)]
        temporadas = df3['Versão_Temporada']
        temporada = st.selectbox("Escolha a Temporada", options=temporadas)
        if temporada:
            #Determinar a Liga
            dfa = df3.loc[(df3['Versão_Temporada']==temporada)]
            ligas = dfa['Liga']
            liga = st.selectbox("Escolha a Liga", options=ligas)
            if liga:
                df4 = dfa.loc[(dfa['Versão_Temporada']==temporada)&(dfa['Liga']==liga)]
                posição = dfa['Posição']
                posição = st.selectbox("Escolha a Posição", options=posição)
                if posição == ("Goleiro"):
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # GOLEIRO CLÁSSICO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_1.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[9, 14, 26, 30:34, 28, 32, 11]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==0)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 9]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        #####################################################################################################################
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_1.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[9, 11, 15:21, 22:25, 14, 26, 28]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==0)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:11]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        #####################################################################################################################
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>GOLEIRO CLÁSSICO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                       ##################################################################################################################### 
                       #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('1_Role_Goleiro.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:25, 6, 25, 27]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==0)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2  = tabela_2.iloc[:, np.r_[0:8]]
                        tabela_2 = tabela_2.rename(columns={'Interceptações.1':'Interceptações'})
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('1_Role_Goleiro.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:25, 6, 25, 27]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==0)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:8, 9]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_b = tabela_b.rename(columns={'Interceptações.1':'Interceptações'})
                        tabela_c = (tabela_b.groupby('Liga')[['Duelos_Aéreos_Ganhos', 'Defesas', 'Gols_Evitados', 'Saídas', 'Interceptações', 'xG_Evitado', 'Finalizações_por_Gol_Sofrido']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_1.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[48:55, 9, 14, 26, 28]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==0)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:7]]
                        tabela_d = tabela_d.rename(columns={'Duelos_Aéreos_Ganhos_Percentil':'Duelos_Aéreos_Ganhos', 'Defesas_Percentil': 'Defesas', 
                                                            'Gols_Evitados_Percentil':'Gols_Evitados', 'Saídas_Percentil': 'Saídas', 
                                                            'Interceptações.1_Percentil': 'Interceptações', 'xG_Evitado_Percentil': 'xG_Evitado', 
                                                            'Finalizações_por_Gol_Sofrido_Percentil': 'Finalizações_por_Gol_Sofrido'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_1.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Determining Club and League 
                        Role_x_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[11, 26, 9]]
                        Role_x_Mean_Charts  = pd.DataFrame(Role_x_Mean_Charts)
                        Role_x_Mean_Charts = Role_x_Mean_Charts[(Role_x_Mean_Charts['Atleta']==jogadores)].reset_index()
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[9, 1:8, 11, 26, 28, 34:41]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[11:18]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        League_Mean = League_Mean.rename(columns={'Duelos_Aéreos_Ganhos_LM':'Duelos_Aéreos_Ganhos', 'Defesas_LM': 'Defesas', 
                                                                  'Gols_Evitados_LM':'Gols_Evitados', 'Saídas_LM': 'Saídas',  
                                                                  'Interceptações.1_LM': 'Interceptações.1', 'xG_Evitado_LM': 'xG_Evitado', 
                                                                  'Finalizações_por_Gol_Sofrido_LM': 'Finalizações_por_Gol_Sofrido'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:8]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        Role_1_Mean_Charts = Role_1_Mean_Charts.rename(columns={'Interceptações.1': 'Interceptações'})    
                        # Preparing the Graph
                        params = list(Role_1_Mean_Charts.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts['Atleta'])):
                            if Role_1_Mean_Charts['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts.iloc[x].values.tolist()
                            if Role_1_Mean_Charts['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # GOLEIRO LÍBERO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_2.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[12, 17, 29, 33:37, 31, 35, 14]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==0)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 9]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        #markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        #markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        #st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        #st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        #st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        #st.markdown("---")
                        #####################################################################################################################
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        #tabela_a  = pd.read_excel("PlayerAnalysis_Role_2.xlsx")
                        #tabela_a = tabela_a.iloc[:, np.r_[12, 14, 18:24, 25:28, 17, 29, 31]]
                        #tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==0)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        #tabela_a  = tabela_a.iloc[:, np.r_[0:11]]
                        #st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        #st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        #st.markdown("---")    
                        #####################################################################################################################
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>GOLEIRO LÍBERO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                       ##################################################################################################################### 
                       #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        #tabela_2 = pd.read_excel('1_Role_Goleiro.xlsx')
                        #tabela_2 = tabela_2.iloc[:, np.r_[1, 18:25, 6, 25, 27]]
                        #tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==0)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        #tabela_2  = tabela_2.iloc[:, np.r_[0:8]]
                        #tabela_2 = tabela_2.rename(columns={'Interceptações.1':'Interceptações'})
                        #tabela_2  = pd.DataFrame(tabela_2)
                        #tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        #tabela_b = pd.read_excel('1_Role_Goleiro.xlsx')
                        #tabela_b = tabela_b.iloc[:, np.r_[1, 18:25, 6, 25, 27]]
                        #tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==0)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        #tabela_b = tabela_b.iloc[:, np.r_[1:8, 9]]
                        #tabela_b = tabela_b.round(decimals=2)
                        #tabela_b = tabela_b.rename(columns={'Interceptações.1':'Interceptações'})
                        #tabela_c = (tabela_b.groupby('Liga')[['Duelos_Aéreos_Ganhos', 'Defesas', 'Gols_Evitados', 'Saídas', 'Interceptações', 'xG_Evitado', 'Finalizações_por_Gol_Sofrido']].mean())
                        #tabela_c = tabela_c.round(decimals=2)
                        #Atleta = ['Média da Liga']
                        #tabela_c['Atleta'] = Atleta 
                        #tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        #tabela_d = pd.read_excel('PlayerAnalysis_Role_1.xlsx')
                        #tabela_d = tabela_d.iloc[:, np.r_[48:55, 9, 14, 26, 28]]
                        #tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==0)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        #tabela_d = tabela_d.iloc[:, np.r_[0:7]]
                        #tabela_d = tabela_d.rename(columns={'Duelos_Aéreos_Ganhos_Percentil':'Duelos_Aéreos_Ganhos', 'Defesas_Percentil': 'Defesas', 
                        #                                    'Gols_Evitados_Percentil':'Gols_Evitados', 'Saídas_Percentil': 'Saídas', 
                        #                                    'Interceptações.1_Percentil': 'Interceptações', 'xG_Evitado_Percentil': 'xG_Evitado', 
                        #                                    'Finalizações_por_Gol_Sofrido_Percentil': 'Finalizações_por_Gol_Sofrido'})
                        #Atleta = ['Percentil na Liga']
                        #tabela_d['Atleta'] = Atleta 
                        #tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        #tabela_2 = tabela_2.append(tabela_c).reset_index()
                        #tabela_2 = tabela_2.append(tabela_d).reset_index()
                        #tabela_2 = tabela_2.transpose()
                        #tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        #st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        #st.dataframe(tabela_2, use_container_width=True)
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_2.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Determining Club and League 
                        Role_x_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[14, 29, 12]]
                        Role_x_Mean_Charts  = pd.DataFrame(Role_x_Mean_Charts)
                        Role_x_Mean_Charts = Role_x_Mean_Charts[(Role_x_Mean_Charts['Atleta']==jogadores)].reset_index()
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[12, 1:11, 14, 29, 31, 37:47]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[14:24]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        League_Mean = League_Mean.rename(columns={'Duelos_Aéreos_Ganhos_LM':'Duelos_Aéreos_Ganhos', 'Passes_Curtos_Médios_Certos_LM': 'Passes_Curtos_Médios_Certos', 
                                                                  'Passes_Longos_Certos_LM': 'Passes_Longos_Certos', 'Passes_Progressivos_Certos_LM':'Passes_Progressivos_Certos', 
                                                                  'Defesas_LM': 'Defesas', 'Gols_Evitados_LM':'Gols_Evitados', 'Saídas_LM': 'Saídas',  
                                                                  'Interceptações.1_LM': 'Interceptações.1', 'xG_Evitado_LM': 'xG_Evitado', 
                                                                  'Finalizações_por_Gol_Sofrido_LM': 'Finalizações_por_Gol_Sofrido'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:11]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        Role_1_Mean_Charts = Role_1_Mean_Charts.rename(columns={'Interceptações.1': 'Interceptações'})    
                        # Preparing the Graph
                        params = list(Role_1_Mean_Charts.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts['Atleta'])):
                            if Role_1_Mean_Charts['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts.iloc[x].values.tolist()
                            if Role_1_Mean_Charts['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                elif posição == ("Lateral"):
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # LATERAL DEFENSIVO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_3.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[8, 13, 25, 29:33, 27, 10]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==1)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_3.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[8, 10, 14:20, 21:24, 13, 25, 27]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==1)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:11]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        ##################################################################################################################### 
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>LATERAL DEFENSIVO</b></h3>", unsafe_allow_html=True)
                        st.markdown("<h6 style='text-align: center;'>(Laterais D/E são ranqueados em conjunto)</b></h6>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # LATERAL OFENSIVO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_4.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[17, 22, 34, 38:42, 36, 19]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==1)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>LATERAL OFENSIVO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # LATERAL EQUILIBRADO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_5.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[20, 25, 37, 41:45, 39, 22]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==1)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>LATERAL EQUILIBRADO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('5_Role_Lateral_Equilibrado.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:36, 6, 36, 38]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==1)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2  = tabela_2.iloc[:, np.r_[0:19]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('5_Role_Lateral_Equilibrado.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:36, 6, 36, 38]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==1)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:19, 20]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos', 
                                                              'Passes_Longos_Certos', 'Passes_Progressivos_Certos', 'Passes_Laterais_Certos', 'Ações_Ofensivas_BemSucedidas', 
                                                              'Duelos_Ofensivos_Ganhos', 'Pisadas_Área', 'Dribles_BemSucedidos', 'Corridas_Progressivas', 
                                                              'Acelerações', 'xA', 'Assistência_Finalização', 'Passes_TerçoFinal_Certos', 'Deep_Completions', 
                                                              'Deep_Completed_Crosses', 'Passes_ÁreaPênalti_Certos']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_5.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[81:99, 20, 25, 37, 39]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==1)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:18]]
                        tabela_d = tabela_d.rename(columns={'Ações_Defensivas_BemSucedidas_Percentil':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_Percentil':'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos_Percentil':'Duelos_Aéreos_Ganhos', 'Passes_Longos_Certos_Percentil':'Passes_Longos_Certos', 'Passes_Progressivos_Certos_Percentil':'Passes_Progressivos_Certos',
                                                             'Passes_Laterais_Certos_Percentil':'Passes_Laterais_Certos', 'Ações_Ofensivas_BemSucedidas_Percentil':'Ações_Ofensivas_BemSucedidas', 'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 
                                                              'Pisadas_Área_Percentil':'Pisadas_Área', 'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 'Corridas_Progressivas_Percentil':'Corridas_Progressivas', 'Acelerações_Percentil':'Acelerações', 
                                                              'xA_Percentil':'xA', 'Assistência_Finalização_Percentil':'Assistência_Finalização', 'Passes_TerçoFinal_Certos_Percentil':'Passes_TerçoFinal_Certos', 'Deep_Completions_Percentil':'Deep_Completions',
                                                                'Deep_Completed_Crosses_Percentil':'Deep_Completed_Crosses', 'Passes_ÁreaPênalti_Certos_Percentil':'Passes_ÁreaPênalti_Certos'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        #Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_5_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_5.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_5_Mean_Charts  = Role_5_Mean_Charts.iloc[:, np.r_[20, 1:19, 25, 37, 39, 45:63]]
                        Role_5_Mean_Charts  = pd.DataFrame(Role_5_Mean_Charts)
                        Role_5_Mean_Charts = Role_5_Mean_Charts[(Role_5_Mean_Charts['Atleta']==jogadores)&(Role_5_Mean_Charts['Versão_Temporada']==temporada)&(Role_5_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_5_Mean_Charts.iloc[:, np.r_[22:40]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Ações_Defensivas_BemSucedidas_LM':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_LM':'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos_LM':'Duelos_Aéreos_Ganhos', 'Passes_Longos_Certos_LM':'Passes_Longos_Certos', 'Passes_Progressivos_Certos_LM':'Passes_Progressivos_Certos',
                                                             'Passes_Laterais_Certos_LM':'Passes_Laterais_Certos', 'Ações_Ofensivas_BemSucedidas_LM':'Ações_Ofensivas_BemSucedidas', 'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 
                                                              'Pisadas_Área_LM':'Pisadas_Área', 'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 'Corridas_Progressivas_LM':'Corridas_Progressivas', 'Acelerações_LM':'Acelerações', 
                                                              'xA_LM':'xA', 'Assistência_Finalização_LM':'Assistência_Finalização', 'Passes_TerçoFinal_Certos_LM':'Passes_TerçoFinal_Certos', 'Deep_Completions_LM':'Deep_Completions',
                                                                'Deep_Completed_Crosses_LM':'Deep_Completed_Crosses', 'Passes_ÁreaPênalti_Certos_LM':'Passes_ÁreaPênalti_Certos'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_5_Mean_Charts  = Role_5_Mean_Charts.iloc[:, np.r_[0:19]]
                        #Concatenating Dataframes
                        Role_5_Mean_Charts = Role_5_Mean_Charts.append(League_Mean).reset_index()
                        #Splitting Columns
                        Role_5_Mean_Charts_1 = Role_5_Mean_Charts.iloc[:, np.r_[1, 2:11]]
                        Role_5_Mean_Charts_2 = Role_5_Mean_Charts.iloc[:, np.r_[1, 11:20]]

                        # Preparing Graph 1
                        # Get Parameters

                        params = list(Role_5_Mean_Charts_1.columns)
                        params = params[1:]
                        
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_5_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_5_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_5_Mean_Charts_1['Atleta'])):
                            if Role_5_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_5_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_5_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_5_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################

                        # Preparing Graph 2
                        # Get Parameters

                        params = list(Role_5_Mean_Charts_2.columns)
                        params = params[1:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_5_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_5_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_5_Mean_Charts_2['Atleta'])):
                            if Role_5_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_5_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_5_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_5_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                elif posição == ("Zagueiro"):
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # ZAGUEIRO CLÁSSICO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_6.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[8, 13, 25, 29:33, 27, 10]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==4)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_6.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[8, 10, 14:20, 21:24, 13, 25, 27]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==4)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:11]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        ##################################################################################################################### 
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>ZAGUEIRO CLÁSSICO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # ZAGUEIRO CONSTRUTOR
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_7.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[12, 17, 29, 33:37, 31, 14]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==4)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>ZAGUEIRO CONSTRUTOR</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # ZAGUEIRO EQUILIBRADO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_8.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[15, 20, 32, 36:40, 34, 17]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==4)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>ZAGUEIRO EQUILIBRADO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('8_Role_Zagueiro_Equilibrado.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==4)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2  = tabela_2.iloc[:, np.r_[0:14]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('8_Role_Zagueiro_Equilibrado.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==4)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        #st.dataframe(tabela_b)
                        tabela_b = tabela_b.iloc[:, np.r_[1:14, 15]]
                        #st.dataframe(tabela_b)
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos', 
                                                              'Finalizações_Bloqueadas', 'Interceptações_Ajustadas_a_Posse', 'Passes_Longos_Certos', 
                                                              'Passes_Frontais_Certos', 'Passes_Progressivos_Certos', 'Passes_Laterais_Certos', 'Duelos_Ofensivos_Ganhos', 
                                                              'Dribles_BemSucedidos', 'Corridas_Progressivas', 'Passes_TerçoFinal_Certos']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_8.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[66:79, 15, 20, 32, 34]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==4)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:13]]
                        tabela_d = tabela_d.rename(columns={'Ações_Defensivas_BemSucedidas_Percentil':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_Percentil':'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos_Percentil':'Duelos_Aéreos_Ganhos',
                                                            'Finalizações_Bloqueadas_Percentil':'Finalizações_Bloqueadas', 'Interceptações_Ajustadas_a_Posse_Percentil':'Interceptações_Ajustadas_a_Posse', 'Passes_Longos_Certos_Percentil':'Passes_Longos_Certos', 
                                                            'Passes_Frontais_Certos_Percentil':'Passes_Frontais_Certos', 'Passes_Progressivos_Certos_Percentil':'Passes_Progressivos_Certos', 'Passes_Laterais_Certos_Percentil':'Passes_Laterais_Certos', 'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 
                                                            'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 'Corridas_Progressivas_Percentil':'Corridas_Progressivas', 'Passes_TerçoFinal_Certos_Percentil':'Passes_TerçoFinal_Certos'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_5_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_8.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_5_Mean_Charts  = Role_5_Mean_Charts.iloc[:, np.r_[15, 1:14, 20, 32, 34, 40:53]]
                        Role_5_Mean_Charts  = pd.DataFrame(Role_5_Mean_Charts)
                        Role_5_Mean_Charts = Role_5_Mean_Charts[(Role_5_Mean_Charts['Atleta']==jogadores)&(Role_5_Mean_Charts['Versão_Temporada']==temporada)&(Role_5_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_5_Mean_Charts.iloc[:, np.r_[17:30]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Ações_Defensivas_BemSucedidas_LM':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_LM':'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos_LM':'Duelos_Aéreos_Ganhos',
                                                            'Finalizações_Bloqueadas_LM':'Finalizações_Bloqueadas', 'Interceptações_Ajustadas_a_Posse_LM':'Interceptações_Ajustadas_a_Posse', 'Passes_Longos_Certos_LM':'Passes_Longos_Certos', 
                                                            'Passes_Frontais_Certos_LM':'Passes_Frontais_Certos', 'Passes_Progressivos_Certos_LM':'Passes_Progressivos_Certos', 'Passes_Laterais_Certos_LM':'Passes_Laterais_Certos', 'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 
                                                            'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 'Corridas_Progressivas_LM':'Corridas_Progressivas', 'Passes_TerçoFinal_Certos_LM':'Passes_TerçoFinal_Certos'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_5_Mean_Charts  = Role_5_Mean_Charts.iloc[:, np.r_[0:14]]
                        #Concatenating Dataframes
                        Role_5_Mean_Charts = Role_5_Mean_Charts.append(League_Mean).reset_index()
                        #Splitting Columns
                        Role_5_Mean_Charts_1 = Role_5_Mean_Charts.iloc[:, np.r_[1, 2:9]]
                        Role_5_Mean_Charts_2 = Role_5_Mean_Charts.iloc[:, np.r_[1, 9:13]]
                        
                        # Preparing Graph 1
                        # Get Parameters

                        params = list(Role_5_Mean_Charts_1.columns)
                        params = params[1:]
                        #st.write(params)
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_5_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_5_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_5_Mean_Charts_1['Atleta'])):
                            if Role_5_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_5_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_5_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_5_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################

                        # Preparing Graph 2
                        # Get Parameters

                        params = list(Role_5_Mean_Charts_2.columns)
                        params = params[1:]
    #                    params
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_5_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_5_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_5_Mean_Charts_2['Atleta'])):
                            if Role_5_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_5_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_5_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_5_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                elif posição == ("Primeiro Volante"):
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # PRIMEIRO VOLANTE DEFENSIVO
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_9.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[6, 11, 23, 27:31, 25, 8]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==7)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_9.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[6, 8, 12:18, 19:22, 11, 23, 25]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==7)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:11]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        ##################################################################################################################### 
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>PRIMEIRO VOLANTE DEFENSIVO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        #####################################################################################################################
                        #####################################################################################################################
                        # PRIMEIRO VOLANTE CONSTRUTOR
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_10.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[11, 16, 28, 32:36, 30, 13]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==7)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>PRIMEIRO VOLANTE CONSTRUTOR</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # PRIMEIRO VOLANTE EQUILIBRADO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_11.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[13, 18, 30, 34:38, 32, 15]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==7)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>PRIMEIRO VOLANTE EQUILIBRADO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('11_Role_Volante_Equilibrado.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:29, 6, 29, 31]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==7)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2  = tabela_2.iloc[:, np.r_[0:12]]
                        #tabela_2 = tabela_2.rename(columns={'Interceptações.1':'Interceptações'})
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('11_Role_Volante_Equilibrado.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:29, 6, 29, 31]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==7)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:12, 13]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos', 
                                                              'Passes_Longos_Certos', 'Passes_Frontais_Certos', 'Passes_Progressivos_Certos', 
                                                              'Ações_Ofensivas_BemSucedidas', 'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos', 
                                                              'Corridas_Progressivas', 'Passes_TerçoFinal_Certos']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_11.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[60:71, 13, 18, 30, 32]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==7)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:12]]
                        tabela_d = tabela_d.rename(columns={'Ações_Defensivas_BemSucedidas_Percentil':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_Percentil':'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos_Percentil':'Duelos_Aéreos_Ganhos',
                                                            'Passes_Longos_Certos_Percentil':'Passes_Longos_Certos', 'Passes_Frontais_Certos_Percentil':'Passes_Frontais_Certos', 'Passes_Progressivos_Certos_Percentil':'Passes_Progressivos_Certos',
                                                            'Ações_Ofensivas_BemSucedidas_Percentil':'Ações_Ofensivas_BemSucedidas', 'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos',
                                                            'Corridas_Progressivas_Percentil':'Corridas_Progressivas', 'Passes_TerçoFinal_Certos_Percentil':'Passes_TerçoFinal_Certos'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_5_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_11.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_5_Mean_Charts  = Role_5_Mean_Charts.iloc[:, np.r_[13, 1:12, 18, 30, 32, 38:49]]
                        Role_5_Mean_Charts  = pd.DataFrame(Role_5_Mean_Charts)
                        Role_5_Mean_Charts = Role_5_Mean_Charts[(Role_5_Mean_Charts['Atleta']==jogadores)&(Role_5_Mean_Charts['Versão_Temporada']==temporada)&(Role_5_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_5_Mean_Charts.iloc[:, np.r_[15:26]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Ações_Defensivas_BemSucedidas_LM':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_LM':'Duelos_Defensivos_Ganhos', 'Duelos_Aéreos_Ganhos_LM':'Duelos_Aéreos_Ganhos',
                                                            'Passes_Longos_Certos_LM':'Passes_Longos_Certos', 'Passes_Frontais_Certos_LM':'Passes_Frontais_Certos', 'Passes_Progressivos_Certos_LM':'Passes_Progressivos_Certos',
                                                            'Ações_Ofensivas_BemSucedidas_LM':'Ações_Ofensivas_BemSucedidas', 'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos',
                                                            'Corridas_Progressivas_LM':'Corridas_Progressivas', 'Passes_TerçoFinal_Certos_LM':'Passes_TerçoFinal_Certos'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_5_Mean_Charts  = Role_5_Mean_Charts.iloc[:, np.r_[0:12]]
                        #Concatenating Dataframes
                        Role_5_Mean_Charts = Role_5_Mean_Charts.append(League_Mean).reset_index()
                        #Splitting Columns
                        Role_5_Mean_Charts_1 = Role_5_Mean_Charts.iloc[:, np.r_[1, 2:8]]
                        Role_5_Mean_Charts_2 = Role_5_Mean_Charts.iloc[:, np.r_[1, 8:13]]
                        
                        # Preparing Graph 1
                        # Get Parameters

                        params = list(Role_5_Mean_Charts_1.columns)
                        params = params[1:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_5_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_5_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_5_Mean_Charts_1['Atleta'])):
                            if Role_5_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_5_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_5_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_5_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################

                        # Preparing Graph 2
                        # Get Parameters

                        params = list(Role_5_Mean_Charts_2.columns)
                        params = params[1:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_5_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_5_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_5_Mean_Charts_2['Atleta'])):
                            if Role_5_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_5_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_5_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_5_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                elif posição == ("Segundo Volante"):
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # SEGUNDO VOLANTE BOX TO BOX
                       # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_12.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[15, 20, 32, 36:40, 34, 17]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==8)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        #####################################################################################################################
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_12.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[15, 17, 21:27, 28:31, 20, 32, 34]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==8)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:11]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        #####################################################################################################################
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>SEGUNDO VOLANTE BOX TO BOX</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # SEGUNDO VOLANTE ORGANIZADOR
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_13.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[12, 17, 29, 33:37, 31, 14]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==8)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>SEGUNDO VOLANTE ORGANIZADOR</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # SEGUNDO VOLANTE EQUILIBRADO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_14.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[15, 20, 32, 36:40, 34, 17]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==8)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>SEGUNDO VOLANTE EQUILIBRADO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('14_Role_Segundo_Volante_Equilibrado.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==8)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2  = tabela_2.iloc[:, np.r_[0:14]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('14_Role_Segundo_Volante_Equilibrado.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==8)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:14, 15]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos', 'Passes_Longos_Certos', 'Passes_Progressivos_Certos', 'Pisadas_Área',
                                                              'Dribles_BemSucedidos', 'Corridas_Progressivas', 'xG', 'xA', 'Assistência_Finalização', 'Passes_TerçoFinal_Certos',
                                                               'Deep_Completions', 'Passes_ÁreaPênalti_Certos']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_14.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[66:79, 15, 20, 32, 34]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==8)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:13]]
                        tabela_d = tabela_d.rename(columns={'Ações_Defensivas_BemSucedidas_Percentil':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_Percentil':'Duelos_Defensivos_Ganhos', 
                                                            'Passes_Longos_Certos_Percentil':'Passes_Longos_Certos', 'Passes_Progressivos_Certos_Percentil':'Passes_Progressivos_Certos',
                                                            'Pisadas_Área_Percentil':'Pisadas_Área', 'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 
                                                            'Corridas_Progressivas_Percentil':'Corridas_Progressivas', 'xG_Percentil':'xG', 'xA_Percentil':'xA', 
                                                            'Assistência_Finalização_Percentil':'Assistência_Finalização', 'Passes_TerçoFinal_Certos_Percentil':'Passes_TerçoFinal_Certos',
                                                            'Deep_Completions_Percentil':'Deep_Completions', 'Passes_ÁreaPênalti_Certos_Percentil':'Passes_ÁreaPênalti_Certos'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_14.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[15, 1:14, 20, 32, 34, 40:53]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[17:30]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Ações_Defensivas_BemSucedidas_LM':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_LM':'Duelos_Defensivos_Ganhos', 
                                                            'Passes_Longos_Certos_LM':'Passes_Longos_Certos', 'Passes_Progressivos_Certos_LM':'Passes_Progressivos_Certos',
                                                            'Pisadas_Área_LM':'Pisadas_Área', 'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 
                                                            'Corridas_Progressivas_LM':'Corridas_Progressivas', 'xG_LM':'xG', 'xA_LM':'xA', 
                                                            'Assistência_Finalização_LM':'Assistência_Finalização', 'Passes_TerçoFinal_Certos_LM':'Passes_TerçoFinal_Certos',
                                                            'Deep_Completions_LM':'Deep_Completions', 'Passes_ÁreaPênalti_Certos_LM':'Passes_ÁreaPênalti_Certos'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[0:14]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        #Splitting Columns
                        Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[1, 2:8]]
                        Role_1_Mean_Charts_2 = Role_1_Mean_Charts.iloc[:, np.r_[1, 8:15]]
                        
                        # Preparing Graph 1
                        # Get Parameters
                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[1:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################

                        # Preparing Graph 2
                        # Get Parameters
                        params = list(Role_1_Mean_Charts_2.columns)
                        params = params[1:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_2['Atleta'])):
                            if Role_1_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison_1.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison_1.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                elif posição == ("Meia"):
                        #####################################################################################################################
                        #####################################################################################################################
                        # MEIA ORGANIZADOR
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_15.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[12, 17, 29, 33:37, 31, 14]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==9)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        #####################################################################################################################
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_15.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[12, 14, 19:24, 25:28, 17, 29, 31]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==9)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:10]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        #####################################################################################################################
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>MEIA ORGANIZADOR</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('15_Role_Meia_Organizador.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:28, 6, 28, 30]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==9)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2  = tabela_2.iloc[:, np.r_[0:11]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('15_Role_Meia_Organizador.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:28, 6, 28, 30]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==9)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[0:11, 12]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Passes_Longos_Certos', 'Passes_Frontais_Certos', 'Passes_Progressivos_Certos',
                                                              'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos', 'xA', 'Assistência_Finalização',
                                                              'Passes_TerçoFinal_Certos', 'Passes_EntreLinhas_Certos', 'Passes_Chave',]].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_15.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[57:67, 12, 17, 29, 31]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==9)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:10]]
                        tabela_d = tabela_d.rename(columns={'Passes_Longos_Certos_Percentil':'Passes_Longos_Certos', 'Passes_Frontais_Certos_Percentil':'Passes_Frontais_Certos',
                                                            'Passes_Progressivos_Certos_Percentil': 'Passes_Progressivos_Certos', 'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 
                                                            'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 'xA_Percentil':'xA', 'Assistência_Finalização_Percentil':'Assistência_Finalização',
                                                            'Passes_TerçoFinal_Certos_Percentil':'Passes_TerçoFinal_Certos', 'Passes_EntreLinhas_Certos_Percentil':'Passes_EntreLinhas_Certos',
                                                            'Passes_Chave_Percentil':'Passes_Chave'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_15.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[12, 1:11, 17, 29, 31, 37:47]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[14:24]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Passes_Longos_Certos_LM':'Passes_Longos_Certos', 'Passes_Frontais_Certos_LM':'Passes_Frontais_Certos',
                                                            'Passes_Progressivos_Certos_LM': 'Passes_Progressivos_Certos', 'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 
                                                            'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 'xA_LM':'xA', 'Assistência_Finalização_LM':'Assistência_Finalização',
                                                            'Passes_TerçoFinal_Certos_LM':'Passes_TerçoFinal_Certos', 'Passes_EntreLinhas_Certos_LM':'Passes_EntreLinhas_Certos',
                                                            'Passes_Chave_LM':'Passes_Chave'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:12]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        # Preparing the Graph
                        #Not Splitting Columns
                        Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[0:12]]
                        # Plotting graph 1
                        # Get Parameters
                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # MEIA ATACANTE
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_16.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[19, 24, 36, 40:44, 38, 21]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==9)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>MEIA ATACANTE</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('16_Role_Meia_Atacante.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:35, 6, 35, 37]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==9)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2 = tabela_2.iloc[:, np.r_[0:18]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('16_Role_Meia_Atacante.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:35, 6, 35, 37]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==9)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[0:18, 19]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Passes_Longos_Certos', 'Passes_Frontais_Certos', 'Passes_Progressivos_Certos',
                                                              'Duelos_Ofensivos_Ganhos', 'Pisadas_Área', 'Dribles_BemSucedidos', 'xG', 'Finalizações_NoAlvo',
                                                                'Ameaça_Ofensiva', 'xA', 'Assistência_Finalização', 'Passes_TerçoFinal_Certos', 
                                                                'Passes_Inteligentes_Certos', 'Passes_EntreLinhas_Certos', 'Deep_Completions', 'Passes_Chave',
                                                                'Passes_ÁreaPênalti_Certos']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_16.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[78:95, 19, 24, 36, 38]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==9)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:17]]
                        tabela_d = tabela_d.rename(columns={'Passes_Longos_Certos_Percentil':'Passes_Longos_Certos', 'Passes_Frontais_Certos_Percentil':'Passes_Frontais_Certos',
                                                            'Passes_Progressivos_Certos_Percentil': 'Passes_Progressivos_Certos', 'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 
                                                            'Pisadas_Área_Percentil':'Pisadas_Área', 'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 'xG_Percentil':'xG', 
                                                            'Finalizações_NoAlvo_Percentil':'Finalizações_NoAlvo', 'Ameaça_Ofensiva_Percentil':'Ameaça_Ofensiva', 'xA_Percentil':'xA',
                                                            'Assistência_Finalização_Percentil':'Assistência_Finalização', 'Passes_TerçoFinal_Certos_Percentil':'Passes_TerçoFinal_Certos', 
                                                            'Passes_Inteligentes_Certos_Percentil':'Passes_Inteligentes_Certos', 'Passes_EntreLinhas_Certos_Percentil':'Passes_EntreLinhas_Certos',
                                                            'Deep_Completions_Percentil':'Deep_Completions', 'Passes_Chave_Percentil':'Passes_Chave', 'Passes_ÁreaPênalti_Certos_Percentil':'Passes_ÁreaPênalti_Certos'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_16.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[19, 1:18, 24, 36, 38, 44:61]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[21:38]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        League_Mean = League_Mean.rename(columns={'Passes_Longos_Certos_LM':'Passes_Longos_Certos', 'Passes_Frontais_Certos_LM':'Passes_Frontais_Certos',
                                                            'Passes_Progressivos_Certos_LM': 'Passes_Progressivos_Certos', 'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 
                                                            'Pisadas_Área_LM':'Pisadas_Área', 'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 'xG_LM':'xG', 
                                                            'Finalizações_NoAlvo_LM':'Finalizações_NoAlvo', 'Ameaça_Ofensiva_LM':'Ameaça_Ofensiva', 'xA_LM':'xA',
                                                            'Assistência_Finalização_LM':'Assistência_Finalização', 'Passes_TerçoFinal_Certos_LM':'Passes_TerçoFinal_Certos', 
                                                            'Passes_Inteligentes_Certos_LM':'Passes_Inteligentes_Certos', 'Passes_EntreLinhas_Certos_LM':'Passes_EntreLinhas_Certos',
                                                            'Deep_Completions_LM':'Deep_Completions', 'Passes_Chave_LM':'Passes_Chave', 'Passes_ÁreaPênalti_Certos_DM':'Passes_ÁreaPênalti_Certos'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:18]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        # Preparing the Graph
                        #Splitting Columns
                        Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[0:10]]
                        Role_1_Mean_Charts_2 = Role_1_Mean_Charts.iloc[:, np.r_[1, 10:18]]

                        # Plotting graph 1
                        # Get Parameters
                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        ##################################################################################################################### 
                        #####################################################################################################################

                        # Plotting graph 2
                        # Get Parameters
                        params = list(Role_1_Mean_Charts_2.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_2['Atleta'])):
                            if Role_1_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                elif posição == ("Extremo"):
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # EXTREMO ORGANIZADOR
                        # Texto de Abertura
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_17.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[15, 20, 32, 36:40, 34, 17]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&((tabela_1['Código_Posição_Wyscout']==10)|(tabela_1['Código_Posição_Wyscout']==11))&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        ##################################################################################################################### 
                        #####################################################################################################################
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_17.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[15, 17, 21:27, 28:31, 20, 32, 34]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&((tabela_a['Código_Posição_Wyscout']==10)|(tabela_a['Código_Posição_Wyscout']==11))&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:10]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>EXTREMO ORGANIZADOR</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('17_Role_Extremo_Organizador.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&((tabela_2['Código_Posição_Wyscout']==10)|(tabela_2['Código_Posição_Wyscout']==11))&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2 = tabela_2.iloc[:, np.r_[0:14]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('17_Role_Extremo_Organizador.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_b = tabela_b[((tabela_b['Código_Posição_Wyscout']==10)|(tabela_b['Código_Posição_Wyscout']==11))&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:14, 15]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Passes_Longos_Certos', 'Passes_Frontais_Certos', 'Passes_Progressivos_Certos',
                                                              'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos', 'xG', 'Finalizações_NoAlvo',
                                                                'Conversão_Gols', 'xA', 'Assistência_Finalização', 'Passes_Inteligentes_Certos', 
                                                                'Passes_EntreLinhas_Certos', 'Passes_Chave']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_17.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[66:79, 15, 20, 32, 34]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&((tabela_d['Código_Posição_Wyscout']==10)|(tabela_d['Código_Posição_Wyscout']==11))&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:14]]
                        tabela_d = tabela_d.rename(columns={'Passes_Longos_Certos_Percentil':'Passes_Longos_Certos', 'Passes_Frontais_Certos_Percentil':'Passes_Frontais_Certos',
                                                            'Passes_Progressivos_Certos_Percentil': 'Passes_Progressivos_Certos', 'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 
                                                            'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 'xG_Percentil':'xG', 'Finalizações_NoAlvo_Percentil':'Finalizações_NoAlvo', 
                                                            'Conversão_Gols_Percentil':'Conversão_Gols', 'xA_Percentil':'xA', 'Assistência_Finalização_Percentil':'Assistência_Finalização', 
                                                            'Passes_Inteligentes_Certos_Percentil':'Passes_Inteligentes_Certos', 'Passes_EntreLinhas_Certos_Percentil':'Passes_EntreLinhas_Certos',
                                                            'Passes_Chave_Percentil':'Passes_Chave'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_17.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[15, 1:14, 20, 32, 34, 40:53]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[16:30]]
    #                    Atleta = ['Média da Liga']
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Passes_Longos_Certos_LM':'Passes_Longos_Certos', 'Passes_Frontais_Certos_LM':'Passes_Frontais_Certos',
                                                            'Passes_Progressivos_Certos_LM': 'Passes_Progressivos_Certos', 'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 
                                                            'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 'xG_LM':'xG', 'Finalizações_NoAlvo_LM':'Finalizações_NoAlvo', 
                                                            'Conversão_Gols_LM':'Conversão_Gols', 'xA_LM':'xA', 'Assistência_Finalização_LM':'Assistência_Finalização', 
                                                            'Passes_Inteligentes_Certos_LM':'Passes_Inteligentes_Certos', 'Passes_EntreLinhas_Certos_LM':'Passes_EntreLinhas_Certos',
                                                            'Passes_Chave_DM':'Passes_Chave'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:14]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        # Preparing the Graph
                        #Splitting Columns
                        Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[0:8]]
                        Role_1_Mean_Charts_2 = Role_1_Mean_Charts.iloc[:, np.r_[1, 8:14]]

                        # Plotting graph 1
                        # Get Parameters
                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        ##################################################################################################################### 
                        #####################################################################################################################

                        # Plotting graph 2
                        # Get Parameters

                        params = list(Role_1_Mean_Charts_2.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_2['Atleta'])):
                            if Role_1_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        ##################################################################################################################### 
                        #####################################################################################################################
                        # EXTREMO TÁTICO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_18.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[9, 14, 26, 30:34, 28, 11]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&((tabela_1['Código_Posição_Wyscout']==10)|(tabela_1['Código_Posição_Wyscout']==11))&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>EXTREMO TÁTICO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('18_Role_Extremo_Tático.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:25, 6, 25, 27]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&((tabela_2['Código_Posição_Wyscout']==10)|(tabela_2['Código_Posição_Wyscout']==11))&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2 = tabela_2.iloc[:, np.r_[0:8]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('18_Role_Extremo_Tático.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:25, 6, 25, 27]]
                        tabela_b = tabela_b[((tabela_b['Código_Posição_Wyscout']==10)|(tabela_b['Código_Posição_Wyscout']==11))&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:8, 9]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos', 'Passes_Frontais_Certos',
                                                              'Passes_Progressivos_Certos', 'Duelos_Ofensivos_Ganhos', 'xG', 'xA']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_18.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[48:55, 9, 14, 26, 28]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&((tabela_d['Código_Posição_Wyscout']==10)|(tabela_d['Código_Posição_Wyscout']==11))&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:7]]
                        tabela_d = tabela_d.rename(columns={'Ações_Defensivas_BemSucedidas_Percentil':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_Percentil':'Duelos_Defensivos_Ganhos', 
                                                            'Passes_Frontais_Certos_Percentil':'Passes_Frontais_Certos', 'Passes_Progressivos_Certos_Percentil': 'Passes_Progressivos_Certos', 
                                                            'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 'xG_Percentil':'xG', 'xA_Percentil':'xA'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_18.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[9, 1:8, 14, 26, 28, 34:41]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #liga = Role_1_Mean_Charts["Liga"]
                        #clube = Role_1_Mean_Charts["Equipe_Janela_Análise"]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[11:18]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Ações_Defensivas_BemSucedidas_LM':'Ações_Defensivas_BemSucedidas', 'Duelos_Defensivos_Ganhos_LM':'Duelos_Defensivos_Ganhos', 
                                                            'Passes_Frontais_Certos_LM':'Passes_Frontais_Certos', 'Passes_Progressivos_Certos_LM': 'Passes_Progressivos_Certos', 
                                                            'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 'xG_LM':'xG', 'xA_LM':'xA'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:9]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        # Preparing the Graph
                        #Not Splitting Columns
                        Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[0:9]]

                        # Plotting graph 1
                        # Get Parameters

                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        # EXTREMO AGUDO
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_19.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[15, 20, 32, 36:40, 34, 17]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&((tabela_1['Código_Posição_Wyscout']==10)|(tabela_1['Código_Posição_Wyscout']==11))&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>EXTREMO AGUDO</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('19_Role_Extremo_Agudo.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&((tabela_2['Código_Posição_Wyscout']==10)|(tabela_2['Código_Posição_Wyscout']==11))&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2 = tabela_2.iloc[:, np.r_[0:14]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('19_Role_Extremo_Agudo.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_b = tabela_b[((tabela_b['Código_Posição_Wyscout']==10)|(tabela_b['Código_Posição_Wyscout']==11))&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[0:14, 15]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Duelos_Ofensivos_Ganhos', 'Pisadas_Área', 'Dribles_BemSucedidos', 'Acelerações', 
                                                              'Passes_Longos_Recebidos', 'xG', 'Finalizações_NoAlvo', 'Conversão_Gols', 'xA', 
                                                              'Assistência_Finalização', 'Deep_Completions', 'Deep_Completed_Crosses', 'Passes_Chave']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_19.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[66:79, 15, 20, 32, 34]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&((tabela_d['Código_Posição_Wyscout']==10)|(tabela_d['Código_Posição_Wyscout']==11))&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:13]]
                        tabela_d = tabela_d.rename(columns={'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 'Pisadas_Área_Percentil':'Pisadas_Área', 
                                                            'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 'Acelerações_Percentil':'Acelerações', 
                                                            'Passes_Longos_Recebidos_Percentil':'Passes_Longos_Recebidos', 'xG_Percentil':'xG', 'Finalizações_NoAlvo_Percentil':'Finalizações_NoAlvo', 
                                                            'Conversão_Gols_Percentil':'Conversão_Gols', 'xA_Percentil':'xA', 'Assistência_Finalização_Percentil':'Assistência_Finalização', 
                                                            'Deep_Completions_Percentil':'Deep_Completions', 'Deep_Completed_Crosses_Percentil':'Deep_Completed_Crosses', 
                                                            'Passes_Chave_Percentil':'Passes_Chave'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        #####################################################################################################################
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_19.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[15, 1:14, 20, 32, 34, 40:53]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[17:30]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 'Pisadas_Área_LM':'Pisadas_Área', 
                                                            'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 'Acelerações_LM':'Acelerações', 
                                                            'Passes_Longos_Recebidos_LM':'Passes_Longos_Recebidos', 'xG_LM':'xG', 'Finalizações_NoAlvo_LM':'Finalizações_NoAlvo', 
                                                            'Conversão_Gols_LM':'Conversão_Gols', 'xA_LM':'xA', 'Assistência_Finalização_LM':'Assistência_Finalização', 
                                                            'Deep_Completions_LM':'Deep_Completions', 'Deep_Completed_Crosses_LM':'Deep_Completed_Crosses', 
                                                            'Passes_Chave_LM':'Passes_Chave'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:14]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        # Preparing the Graph
                        #Splitting Columns
                        Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[0:10]]
                        Role_1_Mean_Charts_2 = Role_1_Mean_Charts.iloc[:, np.r_[1, 10:15]]

                        # Plotting graph 1
                        # Get Parameters

                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################

                        # Plotting graph 2
                        # Get Parameters

                        params = list(Role_1_Mean_Charts_2.columns)
                        params = params[1:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_2['Atleta'])):
                            if Role_1_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
                elif posição == ("Atacante"):
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # ATACANTE REFERÊNCIA
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_20.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[12, 17, 29, 33:37, 31, 14]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==12)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Texto de Abertura
                        markdown_amount_1 = f"<div style='text-align:center; font-size:{fontsize}px'>{jogadores:}</div>"
                        markdown_amount_2 = f"<div style='text-align:center; font-size:{fontsize}px'>{clube:}</div>"
                        st.markdown("<h4 style='text-align: center;'>Jogador Selecionado</b></h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_1, unsafe_allow_html=True)
                        st.markdown(markdown_amount_2, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # Dados Básicos do Jogador
                        tabela_a  = pd.read_excel("PlayerAnalysis_Role_20.xlsx")
                        tabela_a = tabela_a.iloc[:, np.r_[12, 14, 19:24, 25:28, 17, 29, 31]]
                        tabela_a = tabela_a[(tabela_a['Atleta']==jogadores)&(tabela_a['Código_Posição_Wyscout']==12)&(tabela_a['Versão_Temporada']==temporada)&(tabela_a['Liga']==liga)]
                        tabela_a  = tabela_a.iloc[:, np.r_[0:10]]
                        st.markdown("<h4 style='text-align: center;'>Dados Básicos</b></h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_a, use_container_width=True, hide_index=True)
                        st.markdown("---")    
                        #####################################################################################################################
                        #####################################################################################################################
                        st.markdown("<h3 style='text-align: center;'>ATACANTE REFERÊNCIA</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_20.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[12, 1:11, 17, 29, 31, 37:47]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[14:24]]
                        #Atleta = ['Média da Liga']
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Duelos_Aéreos_Ganhos_LM':'Duelos_Aéreos_Ganhos', 'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 'xG_LM':'xG', 
                                                            'Conversão_Gols_LM':'Conversão_Gols', 'Conversão_xG_LM':'Conversão_xG', 
                                                            'Ameaça_Ofensiva_LM':'Ameaça_Ofensiva', 'xA_LM':'xA',  
                                                            'Deep_Completions_LM':'Deep_Completions', 'Passes_Chave_LM':'Passes_Chave', 
                                                            'Passes_ÁreaPênalti_Certos_LM':'Passes_ÁreaPênalti_Certos'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:11]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        # Preparing the Graph
                        #Splitting Columns
                        #Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[0:10]]
                        #Role_1_Mean_Charts_2 = Role_1_Mean_Charts.iloc[:, np.r_[1, 9:15]]

                        #####################################################################################################################
                        #####################################################################################################################

                        # Plotting graph 1
                        # Get Parameters

                        params = list(Role_1_Mean_Charts.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts['Atleta'])):
                            if Role_1_Mean_Charts['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts.iloc[x].values.tolist()
                            if Role_1_Mean_Charts['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        ##################################################################################################################### 
                        #####################################################################################################################
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # SEGUNDO ATACANTE
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_22.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[15, 20, 32, 36:40, 34, 17]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==12)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>SEGUNDO ATACANTE</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('22_Role_Segundo_Atacante.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==12)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2 = tabela_2.iloc[:, np.r_[0:13]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('22_Role_Segundo_Atacante.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:31, 6, 31, 33]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==12)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:14, 15]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos', 'Acelerações', 'xG', 
                                                              'Finalizações_NoAlvo', 'Conversão_Gols', 'Conversão_xG', 'Ameaça_Ofensiva', 'xA', 
                                                              'Assistência_Finalização', 'Deep_Completions', 'Passes_Chave', 'Passes_ÁreaPênalti_Certos']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_22.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[66:79, 15, 20, 32, 34]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==12)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:13]]
                        tabela_d = tabela_d.rename(columns={'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 
                                                            'Acelerações_Percentil':'Acelerações', 'xG_Percentil':'xG', 'Finalizações_NoAlvo_Percentil':'Finalizações_NoAlvo', 
                                                            'Conversão_Gols_Percentil':'Conversão_Gols', 'Conversão_xG_Percentil':'Conversão_xG', 
                                                            'Ameaça_Ofensiva_Percentil':'Ameaça_Ofensiva', 'xA_Percentil':'xA', 'Assistência_Finalização_Percentil':'Assistência_Finalização', 
                                                            'Deep_Completions_Percentil':'Deep_Completions', 'Passes_Chave_Percentil':'Passes_Chave', 
                                                            'Passes_ÁreaPênalti_Certos_Percentil':'Passes_ÁreaPênalti_Certos'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_22.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[15, 1:14, 20, 32, 34, 40:53]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[17:30]]
    #                    Atleta = ['Média da Liga']
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 
                                                            'Acelerações_LM':'Acelerações', 'xG_LM':'xG', 'Finalizações_NoAlvo_LM':'Finalizações_NoAlvo', 
                                                            'Conversão_Gols_LM':'Conversão_Gols', 'Conversão_xG_LM':'Conversão_xG', 
                                                            'Ameaça_Ofensiva_LM':'Ameaça_Ofensiva', 'xA_LM':'xA', 'Assistência_Finalização_LM':'Assistência_Finalização', 
                                                            'Deep_Completions_LM':'Deep_Completions', 'Passes_Chave_LM':'Passes_Chave', 
                                                            'Passes_ÁreaPênalti_Certos_LM':'Passes_ÁreaPênalti_Certos'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:14]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()
                        # Preparing the Graph
                        #Splitting Columns
                        Role_1_Mean_Charts_1 = Role_1_Mean_Charts.iloc[:, np.r_[0:10]]
                        Role_1_Mean_Charts_2 = Role_1_Mean_Charts.iloc[:, np.r_[1, 9:15]]

                        #####################################################################################################################
                        #####################################################################################################################

                        # Plotting graph 1
                        # Get Parameters

                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################

                        # Plotting graph 2
                        # Get Parameters

                        params = list(Role_1_Mean_Charts_2.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_2[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_2[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_2['Atleta'])):
                            if Role_1_Mean_Charts_2['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_2['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_2.iloc[x].values.tolist()
                                    
                        a_values = a_values[1:]
                        b_values = b_values[1:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        ##################################################################################################################### 
                        #####################################################################################################################

                        # ATACANTE MÓVEL
                        # Elaborar Tabela de Abertura com Rating, Ranking, Percentil
                        tabela_1 = pd.read_excel('PlayerAnalysis_Role_21.xlsx')
                        tabela_1  = tabela_1.iloc[:, np.r_[11, 16, 28, 32:36, 30, 13]]
                        tabela_1 = tabela_1[(tabela_1['Atleta']==jogadores)&(tabela_1['Código_Posição_Wyscout']==12)&(tabela_1['Versão_Temporada']==temporada)&(tabela_1['Liga']==liga)]
                        clube = tabela_1.iat[0, 8]
                        rating = tabela_1.iat[0, 3]
                        ranking = tabela_1.iat[0,4]
                        percentil = tabela_1.iat[0,6]
                        size = tabela_1.iat[0,5]
                        fontsize = 20
                        # Texto de Abertura
                        st.markdown("<h3 style='text-align: center;'>ATACANTE MÓVEL</b></h3>", unsafe_allow_html=True)
                        # Rating/Ranking/Percentil
                        markdown_amount_3 = f"<div style='text-align:center; font-size:{fontsize}px'>{rating:}</div>"
                        markdown_amount_4 = f"<div style='text-align:center; font-size:{fontsize}px'>{ranking:}</div>"
                        markdown_amount_5 = f"<div style='text-align:center; font-size:{fontsize}px'>{percentil:}</div>"
                        markdown_amount_6 = f"<div style='text-align:center; font-size:{fontsize}px'>(Total de {size:} jogadores na Liga)</div>"
                        st.markdown("<h4 style='text-align: center;'>Rating/Ranking/Percentil do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.markdown(markdown_amount_6, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<h4 style='text-align: center;'>Rating</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_3, unsafe_allow_html=True)
                        with col2:
                            st.markdown("<h4 style='text-align: center;'>Ranking</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_4, unsafe_allow_html=True)
                        with col3:
                            st.markdown("<h4 style='text-align: center;'>Percentil</b></h4>", unsafe_allow_html=True)
                            st.markdown(markdown_amount_5, unsafe_allow_html=True)
                        st.markdown("---")
                        ##################################################################################################################### 
                        #####################################################################################################################
                        # #Elaborar Tabela com Métricas do Atleta
                        tabela_2 = pd.read_excel('21_Role_Atacante_Móvel.xlsx')
                        tabela_2 = tabela_2.iloc[:, np.r_[1, 18:27, 6, 27, 29]]
                        tabela_2 = tabela_2[(tabela_2['Atleta']==jogadores)&(tabela_2['Código_Posição_Wyscout']==12)&(tabela_2['Versão_Temporada']==temporada)&(tabela_2['Liga']==liga)]
                        tabela_2 = tabela_2.iloc[:, np.r_[0:10]]
                        tabela_2  = pd.DataFrame(tabela_2)
                        tabela_2 = tabela_2.round(decimals=2)
                        # Média da Liga
                        tabela_b = pd.read_excel('21_Role_Atacante_Móvel.xlsx')
                        tabela_b = tabela_b.iloc[:, np.r_[1, 18:27, 6, 27, 29]]
                        tabela_b = tabela_b[(tabela_b['Código_Posição_Wyscout']==12)&(tabela_b['Versão_Temporada']==temporada)&(tabela_b['Liga']==liga)]
                        tabela_b = tabela_b.iloc[:, np.r_[1:10, 11]]
                        tabela_b = tabela_b.round(decimals=2)
                        tabela_c = (tabela_b.groupby('Liga')[['Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos', 'Acelerações', 'xG', 
                                                              'Conversão_Gols', 'Conversão_xG', 'Ameaça_Ofensiva', 'xA', 
                                                              'Assistência_Finalização']].mean())
                        tabela_c = tabela_c.round(decimals=2)
                        Atleta = ['Média da Liga']
                        tabela_c['Atleta'] = Atleta 
                        tabela_c.insert(0, 'Atleta', tabela_c.pop('Atleta'))
                        # Percentil na Liga
                        tabela_d = pd.read_excel('PlayerAnalysis_Role_21.xlsx')
                        tabela_d = tabela_d.iloc[:, np.r_[54:63, 11, 16, 28, 30]]
                        tabela_d = tabela_d[(tabela_d['Atleta']==jogadores)&(tabela_d['Código_Posição_Wyscout']==12)&(tabela_d['Versão_Temporada']==temporada)&(tabela_d['Liga']==liga)]
                        tabela_d = tabela_d.iloc[:, np.r_[0:9]]
                        tabela_d = tabela_d.rename(columns={'Duelos_Ofensivos_Ganhos_Percentil':'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos_Percentil':'Dribles_BemSucedidos', 
                                                            'Acelerações_Percentil':'Acelerações', 'xG_Percentil':'xG', 'Conversão_Gols_Percentil':'Conversão_Gols', 
                                                            'Conversão_xG_Percentil':'Conversão_xG', 'Ameaça_Ofensiva_Percentil':'Ameaça_Ofensiva', 'xA_Percentil':'xA', 
                                                            'Assistência_Finalização_Percentil':'Assistência_Finalização'})
                        Atleta = ['Percentil na Liga']
                        tabela_d['Atleta'] = Atleta 
                        tabela_d.insert(0, 'Atleta', tabela_d.pop('Atleta'))
                        tabela_2 = tabela_2.append(tabela_c).reset_index()
                        tabela_2 = tabela_2.append(tabela_d).reset_index()
                        tabela_2 = tabela_2.transpose()
                        tabela_2 = tabela_2.drop([tabela_2.index[0], tabela_2.index[1]])
                        st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)
                        st.dataframe(tabela_2, use_container_width=True)
                        ##################################################################################################################### 
                        #####################################################################################################################
                        #Plotar Gráfico
                        # Player Comparison Data
                        st.markdown("<h4 style='text-align: center;'>Comparativo do Jogador com a Média da Liga</h4>", unsafe_allow_html=True)
                        Role_1_Mean_Charts = pd.read_excel('PlayerAnalysis_Role_21.xlsx')
                        #PLOTTING COMPARISON BETWEEN 1 PLAYER AND LEAGUE MEAN
                        #Selecting data to compare 1 player and league mean
                        Role_1_Mean_Charts  = Role_1_Mean_Charts.iloc[:, np.r_[11, 1:10, 16, 28, 30, 36:45]]
                        Role_1_Mean_Charts  = pd.DataFrame(Role_1_Mean_Charts)
                        Role_1_Mean_Charts = Role_1_Mean_Charts[(Role_1_Mean_Charts['Atleta']==jogadores)&(Role_1_Mean_Charts['Versão_Temporada']==temporada)&(Role_1_Mean_Charts['Liga']==liga)]
                        #Preparing League Mean Data
                        League_Mean = Role_1_Mean_Charts.iloc[:, np.r_[13:22]]
                        League_Mean['Atleta'] = 'Média da Liga' 
                        League_Mean.insert(0, 'Atleta', League_Mean.pop('Atleta'))
                        
                        League_Mean = League_Mean.rename(columns={'Duelos_Ofensivos_Ganhos_LM':'Duelos_Ofensivos_Ganhos', 'Dribles_BemSucedidos_LM':'Dribles_BemSucedidos', 
                                                            'Acelerações_LM':'Acelerações', 'xG_LM':'xG', 'Conversão_Gols_LM':'Conversão_Gols', 
                                                            'Conversão_xG_LM':'Conversão_xG', 'Ameaça_Ofensiva_LM':'Ameaça_Ofensiva', 'xA_LM':'xA', 
                                                            'Assistência_Finalização_LM':'Assistência_Finalização'})
                        #Merging Dataframes
                        #Adjusting Player Dataframe
                        Role_1_Mean_Charts  = Role_1_Mean_Charts .iloc[:, np.r_[0:10]]
                        #Concatenating Dataframes
                        Role_1_Mean_Charts = Role_1_Mean_Charts.append(League_Mean).reset_index()

                        #####################################################################################################################
                        #####################################################################################################################

                        # Plotting graph 1
                        # Get Parameters

                        params = list(Role_1_Mean_Charts_1.columns)
                        params = params[2:]
                        #Preparing Data
                        ranges = []
                        a_values = []
                        b_values = []

                        for x in params:
                            a = min(Role_1_Mean_Charts_1[params][x])
                            a = 0
                            b = max(Role_1_Mean_Charts_1[params][x])
                            b = 1
                            ranges.append((a, b))

                        for x in range(len(Role_1_Mean_Charts_1['Atleta'])):
                            if Role_1_Mean_Charts_1['Atleta'][x] == jogadores:
                                a_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                            if Role_1_Mean_Charts_1['Atleta'][x] == 'Média da Liga':
                                b_values = Role_1_Mean_Charts_1.iloc[x].values.tolist()
                                    
                        a_values = a_values[2:]
                        b_values = b_values[2:]

                        values = [a_values, b_values]

                        #Plotting Data
                        title = dict(
                            title_name = jogadores,
                            title_color = '#B6282F',
                            #subtitle_name = clube,
                            #subtitle_color = '#B6282F',
                            title_name_2 = 'Média da Liga',
                            title_color_2 = '#344D94',
                            #subtitle_name_2 = liga,
                            #subtitle_color_2 = '#344D94',
                            title_fontsize = 18,
                            #subtitle_fontsize = 15,
                        ) 

                        endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are per90 & normalized'

                        radar=Radar(fontfamily='Cursive', range_fontsize=8)
                        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
                        plt.savefig('Player&League_Comparison.png')
                        st.pyplot(fig)
                        fig.savefig('Player&League_Comparison.png', dpi=600, bbox_inches="tight")

                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        #####################################################################################################################
                        ##################################################################################################################### 
