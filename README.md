# **Zomato Food Delivery & Dining - Analisando dados com Python**

# Sobre a empresa

A **Zomato** é uma plataforma global dedicada à descoberta de restaurantes e à entrega de alimentos, fundada em 2010 e com sede na Índia. Presente em diversos países, a empresa permite que os usuários explorem uma ampla variedade de estabelecimentos gastronômicos, consultem cardápios, avaliações e classificações. Além de facilitar a busca por restaurantes, cafés e outros locais de alimentação, a Zomato também oferece o serviço de pedidos online, possibilitando a entrega de refeições diretamente na casa dos clientes.

Guiada por uma missão que valoriza a **conexão entre pessoas e comida**, a Zomato celebra a diversidade culinária e busca proporcionar experiências gastronômicas únicas. Seus princípios estão baseados na **transparência, inovação e paixão pela culinária**, impulsionando melhorias contínuas na forma como as pessoas descobrem, compartilham e apreciam refeições. Desempenhando um papel essencial na transformação digital do setor de alimentação, a Zomato se consolida como uma plataforma prática e completa para a comunidade gastronômica global.

# **1. Problema de negócio**

A **Zomato** é um marketplace de restaurantes cujo principal objetivo é conectar clientes e estabelecimentos gastronômicos. Seu **core business** consiste em facilitar o encontro entre quem busca uma boa refeição e os restaurantes que desejam alcançar novos públicos. Na plataforma, os estabelecimentos realizam seu cadastro e disponibilizam informações como endereço, tipo de culinária, possibilidade de reservas, opções de entrega e avaliações de clientes, entre outros dados relevantes.

### O Desafio

Com a recente contratação de um **novo CEO**, a empresa busca compreender de forma mais profunda o funcionamento do negócio para embasar **decisões estratégicas** e ampliar o alcance da plataforma. Para isso, foi proposta uma **análise dos dados da Zomato**, com o objetivo de gerar **dashboards interativos** que permitam visualizar informações sobre os países e cidades cadastrados, bem como detalhes sobre os restaurantes e tipos de culinária disponíveis.

# **2. Premissas**

O modelo de negócio é o marketplace.

A base de dados pública utilizada foi a da plataforma Kaggle, através do link:https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

As principais visões de negócios assumidas foram : Países, Cidades, Restaurantes e tipos de culinária.

# **3. Estratégia da solução**

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa:

- Visão geral

  Aqui são apresentadas métricas gerais da Zomato, além de um mapa mundi para visualização dos seus restaurantes parceiros.

- Países

  Painéis interativos com as principais métricas por país

- Cidades

  Painéis interativos com as principais métricas por cidade

- Culinárias

  Principais indicadores por tipo de culinária

# **4. Principais insights**

- A empresa oferece o serviço em todos continentes.
- Índia tem mais restaurantes cadastrados (311).
- Índia, EUA e Inglaterra lideram em diversidade culinária.
- Brasil tem a menor média de avaliação.
- Índia lidera em restaurantes com reserva.
- Singapura tem o maior custo médio por refeição (valor normalizado em dólar americano).

# **5. O produto final do projeto**

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: https://deiv-cunha-zomatodelivery.streamlit.app/

# **6. Conclusão**

As análises e dashboards permitem que o novo CEO tome decisões data-driven para expandir os negócios e otimizar a plataforma de marketplace.

# **7. Próximos passos**

Gerar uma base de informações sobre os clientes.

Adicionar novas visões de negócios.

Implementar modelos preditivos e de recomendações.

# **8. Tecnologias e Ferramentas utilizadas**

- GitHub
- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Jupyter
- VsCode
