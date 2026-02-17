#BIBLIOTECAS
import streamlit as st
import pandas as pd
import plotly.express as px
# import glob




#PARTE 1 - CONFIGURAÇÕES DA PÁGINA
# Configuração da página (deve ser a primeira linha do Streamlit)
st.set_page_config(
    page_title="SF6 Analytics",
    layout="wide",
    page_icon="🥊" # Pode ser um emoji ou o caminho para uma imagem .png pequena
)

st.title("🎮 Street Fighter 6 - Análise a partir do Rank High Master - TEMPORADA ENCERRADA")
st.markdown("Dashboard interativo para análise.")
st.divider() # Desenha uma linha horizontal para separar o texto dos gráficos

# Função super rápida para ler o arquivo já mastigado
@st.cache_data
def carregar_dados_limpos():
    # Caminho relativo: ele vai procurar o CSV na mesma pasta do script
    caminho = "sf6_dados_limpos.csv" 
    return pd.read_csv(caminho)

df = carregar_dados_limpos()






# --- DAQUI PRA BAIXO É A SUA SEÇÃO DE FILTROS ---
# st.markdown("### 🔍 Filtros")
# ... (o resto do seu código continua exatamente igual) ...



# Função para carregar os dados
# def carregar_dados():
#     # 1. Busca todos os arquivos CSV na pasta
#     caminho_dos_arquivos = r"C:\Users\Kujo Jotaro\Documents\Andrey\Python\SF6/*.csv"
#     arquivos = glob.glob(caminho_dos_arquivos)

#     # 2. Cria uma lista com todos os DataFrames
#     lista_df = []
#     for f in arquivos:
#         df_temp = pd.read_csv(f)
#         lista_df.append(df_temp)

#     # 3. Concatena tudo em um só DataFrame
#     df_principal = pd.concat(lista_df, ignore_index=True)

#     # 4. (Opcional) Remova duplicatas caso algum registro tenha sido pego duas vezes
#     df_principal = df_principal.drop_duplicates()









#     # 3. Dicionário de tradução
#     traducao_ranking = {
#         "rank37": "Legend",
#         "rank42": "Ultimate Master",
#         "rank41": "Grand Master",
#         "rank40": "High Master",
#         "rank36": "Master"
#     }

#     # 4. Usamos uma forma mais segura de acessar a coluna
#     # Caso o nome tenha algum caractere estranho, o Pandas tenta achar o 'Rank ID'
#     df_principal.columns = [c.strip() for c in df_principal.columns]
    
#     if 'Rank ID' in df_principal.columns:
#         df_principal['Rank ID'] = df_principal['Rank ID'].replace(traducao_ranking)
#     else:
#         # Se falhar, essa linha vai te mostrar no site o que o Pandas está vendo
#         st.error(f"Erro Crítico: Coluna 'Rank ID' não encontrada. O Pandas leu: {df_principal.columns.tolist()}")
#         st.stop() # Para a execução aqui para não dar erro lá na frente

#     # Limpeza dos pontos
#     if 'Pontos (AM)' in df_principal.columns:
#         df_principal['Pontos (AM)'] = df_principal['Pontos (AM)'].str.replace(' AM', '', regex=False)
#         df_principal['Pontos (AM)'] = pd.to_numeric(df_principal['Pontos (AM)'], errors='coerce')

#     df_principal = df_principal[df_principal['Rank ID'] != 'Master']

#     return df_principal

# # --- NOVA FUNÇÃO: SEPARADOR DE CLONES (BUCKET FILLING) ---
# def tratar_jogadores_clones(df_bruto):
#     # 1. Ordenamos pelos pontos para garantir que o "Balde 1" fique com os melhores personagens
#     df = df_bruto.sort_values(by=['Pontos (AM)'], ascending=False).reset_index(drop=True)
    
#     controle_baldes = {} # Dicionário para rastrear os personagens de cada "clone"
#     ids_ocultos = []
#     indices_balde = []
    
#     # 2. O Preenchimento dos Baldes
#     for index, row in df.iterrows():
#         nome = row['Jogador']
#         pais = row['País']
#         personagem = row['Personagem']
        
#         chave_jogador = (nome, pais)
        
#         # Se é um jogador novo, cria o primeiro balde vazio para ele
#         if chave_jogador not in controle_baldes:
#             controle_baldes[chave_jogador] = [set()]
            
#         baldes = controle_baldes[chave_jogador]
#         balde_alocado = -1
        
#         # Tenta colocar o personagem no primeiro balde que ainda NÃO tenha esse boneco
#         for i, chars_no_balde in enumerate(baldes):
#             if personagem not in chars_no_balde:
#                 chars_no_balde.add(personagem)
#                 balde_alocado = i
#                 break
                
#         # Se todos os baldes já tiverem esse boneco, cria um NOVO jogador (clone)
#         if balde_alocado == -1:
#             baldes.append(set([personagem]))
#             balde_alocado = len(baldes) - 1
            
#         # Salva o resultado
#         ids_ocultos.append(f"{nome}_{pais}_{balde_alocado + 1}")
#         indices_balde.append(balde_alocado)
        
#     df['ID_Oculto'] = ids_ocultos
    
#     # 3. Criando o Nome Bonito para o Gráfico (O "Pulo do Gato")
#     nomes_exibicao = []
#     for index, row in df.iterrows():
#         nome = row['Jogador']
#         pais = row['País']
#         balde_atual = indices_balde[index]
        
#         # Verifica se esse cara tem clones. Se tiver, adiciona a numeração.
#         total_baldes = len(controle_baldes[(nome, pais)])
#         if total_baldes > 1:
#             nomes_exibicao.append(f"{nome} (#{balde_atual + 1})")
#         else:
#             nomes_exibicao.append(nome) # Se for único, deixa o nome normal
            
#     df['Nome_Exibicao'] = nomes_exibicao
    
#     return df

# --- APLICAÇÃO ---
# Você vai alterar a forma como carrega os dados para usar a função nova:
# df_inicial = carregar_dados()
# df = tratar_jogadores_clones(df_inicial)

# O resto do seu código de filtros continua a partir daqui...











# --- SEÇÃO DE FILTROS (LINHA ÚNICA) ---
st.markdown("### 🔍 Filtros")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    lista_paises = sorted(df['País'].unique())
    paises_sel = st.multiselect("Filtrar por País:", options=lista_paises)

with col_f2:
    lista_personagens = sorted(df['Personagem'].unique())
    personagens_sel = st.multiselect("Filtrar por Personagem:", options=lista_personagens)

with col_f3:
    lista_rank = sorted(df['Rank ID'].unique())
    rank_sel = st.multiselect("Filtrar por Rank:", options=lista_rank)


# --- LÓGICA DE FILTRAGEM COMBINADA ---
df_filtrado = df.copy()

if paises_sel:
    df_filtrado = df_filtrado[df_filtrado['País'].isin(paises_sel)]

if personagens_sel:
    df_filtrado = df_filtrado[df_filtrado['Personagem'].isin(personagens_sel)]

if rank_sel:
    df_filtrado = df_filtrado[df_filtrado['Rank ID'].isin(rank_sel)]

st.divider() # Linha para separar os filtros dos gráficos


# --- LINHA 1: RESUMO DOS RANKINGS ---
st.subheader("📊 Análise por Ranking")

# Criando as colunas (30% para pizza, 70% para barras)
col1, col2 = st.columns([0.3, 0.7])

with col1:
    # 1. Criamos o mapa de cores exato para cada Ranking
    # Ajustei as cores para os códigos que você usou no seu comando
    cores_rank = {
        "Legend": "#CF4D10",          
        "Ultimate Master": "#941EE2",   
        "Grand Master": "#F0BE1C",      
        "High Master": "#c0c0c0"         
    }


    # Gráfico de Pizza
    contagem_ranking = df_filtrado['Rank ID'].value_counts().reset_index()
    contagem_ranking.columns = ['Ranking', 'Quantidade']
    
    fig_pizza = px.pie(
        contagem_ranking, 
        values='Quantidade', 
        names='Ranking',
        color='Ranking',                # ADICIONE ISSO: diz qual coluna define a cor
        color_discrete_map=cores_rank,  # ADICIONE ISSO: aplica o seu mapa de cores
        hole=0, 
        title="Distribuição %",
        template="plotly_dark",
        height=800
    )
    # O comando de mostrar tem que estar AQUI dentro!

    fig_pizza.update_traces(
        textfont_color="white",      # Força o texto dentro da barra a ser branco
        marker_line_color='white',   # Borda branca
        marker_line_width=0.5
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

with col2:
    # 2. Criamos o gráfico usando o mapa
    fig_barras_rank = px.bar(
        contagem_ranking,
        x='Ranking',
        y='Quantidade',
        color='Ranking',                # Ativamos a diferenciação por cor
        color_discrete_map=cores_rank,  # Aplicamos o mapa exato
        title= f"Quantidade total de Personagens: {sum(contagem_ranking['Quantidade'])}",
        template="plotly_dark",
        text_auto=True,
        height=800
    )

    # 3. Adicionamos apenas a borda branca
    fig_barras_rank.update_traces(
        textfont_color="white",      # Força o texto dentro da barra a ser branco
        textposition="outside",       # Garante que o texto fique dentro da barra
        marker_line_color='white',   # Borda branca
        marker_line_width=0.5
    )
    
    st.plotly_chart(fig_barras_rank, use_container_width=True)
    

# --- LINHA 2: POPULARIDADE DOS PERSONAGENS (LARGURA TOTAL) ---
st.divider()
st.subheader("👥 Popularidade dos personagens")

# 1. Preparar os dados baseados no DF FILTRADO (para o filtro de país funcionar aqui também!)
pop_personagem = df_filtrado['Personagem'].value_counts().reset_index()
pop_personagem.columns = ['Personagem', 'Quantidade']

# 1. Defina a cor aqui. O VS Code vai reconhecer o "#2814DD" e criar o quadradinho para você clicar!
cor_das_barras = "#1937C0"

# 2. Criar o gráfico de barras horizontal
fig_pop = px.bar(
    pop_personagem,
    x='Quantidade',
    y='Personagem',
    orientation='h', 
    title="Total de Jogadores por Personagem",
    template="plotly_dark",
    text_auto=True, 
    height=800
)

# 3. Ajustes finos: Cor, Texto e Hover (Mouse)
fig_pop.update_traces(
    marker_color=cor_das_barras,   # Puxa a cor que você vai escolher no quadradinho do VS Code
    marker_line_color='#FFFFFF',   # Bordinha branca (coloquei em HEX pra você poder mudar pelo quadradinho tbm)
    marker_line_width=0.5,
    textangle=0,                   # FORÇA o número a ficar SEMPRE na horizontal
    textposition="outside",        # Joga o número para o lado de fora da barra
    hovertemplate="<b>%{y}</b><br>%{x} jogadores<extra></extra>" # Formata o balão do mouse limpo
)

# Ajuste de layout
fig_pop.update_layout(
    yaxis={'categoryorder':'total ascending'},
    margin=dict(l=150, r=50, t=50, b=50),
    xaxis_title=None, # Remove os títulos de eixo padrão para ficar mais limpo
    yaxis_title=None
)

# 4. Mostrar o gráfico ocupando a linha toda
st.plotly_chart(fig_pop, use_container_width=True)




st.divider()





# --- LINHA DE PAÍSES ---
st.subheader("🌍 Distribuição por País")
col_pais_1, col_pais_2 = st.columns([0.3, 0.7])

# 1. Preparar os dados de PAÍS
contagem_pais = df_filtrado['País'].value_counts().reset_index()
contagem_pais.columns = ['País', 'Quantidade']

# 2. Lógica para agrupar no Top 7 + "Outros"
if len(contagem_pais) > 7:
    top_7_paises = contagem_pais.head(7).copy()
    outros_paises = pd.DataFrame({
        'País': ['Outros'],
        'Quantidade': [contagem_pais['Quantidade'].iloc[7:].sum()]
    })
    df_paises_grafico = pd.concat([top_7_paises, outros_paises], ignore_index=True)
else:
    df_paises_grafico = contagem_pais

# 3. DICIONÁRIO MANUAL DE CORES (O VS Code vai criar os quadradinhos aqui do lado)
cores_paises_custom = {
    "Japão": "#EB0000",       # Vermelho
    "Estados Unidos": "#1C83E1",# Azul
    "Brasil": "#008000",      # Verde
    "Coreia do Sul": "#F0F2F6", # Branco/Cinza
    "França": "#002395",      # Azul Escuro
    "United Kingdom": "#B10B9B",
    "China": "#AF5501",
    "Outros": "#555555"       # Cinza para o resto
}

with col_pais_1:
    # 4. Gráfico de Pizza
    fig_pizza_pais = px.pie(
        df_paises_grafico, 
        values='Quantidade', 
        names='País',
        color='País',
        color_discrete_map=cores_paises_custom, 
        hole=0,
        title="Participação por País",
        template="plotly_dark",
        height=600
    )
    
    # APLICANDO O HOVER DA PIZZA (label e value)
    fig_pizza_pais.update_traces(
        textfont_color="white", 
        marker_line_color='white', 
        marker_line_width=0.5,
        hovertemplate="<b>%{label}</b><br>%{value} jogadores<extra></extra>"
    )
    st.plotly_chart(fig_pizza_pais, use_container_width=True)

with col_pais_2:
    # 5. Gráfico de Barras
    fig_barras_pais = px.bar(
        df_paises_grafico,
        x='País',
        y='Quantidade',
        color='País',
        color_discrete_map=cores_paises_custom, 
        title="Quantidade Total: Top 7 + Outros",
        template="plotly_dark",
        text_auto=True,
        height=600
    )

    # APLICANDO O HOVER DA BARRA (x e y) E LIMPANDO OS EIXOS
    fig_barras_pais.update_traces(
        textfont_color="white", 
        textposition="outside", 
        marker_line_color='white', 
        marker_line_width=0.5,
        hovertemplate="<b>%{x}</b><br>%{y} jogadores<extra></extra>"
    )

    # Ajuste de layout para esconder linhas do fundo e remover nomes de eixos soltos
    fig_barras_pais.update_layout(
        xaxis={
            'categoryorder':'total descending',
            'showgrid': False,   
            'zeroline': False,   
        },
        yaxis={
            'showgrid': False,   
            'zeroline': False
        },
        showlegend=False,
        xaxis_title=None, 
        yaxis_title=None
    )
    
    st.plotly_chart(fig_barras_pais, use_container_width=True)












# --- NOVA SEÇÃO: ANÁLISE DE JOGADORES ---
st.divider()
st.header("👤 Perfil dos Jogadores")

# A MÁGICA DA CORREÇÃO AQUI:
# 1. Descobre quem são as pessoas que passaram no filtro lá de cima (Ex: Quem joga de Mai no BR)
jogadores_ativos = df_filtrado['Nome_Exibicao'].unique()

# 2. Vai no 'df' original e puxa o "arsenal" completo SÓ desses caras
df_jogadores_ativos_completo = df[df['Nome_Exibicao'].isin(jogadores_ativos)]

# 3. Faz as contagens em cima do arsenal completo deles!
contagem_chars_por_jogador = df_jogadores_ativos_completo['Nome_Exibicao'].value_counts()
total_jogadores = len(jogadores_ativos)
total_registros = len(df_jogadores_ativos_completo)

# 1. Métricas Globais da Seção (ANTES DO FILTRO)
m1, m2 = st.columns(2)

with m1:
    texto_ajuda = "Quantidade de contas únicas (jogadores reais). Um mesmo jogador pode atingir o rank Master com múltiplos personagens."
    st.metric("Jogadores Únicos", total_jogadores, help=texto_ajuda)

with m2:
    media_char_por_player = total_registros / total_jogadores if total_jogadores > 0 else 0
    st.metric("Média Geral (Personagens/Jogador)", f"{media_char_por_player:.2f}")

st.divider()

# 2. Filtro Interativo de Versatilidade (Slider)
st.markdown("#### ⚙️ Filtros de Versatilidade")
min_chars = st.slider(
    "Mostrar estatísticas para jogadores com pelo menos quantos personagens?", 
    min_value=1, max_value=29, value=2,
    help="Deslize para ver como o ranking muda quando exigimos que o jogador domine mais personagens."
)

jogadores_acima_filtro = (contagem_chars_por_jogador >= min_chars).sum()
st.info(f"🎯 **{jogadores_acima_filtro} jogadores** na seleção atual possuem **{min_chars} ou mais** personagens no ranking geral.")

# 3. Top 15 Rankings (Gráficos Lado a Lado)
col_jog_1, col_jog_2 = st.columns(2)

cor_barras_qtd = "#E53935" 
cor_barras_pts = "#1E88E5" 

with col_jog_1:
    st.subheader("🏆 Top 15: Mais Personagens")
    top_multi = contagem_chars_por_jogador.head(15).reset_index()
    top_multi.columns = ['Jogador', 'Qtd Personagens']
    
    fig_multi = px.bar(
        top_multi, x='Qtd Personagens', y='Jogador', orientation='h',
        template="plotly_dark", height=500,
        text_auto=True 
    )
    
    fig_multi.update_traces(
        marker_color=cor_barras_qtd,
        textfont_color="white", 
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x} personagens<extra></extra>"
    )
    
    fig_multi.update_layout(
        showlegend=False, 
        yaxis={'categoryorder':'total ascending'},
        xaxis={'showgrid': False, 'zeroline': False},
        xaxis_title=None, 
        yaxis_title=None,
        margin=dict(r=50) 
    )
    
    st.plotly_chart(fig_multi, use_container_width=True)

with col_jog_2:
    st.subheader(f"📈 Top 15: Média de Pontos")
    
    jogadores_validos = contagem_chars_por_jogador[contagem_chars_por_jogador >= min_chars].index
    
    if len(jogadores_validos) > 0:
        # ATENÇÃO AQUI: Trocamos df_filtrado pelo df completo desses jogadores
        df_validos = df_jogadores_ativos_completo[df_jogadores_ativos_completo['Nome_Exibicao'].isin(jogadores_validos)]
        
        top_media = df_validos.groupby('Nome_Exibicao')['Pontos (AM)'].mean().sort_values(ascending=False).head(15).reset_index()
        top_media.columns = ['Jogador', 'Média Pontos']
        top_media['Média Pontos'] = top_media['Média Pontos'].astype(int)
        
        top_media['Jogador (Qtd)'] = top_media['Jogador'].apply(lambda x: f"{x} ({contagem_chars_por_jogador[x]} personagens)")
        top_media['Texto_Barra'] = top_media['Média Pontos'].astype(str) + " pontos AM"
        
        fig_media = px.bar(
            top_media, x='Média Pontos', y='Jogador (Qtd)', orientation='h',
            template="plotly_dark", height=500,
            text='Texto_Barra' 
        )
        
        fig_media.update_traces(
            marker_color=cor_barras_pts,
            textfont_color="white", 
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x} pontos AM<extra></extra>"
        )
        
        fig_media.update_layout(
            showlegend=False, 
            yaxis={'categoryorder':'total ascending'},
            xaxis={'showgrid': False, 'zeroline': False},
            xaxis_title=None, 
            yaxis_title=None,
            margin=dict(r=100) 
        )
        
        st.plotly_chart(fig_media, use_container_width=True)
    else:
        st.warning(f"Nenhum jogador possui {min_chars} ou mais personagens com os filtros atuais.")


# 4. BUSCA POR JOGADOR (O "Card de Detalhes")
st.divider()
st.subheader("🔍 Consultar Ficha Completa do Jogador")

# 1. Pegamos os nomes, tiramos os vazios (dropna), forçamos ser texto (astype) e pegamos os únicos
lista_nomes_limpa = df_filtrado['Nome_Exibicao'].dropna().astype(str).unique().tolist()

# 2. Agora sim passamos para o Selectbox ordenado com segurança
nome_busca = st.selectbox(
    "Selecione ou digite o nome do jogador:", 
    options=[""] + sorted(lista_nomes_limpa)
)

if nome_busca:
    # O resto do seu código continua idêntico!
    dados_jogador = df[df['Nome_Exibicao'] == nome_busca].sort_values(by='Pontos (AM)', ascending=False)
    
    st.info(f"Exibindo Dossiê de Elite para: **{nome_busca}**")
    
    c_p1, c_p2 = st.columns([0.4, 0.6])
    
    with c_p1:
        # Pega o personagem que está na primeira linha (o com maior pontuação)
        main_character = dados_jogador['Personagem'].iloc[0]
        
        st.write(f"🌍 **País:** {dados_jogador['País'].iloc[0]}")
        st.write(f"🎮 **Main (Principal):** {main_character}")
        st.write(f"📊 **Total de Personagens Master:** {len(dados_jogador)}")
        st.write(f"🏆 **Melhor Pontuação:** {int(dados_jogador['Pontos (AM)'].max())} pts")
        st.write(f"⚖️ **Média Geral:** {int(dados_jogador['Pontos (AM)'].mean())} pts")
    
    with c_p2:
        # Tabela bonitinha listando o "arsenal" do jogador
        st.markdown("**Personagens Utilizados:**")
        st.dataframe(
            dados_jogador[['Personagem', 'Rank ID', 'Pontos (AM)']], 
            hide_index=True,
            use_container_width=True
        )