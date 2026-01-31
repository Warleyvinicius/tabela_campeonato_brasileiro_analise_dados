import requests
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import plotly.express as px 
from datetime import datetime

# Url do Site
URL ='https://www.mat.ufmg.br/futebol/classificacao-geral_seriea/'
URL_PROBABILIDADE_CAMPEAO ='https://www.mat.ufmg.br/futebol/campeao_seriea/'

# Fazer Requisição do HTTP
response = requests.get(URL)
response_camp = requests.get(URL_PROBABILIDADE_CAMPEAO)


# Parse do Conteúdo HTML
soup = BeautifulSoup(response.content, 'html.parser')
soup_camp = BeautifulSoup(response_camp.content, 'html.parser')


# Encontrar a Tabela no HTML
table = soup.find('table')
table_camp = soup_camp.find('table')


# Extrair os Dados da Tabela
data = []
headers = [header.text for header in table.find_all('th')]

data_camp = []
headers_camp = [header.text for header in table_camp.find_all('th')]



# Extrair os Dados das Linhas
for row in table.find_all('tr')[1:]:
    columns = row.find_all('td')
    data.append([column.text for column in columns])

for row in table_camp.find_all('tr')[1:]:
    columns = row.find_all('td')
    data_camp.append([column.text for column in columns])
    

# Criar DataFrame com Pandas
tabela = pd.DataFrame(data, columns=headers)
tabela_campeao = pd.DataFrame(data_camp, columns=headers_camp)


#  Personalizar Tabela

pd.set_option('display.width',1000)   #   Tamanho Exibição tabela no Terminal

# Renomear Colunas

tabela_campeao = tabela_campeao.rename(columns={
    'N' : 'Pos',
    'Times' : 'Times_',
    'Prob(%)':'Chance Campeão (%)'
})

# Exibição de Columns Especificas
tabela_campeao = tabela_campeao[['Chance Campeão (%)']]

# Renomear Colunas
tabela = tabela.rename(columns={
    'N':'Posição',
    'Times':'Times',
    'PG':'Pontos',
    'J':'Jogos',
    'V':'Vitorias',
    'E':'Empates',
    'D':'Derrotas',
    'GF':'Gols Marcados',
    'GC':'Gols Sofridos',
    'S':'Saldo Gols',
    'R':'Aproveitamento Campeonato (%)'
    
})

#  Usando o Index para merge
tabela_completa = tabela.merge(tabela_campeao,left_index=True,right_index=True)

# Exibição de Columns Especificas
tabela = tabela_completa[['Posição','Times','Jogos','Vitorias','Empates','Derrotas','Gols Marcados','Gols Sofridos','Saldo Gols','Pontos','Chance Campeão (%)','Aproveitamento Campeonato (%)']]

# Variavel para Salvar Ano Atual
ano_atual = datetime.now().year

# -------------------  Exibição Streamlit------------------------------

# Titulo Pagina
st.title(f'🥅 Tabela do Campeonato Brasileiro {ano_atual}🥅')

# Tabela Campeonato
#   Aumentar Tabela tamanho Janela
st.set_page_config(layout="wide") 

# Ocultar o Index Streamlit
st.dataframe(tabela,hide_index=True,use_container_width=True)      




#  ------------------  Grafico Streamlit   ------------------
st.header('📊 Análise de Dados do Campeonato ')


# ---------------  Dashboard Probabilidade de Ganhar Campeonato  ---------------
#       Personalização Texto Dentro da Barra Grafico

# Tamanho Total da Tabela
total = len(tabela_campeao)

# Cores da Tabela Chance Campeao (%)
meio_tabela_campeao = total - 8

cor_campeao = ['blue']*4,['green']*meio_tabela_campeao,['red']*4

#  Acrescentar Strings % no Valor de Cada Coluna
campeao =[f'{x}.%'for x in tabela_completa['Chance Campeão (%)']]

chance_campeao = px.bar(
    tabela_completa,
    x='Times',
    y='Chance Campeão (%)',
    text= campeao,
    title='Chance De Levantar a Taça do Campeonato 🏆 '
    
)
#  Trocar as cores da Tabela
chance_campeao.update_traces(marker_color = cor_campeao)

# Retirar Linhas do Grafico
chance_campeao.update_yaxes(showgrid=False)

# Aumentar o eixo Y

chance_campeao.update_yaxes(range=[0,100])





# ---------------  Dashboard Aproveitamento Dentro do Campeonato  ---------------

#       Personalização Texto Dentro da Barra Grafico
aproveitamento = [f'{x}%' for x in tabela['Aproveitamento Campeonato (%)']]

aproveitamento = px.bar(
    
    #
    tabela,
    x='Times',
    y='Aproveitamento Campeonato (%)',
    
    # Titulo do Grafico
    title='Aproveitamento dos Times no Campeonato 📊',
    
    # Texto Dentro do Grafico
    text= aproveitamento
    
)
#               Personalizando o Grafico 
 
# Ajustando Valores do Eixo Y para ir ate 100
aproveitamento.update_yaxes(range=[0,100])

# Retirar as linhas atras do Grafico
aproveitamento.update_yaxes(showgrid=False)



#        Mudar as cores da Barra do Grafico 

# Personalizar as linhas Restantes do meio da Tabela ( Tamanho Total da Tabela  - 7 colunas(3 iniciais e 4 finais))
meio_tabela = total - 8

#       Aplicando as Cores Personalizadas

#           Inicio           Meio Tabela         Fim Tabela
cores = ['blue'] *4 + ['#0F92FC'] * meio_tabela + ['red'] *4
aproveitamento.update_traces(marker_color= cores)




# ---------------  Dashboard Gols Marcados  ---------------

gols_marcados = px.bar(
    tabela,
    x='Times',
    y='Gols Marcados',
    title='Gols Marcados 📈',
    text='Gols Marcados'
)


#       Aplicando as Cores Personalizadas

gols_marcados.update_traces(marker_color='blue')

#        Retirar as linhas atras do Grafico
gols_marcados.update_yaxes(showgrid=False)


# ---------------  Dashboard Gols Sofridos  ---------------

gols_sofridos = px.bar(
    tabela,
    x='Times',
    y='Gols Sofridos',
    title='Gols Sofridos 📉',
    text='Gols Sofridos'
)

#       Aplicando as Cores Personalizadas

gols_sofridos.update_traces(marker_color='red')

#       Retirar as linhas atras do Grafico
gols_sofridos.update_yaxes(showgrid=False)



# ---------------  Dashboard Saldo de Gols  ---------------
#          Aplicando Cores Personalizadas
tabela['* Legenda'] = tabela['Saldo Gols'].astype(int).apply(lambda x: 'Saldo Negativo' if x<0 else 'Saldo Positivo')


saldo_gols = px.bar(
    tabela,
    x='Times',
    y='Saldo Gols',
    title='Saldo Gols ⚽',
    text='Saldo Gols',
    color='* Legenda',
    color_discrete_map={
        'Saldo Negativo':'red',
        'Saldo Positivo':'green',
    }
)

#  Retirar Linhas do Grafico
saldo_gols.update_yaxes(showgrid=False)


# ---------------  Dashboard Jogos Feitos  ---------------
#          Mapeando Valores da Coluna Jogos
total_jogos = tabela['Jogos'].astype(int).max()
tabela['Total de Jogos'] = tabela['Jogos'].astype(int).apply(lambda x: 'Jogos a Menos' if x < total_jogos else('Jogos Finalizados' if x == 38 else f'Jogos {total_jogos}/38'))

jogos_realizados = px.bar(
    tabela,
    title='Jogos Realizados ✅',
    x ='Times',
    y='Jogos',
    text='Jogos',
    color = 'Total de Jogos',
    color_discrete_map={
        'Jogos a Menos':'red',
        f'Jogos {total_jogos}/38':'green',
        'Jogos Finalizados':'blue'
    }
)

#          Alterando Valor Eixo Y
jogos_realizados.update_yaxes(range = [1,38])

#  Retirar Linhas do Grafico
jogos_realizados.update_yaxes(showgrid=False)


# ---------------  Dashboard Rodadas do Campeonato  ---------------

#  Titulo Dashboard Jogos Restantes e Completos

jogos_campeonato = tabela['Jogos'].astype(int).max()
rodadas_totais = 38
cor_pie =['green','blue']

#  Criação dicionario DF 
jogos_totais_restantes =pd.DataFrame({
    'Categoria':['Jogos Realizados','Jogos Restantes'],
    'Valor':[jogos_campeonato,rodadas_totais-jogos_campeonato]
})


Jogos_Campeonato = px.pie(
    jogos_totais_restantes,
    values='Valor',
    names='Categoria',
    hole=0.8,
    title='Progresso do Campeonato ⚡',
    color_discrete_sequence=cor_pie
)

Jogos_Campeonato.update_traces(marker=dict(line=dict(color="black", width=3)),textinfo="percent+label",textfont=dict(color="white", size=14))







# ---------------  Exibição dos Gráficos  ---------------

st.plotly_chart(chance_campeao)      # Dashboard Chance dos Times Serem Campeão
st.plotly_chart(aproveitamento)      # Dashboard Aproveitamento Times
st.plotly_chart(gols_marcados)       # Dashboard Gols Marcados
st.plotly_chart(gols_sofridos)       # Dashboard Gols Sofridos
st.plotly_chart(saldo_gols)          # Dashboard Saldo Gols
st.plotly_chart(jogos_realizados)    # Dashboard Jogos Realizados
st.plotly_chart(Jogos_Campeonato)




# Link para Redirecionamento para Tabela Atualizado
#st.markdown(f'[Confira os Proximos Jogos do Campeonato Brasileiro {ano_atual}](https://www.google.com/search?q=rodadas+do+brasileir%C3%A3o+atualizada&sca_esv=9c49312c20cc6857&hl=pt_BR&sxsrf=AE3TifMjdLwwV2FHke_khSmU5YceWi7Rag%3A1763645504752&ei=QBgfaZjWLbj65OUPmqWz6Qs&oq=rodadas+atua&gs_lp=Egxnd3Mtd2l6LXNlcnAiDHJvZGFkYXMgYXR1YSoCCAAyBhAAGBYYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIFEAAY7wUyBRAAGO8FSKMvULsGWMIbcAV4AJABApgBwQOgAdcVqgEKMC4xMi4xLjEuMbgBA8gBAPgBAZgCEqAClxLCAgcQIxiwAxgnwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAhMQLhiABBiwAxhDGMgDGIoF2AEBwgIEECMYJ8ICChAjGIAEGCcYigXCAgoQLhiABBhDGIoFwgIFEC4YgATCAhEQABiABBixAxiDARiKBRiNBsICDhAAGIAEGLEDGIMBGIoFwgIQEAAYgAQYsQMYQxiDARiKBcICEBAuGIAEGLEDGEMYgwEYigXCAhAQABiABBixAxiDARgUGIcCwgIKEAAYgAQYQxiKBcICCxAAGIAEGLEDGIMBwgIFEAAYgATCAg8QABiABBixAxiDARgKGAvCAgkQABiABBgKGAvCAgcQABiABBgKwgIQEAAYgAQYsQMYgwEYigUYCsICDRAAGIAEGLEDGIMBGA3CAgcQABiABBgNwgIQEAAYgAQYsQMYgwEYigUYDcICEhAAGIAEGLEDGIMBGIoFGAoYDcICChAAGIAEGBQYhwKYAwCIBgGQBhO6BgYIARABGAiSBwg1LjEyLjAuMaAHxq8BsgcIMC4xMi4wLjG4B7YRwgcIMi00LjEyLjLIB8sB&sclient=gws-wiz-serp#sie=lg;/g/11lw0zjj1m;2;/m/0fnk7q;mt;fp;1;;;)')




