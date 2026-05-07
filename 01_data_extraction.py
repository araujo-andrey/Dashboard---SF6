import requests
import pandas as pd
import time
import random

# --- 1. CONFIGURAÇÕES ---
BUILD_ID = "xxxxxxxxxxxxxxxx" # Verificar no json qual o endereço, pois muda regularmente
SEASON = 2
URL_BASE = f"https://www.streetfighter.com/6/buckler/_next/data/{BUILD_ID}/pt-br/ranking/master.json"

HEADERS = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/145.0.0.0 Safari/537.36',
    'x-nextjs-data': '1'    
}

# Olhar os cookies que podem mudar
COOKIES = {
    'buckler_id': 'xxxxxxxxxxxxxxxxxxx',
    'buckler_r_id': 'xxxxxxxxxxxxxxxxxxxxx'
}

def raspar_pagina(pagina):
    """Função isolada para raspar uma única página."""
    params = {'page': pagina, 'season_type': SEASON}
    try:
        response = requests.get(URL_BASE, headers=HEADERS, cookies=COOKIES, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            jogadores = data['pageProps']['master_rating_ranking']['ranking_fighter_list']
            
            lista_temp = []
            for j in jogadores:
                # Mapeando os "caminhos" (subpastas) do JSON
                info_banner = j.get('fighter_banner_info', {})
                info_pessoal = info_banner.get('personal_info', {})
                play_points = info_banner.get('favorite_character_play_point', {})
                
                # --- NOVAS PASTAS MAPEADAS ---
                league_info = info_banner.get('favorite_character_league_info', {})
                main_circle = info_banner.get('main_circle', {})
                title_data = info_banner.get('title_data', {})
                max_play = info_banner.get('max_content_play_time', {})
                
                lista_temp.append({
                    'ID_Unico': info_pessoal.get('short_id'),
                    'Jogador': info_pessoal.get('fighter_id', 'N/A'),
                    'Clube': main_circle.get('circle_name', 'Sem Clube'), # NOVO
                    'Titulo': title_data.get('title_data_val', 'Sem Título'), # NOVO
                    'Personagem': j.get('character_name', 'N/A'),
                    'Posicao_Global': j.get('master_rating_ranking', 0), # NOVO
                    'Pontos_MR': j.get('rating', 0),
                    'Pontos_LP': league_info.get('league_point', j.get('league_point', 0)), # CORRIGIDO
                    'Rank_ID': j.get('master_league', 0),
                    'País': info_banner.get('home_name', 'Desconhecido'),
                    'Plataforma': info_pessoal.get('platform_name', 'N/A'),
                    'Tipo_Controle': info_banner.get('battle_input_type', 'N/A'),
                    'Tempo_FightingGround': play_points.get('fighting_ground', 0),
                    'Tempo_BattleHub': play_points.get('battle_hub', 0),
                    'Tempo_WorldTour': play_points.get('world_tour', 0),
                    'Tempo_Total': max_play.get('play_time', 0), # NOVO
                    'Last_Play': info_banner.get('last_play_at', 0)
                })
            return lista_temp, 200
        
        return [], response.status_code
        
    except Exception as e:
        return [], str(e)

# --- 2. LOOP PRINCIPAL (VERSÃO COMPLETA) ---
def main():
    print(f"🚀 Iniciando extração da Temporada {SEASON}...")
    
    lista_jogadores = []
    paginas_com_erro = []
    pagina_atual = 1 # Começa na 1 e vai até o servidor dizer que acabou!
    
    while True:
        jogadores_da_pagina, status = raspar_pagina(pagina_atual)
        
        # Erro fatal (Cookies)
        if status in [401, 403]:
            print("\n⛔ ERRO: Seus Cookies expiraram! Atualize o script e rode de novo.")
            break
            
        # Sucesso
        elif status == 200:
            if len(jogadores_da_pagina) == 0:
                print(f"\n🏁 Fim da lista! Última página lida: {pagina_atual - 1}")
                break
                
            lista_jogadores.extend(jogadores_da_pagina)
            print(f"\r✅ Pág {pagina_atual} OK | Total raspado:     {len(lista_jogadores)}", end="")
            
        # Erro de rede ou servidor engasgou
        else:
            print(f"\n⚠️ Erro na pág {pagina_atual} (Status: {status}). Anotado para resgate.")
            paginas_com_erro.append(pagina_atual)

        # Backup a cada 500 páginas com proteção UTF-8 para não bugar nomes!
        if pagina_atual % 500 == 0:
            pd.DataFrame(lista_jogadores).to_csv("backup_sf6_progresso.csv", index=False, encoding='utf-8-sig')
            
        pagina_atual += 1
        time.sleep(random.uniform(0.15, 0.25))

    # --- 3. OPERAÇÃO RECUPERAÇÃO AUTOMÁTICA ---
    if paginas_com_erro:
        print(f"\n🚑 Iniciando Resgate de {len(paginas_com_erro)} páginas...")
        for pagina in paginas_com_erro:
            jogadores_da_pagina, status = raspar_pagina(pagina)
            if status == 200 and len(jogadores_da_pagina) > 0:
                lista_jogadores.extend(jogadores_da_pagina)
                print(f"✅ Pág {pagina} resgatada!")
            time.sleep(random.uniform(0.15, 0.25))

    # --- 4. SALVAMENTO ---
    if lista_jogadores:
        df_final = pd.DataFrame(lista_jogadores)
        df_final.to_csv("sf6_temporada2_COMPLETO_BRUTO.csv", index=False, encoding='utf-8-sig')
        
        print("\n" + "-" * 30)
        print("📊 RELATÓRIO DE EXTRAÇÃO FINAL")
        print("-" * 30)
        print(f"Total de registros: {len(df_final):,}".replace(',', '.'))
        print("🏆 Arquivo 'sf6_temporada2_COMPLETO_BRUTO.csv' gerado com sucesso!")
        print("-" * 30)

if __name__ == "__main__":
    main()