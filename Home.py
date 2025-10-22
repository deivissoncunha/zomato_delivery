#bibliotecas necessarias
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Fome Zero",
    page_icon="🍽️",
    layout="wide"
)


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

st.write ("# Zomato Food Delivery & Dining - Growth Dashboard")

st.markdown (
    """
    Este Growth Dasboard, denominado projeto Fome Zero, foi construído para acompanhar as métricas de crescimento de negócio da Zomato Food Delivery & Dining app.
    ### Como utilizar esse Growth Dashboard?
    Itens de análise na aba lateral da página.
    
    - Visão geral    
        - Métricas gerais da Zomato, além de um mapa mundi para vizualização dos seus restaurantes parceiros    
    - Países    
        - Painéis interativos com as principais métricas por país
    - Cidades    
        - Painéis interativos com as principais indicadores por cidades    
    - Culinárias    
        - Métricas gerais por tipo de culinária
    
    ### Entre em contato:
    
    e-mail: deivissonlcunha@gmail.com 
    
    LinkedIn: http://www.linkedin.com/in/deivisson-cunha
    """)










    