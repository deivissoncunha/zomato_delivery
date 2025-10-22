#Libraries
from haversine import haversine
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
from PIL import Image
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Cities", page_icon="🏙️")

# -------------------------------------------------------------------
# Funções
# -------------------------------------------------------------------
def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar, formatar e modificar o dataframe.

        Itens realizados:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Inclusão da coluna nome do país em função do código do país
        4. Inclusão da coluna tipo de catergoria de comida
        5. Inclusão da coluna nome da cor em função do código da cor
        6. Remoção de duplicatas de linhas
        7. Categorização do restaurante por um tipo de culinária
        8. Conversão do câmbio (coluna currency) para dólar americano
        9. Modificação do texto e reordenação das colunas

        Input: Dataframe
        Output: Dataframe
    """
    # Retirando os valores nulos (texto e ausente)
    colunas_criticas = ['Cuisines']
    df1 = df1.dropna(subset=colunas_criticas)
    
    #Preenchimento do nome dos países
    COUNTRIES = {
      1: "India",
      14: "Australia",
      30: "Brazil",
      37: "Canada",
      94: "Indonesia",
      148: "New Zeland",
      162: "Philippines",
      166: "Qatar",
      184: "Singapure",
      189: "South Africa",
      191: "Sri Lanka",
      208: "Turkey",
      214: "United Arab Emirates",
      215: "England",
      216: "United States of America",
    }
    def country(country_id):
    
      return COUNTRIES[country_id]
    
    df1["country"] = df1["Country Code"].replace(COUNTRIES)
    
    #Criação do Tipo de Categoria de Comida
    def create_price_tye(price_range):
      if price_range == 1:
        return "cheap"
      elif price_range == 2:
        return "normal"
      elif price_range == 3:
        return "expensive"
      else:
        return "gourmet"
    
    df1["category_food"] = df1["Price range"].dropna().apply(create_price_tye)
    
    #Criação do nome das Cores
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    def color_name(color_code):
      return COLORS[color_code]
    
    df1["color_name"] = df1["Rating color"].replace(COLORS)
    
    #Remover duplicatas de linhas
    df1 = df1.drop_duplicates()
    df1 = df1.reset_index(drop=True)
    
    # Categorização do restaurante por um tipo de culinária
    df1['Cuisines'] = df1.loc[:, 'Cuisines'].apply(lambda x: x.split(",")[0])

    # Conversão do câmbio (coluna currency) para dólar americano
    # taxas dia 06/10/2025 ( pode atualizar com taxas atuais)
    currency_to_usd = {
        "Botswana Pula(P)": 0.075,       # 1 P = 0.075 USD
        "Brazilian Real(R$)": 0.19,      # 1 BRL = 0.19 USD
        "Dollar($)": 1.00,               # já é dólar
        "Emirati Diram(AED)": 0.27,      # 1 AED = 0.27 USD
        "Indian Rupees(Rs.)": 0.012,     # 1 INR = 0.012 USD
        "Indonesian Rupiah(IDR)": 0.000060, # 1 IDR = 0.000060 USD
        "NewZealand($)": 0.58,           # 1 NZD = 0.58 USD
        "Pounds(£)": 1.35,               # 1 GBP = 1.35 USD
        "Qatari Rial(QR)": 0.27,         # 1 QAR = 0.27 USD
        "Rand(R)": 0.058,                # 1 ZAR = 0.058 USD
        "Sri Lankan Rupee(LKR)": 0.0033, # 1 LKR = 0.0033 USD
        "Turkish Lira(TL)": 0.024        # 1 TRY = 0.024 USD
    }
    
    df1["cost_for_two_usd"] = df1.apply(lambda row: row["Average Cost for two"] * currency_to_usd.get(row["Currency"], 1),axis=1)

    # Padroniza nomes (snake_case) das colunas
    df1.columns = [col.strip().lower().replace(" ", "_") for col in df1.columns]

    #Renomear colunas específicas
    df1 = df1.rename(columns={
         "country": "country"})

    # Remove colunas desnecessárias
    df1 = df1.drop(columns=['country_code', 'locality_verbose', 'currency', 'switch_to_order_menu', 'rating_text'])

    # Remover outlier coluna cost_for_two_usd == Australia
    df1 = df1.drop(index=356)

    # Organizando a sequência das colunas do df
    df1 = df1[ ['restaurant_id', 'restaurant_name', 'country', 'city',
                 'cuisines', 'aggregate_rating', 'cost_for_two_usd', 'address',
                 'has_table_booking', 'has_online_delivery', 'is_delivering_now', 'price_range',
                 'locality', 'longitude', 'latitude', 'votes', 'category_food', 'color_name', 'average_cost_for_two']]

    return df1

# ========================Inicio da Estrutura Lógica do código===========================

# Import Dataset
df = pd.read_csv('dataset/zomato.csv')

# ===================================================================
# limpeza dos dados
# ===================================================================

df1 = clean_code(df)

#=============================================
# Cities
#=============================================

# ============================================
# Barra Lateral
# ============================================

with st.sidebar.container():
        col1, col2 = st.columns ([1, 3], gap = 'small')
    
        with col1:
            image_path = 'logo.png'
            image = Image.open (image_path)
            col1.image(image,width=60)
    
        with col2:
            col2.markdown ('# Fome Zero')

st.sidebar.markdown ('## Filtros')

paises = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar as Informações',
    df1['country'].unique().tolist(),
    default=df1['country'].unique().tolist())

# Filtro de países
linhas_selecionadas = df1['country'].isin( paises)
df1 = df1.loc[linhas_selecionadas, :]

# ============================================
# layout no Stramlit
# ============================================

st.markdown ('# 🏙️ Visão Cidades')

with st.container(): 
    df_aux = df1.loc[:, ['restaurant_id', 'city', 'country']].groupby(['city', 'country']).nunique().sort_values(by='restaurant_id', ascending=False).reset_index().head(10)

    fig = px.bar(df_aux, x='city', y='restaurant_id', text = 'restaurant_id', color = 'country')
    fig.update_layout(
        title="Top 10 Cidades com mais Restaurantes na base de dados",
        title_x=0.3,  # centraliza o título
        xaxis_title="Cidade",
        yaxis_title="Quantidade de Restaurantes",
        legend_title_text= "País")
    st.plotly_chart(fig,use_container_width=True)

with st.container():
    col1, col2 = st.columns (2)

    with col1:
        df_aux = df1.loc[df1['aggregate_rating'] > 4, ['restaurant_id', 'city', 'country']].groupby(['city', 'country']).nunique().sort_values(by='restaurant_id', ascending=False).reset_index().head(7)

        fig = px.bar(df_aux,
                     x='city',
                     y='restaurant_id',
                     text = 'restaurant_id',
                     color = 'country',
                     category_orders={"city": df_aux["city"].tolist()})  # mantém ordem do df_aux
        
        fig.update_layout(
            title="Top 7 Cidades com mais Restaurantes com média de avaliação acima de 4",
            title_x=0.1,  # centraliza o título
            xaxis_title="Cidade",
            yaxis_title="Quantidade de Restaurantes",
            legend_title_text= "País")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        df1.loc[df1['aggregate_rating'] < 2.5, ['restaurant_id', 'city', 'country']].groupby(['city', 'country']).nunique().sort_values(by='restaurant_id', ascending=False).reset_index().head(7)

        fig = px.bar(df_aux,
                     x='city',
                     y='restaurant_id',
                     text = 'restaurant_id',
                     color = 'country',
                     category_orders={"city": df_aux["city"].tolist()})  # mantém ordem do df_aux
        
        fig.update_layout(
            title="Top 7 Cidades com os Restaurantes com média de avaliação abaixo de 2.5",
            title_x=0.1,  # centraliza o título
            xaxis_title="Cidade",
            yaxis_title="Quantidade de Restaurantes",
            legend_title_text= "País")
        st.plotly_chart(fig,use_container_width=True)

with st.container():
    df_aux = (df1.loc[:, ['cuisines', 'city', 'country']]
            .groupby(['city','country'])
            .nunique().sort_values(by='cuisines', ascending=False)
            .reset_index().head(10))

    fig = px.bar(df_aux,
                 x='city',
                 y='cuisines',
                 text = 'cuisines',
                 color = 'country',
                 category_orders={"city": df_aux["city"].tolist()})  # mantém ordem do df_aux
    
    fig.update_layout(
        title="Top 10 Cidades com mais maior número de culinárias distintas",
        title_x=0.3,  # centraliza o título
        xaxis_title="Cidade",
        yaxis_title="Tipo distintos de culinárias",
        legend_title_text= "País")
    st.plotly_chart(fig,use_container_width=True)