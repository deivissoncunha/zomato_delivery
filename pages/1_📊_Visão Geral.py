#bibliotecas necessarias
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
from PIL import Image
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from haversine import haversine

st.set_page_config(
    page_title="Fome Zero",
    page_icon="🍽️",
    layout="wide"
)

# -------------------------------------------------------------------
# Funções
# -------------------------------------------------------------------
def mapas_restaurantes(df1):
    # Agrupando dados
    df_aux = (df1.loc[:, ['city', 'aggregate_rating', 'latitude', 'longitude', 'color_name']]
    .groupby(['city', 'aggregate_rating', 'color_name'])
    .mean().reset_index())
    
    # Dicionário de cores
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }
    
    # Cria o mapa centralizado
    m = folium.Map(location=[df_aux['latitude'].mean(), df_aux['longitude'].mean()],
                   zoom_start=3, tiles="CartoDB positron")
    
    # Cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Adiciona círculos com raio proporcional à nota
    for _, row in df_aux.iterrows():
        rating = row['aggregate_rating']
    
        # Definir raio: base 5 + (nota * 2) → entre 5 e 15, por exemplo
        radius = 5 + (rating * 2)
    
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            popup=f"<b>Cidade:</b> {row['city']}<br><b>Avaliação:</b> {rating}",
            color=COLORS.get(row['color_name'], "gray"),
            fill=True,
            fill_color=COLORS.get(row['color_name'], "gray"),
            fill_opacity=0.8
        ).add_to(marker_cluster)
    return m
    
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
    def country_name(country_id):
    
      return COUNTRIES[country_id]
    
    df1["country_name"] = df1["Country Code"].replace(COUNTRIES)
    
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
         "country_name": "country"})

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
# Main Menu
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
    'Escolha os Países que deseja visualizar os Restaurantes',
    df1['country'].unique().tolist(),
    default=df1['country'].unique().tolist())

# Filtro de países
linhas_selecionadas = df1['country'].isin( paises)
df1 = df1.loc[linhas_selecionadas, :]


st.sidebar.markdown ('## Dados Tratados')

# Converter para CSV (string em memória)
csv = df1.to_csv(index=False).encode('utf-8')

# Colocar botão de download na barra lateral
st.sidebar.download_button(
    label="📥 Download",
    data=csv,
    file_name="dados_tratados.csv",
    mime="text/csv"
)

# ============================================
# layout no Stramlit
# ============================================

st.markdown ('# Fome Zero!')
st.markdown ('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

with st.container():
        st.markdown('### Temos as seguintes marcas dentro da nossa plataforma')
        col1, col2, col3, col4, col5 = st.columns (5, gap = 'large')
        
        with col1:
            restaurants = df1['restaurant_id'].nunique()
            col1.metric ('Restaurantes Cadastrados', restaurants)
            
        with col2:
            paises = df1['country'].nunique()
            col2.metric ('Países Cadastrados', paises)

        with col3:
            cidades = df1['city'].nunique()
            col3.metric ('Cidades Cadastradas', cidades)
            
        with col4:
            avaliacao = df1['votes'].sum()
            col4.metric ('Avaliações feitas na plataforma', avaliacao)
            
        with col5:
            culinarias = df1["cuisines"].nunique()
            col5.metric ('Tipos de Culinárias oferecidas', culinarias)

with st.container():
        m = mapas_restaurantes(df1)
        st_folium(m, width=None, height=600)