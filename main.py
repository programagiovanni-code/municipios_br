import pandas as pd
import requests

def extrair_dicionario_ibge():
    """
    Conecta à API de Localidades do IBGE, extrai a hierarquia de todos os municípios,
    trata anomalias geográficas (nulos e emancipações) e retorna um DataFrame padronizado.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    
    print("Conectando à API do IBGE...")
    try:
        # O timeout garante que o script não trave se o servidor não responder
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
        
    except requests.exceptions.RequestException as erro:
        print(f"Erro fatal na conexão com o IBGE: {erro}")
        return None
        
    print("Conexão estabelecida. Processando dados da malha municipal...")
    dados = response.json()
    lista_cidades = []
    
    for mun in dados:
        micro = mun.get('microrregiao') or {}
        meso = micro.get('mesorregiao') or {}
        uf = meso.get('UF') or {}
        regiao = uf.get('regiao') or {}
        
        imediata = mun.get('regiao-imediata') or {}
        intermediaria = imediata.get('regiao-intermediaria') or {}
        
        lista_cidades.append({
            'Pais': 'Brasil',
            'Região': regiao.get('nome'),
            'Estado': uf.get('nome'),
            'Sigla_estado': uf.get('sigla'),
            'Mesoregião': meso.get('nome'),
            'Região_intermediaria': intermediaria.get('nome'),
            'Microregião': micro.get('nome'),
            'Região_imediata': imediata.get('nome'),
            'Municipios': mun.get('nome')
        })

    df_gabarito = pd.DataFrame(lista_cidades)
    return df_gabarito
    
def limpar_texto_gabarito(df_gabarito):
    """Padronização de strings e correção manual de entidades recentes"""
    colunas_texto = ['Região', 'Estado', 'Mesoregião', 'Região_intermediaria', 'Microregião', 'Região_imediata', 'Municipios']
    for col in colunas_texto:
        df_gabarito[col] = df_gabarito[col].astype(str).str.upper().str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # CORREÇÃO AQUI: Usa o df_gabarito local em vez de chamar a API novamente
    mascara_boa = df_gabarito['Municipios'] == 'BOA ESPERANCA DO NORTE'
    if mascara_boa.any():
        df_gabarito.loc[mascara_boa, 'Região'] = 'CENTRO OESTE'
        df_gabarito.loc[mascara_boa, 'Estado'] = 'MATO GROSSO'
        df_gabarito.loc[mascara_boa, 'Sigla_estado'] = 'MT'
        df_gabarito.loc[mascara_boa, 'Mesoregião'] = 'NORTE MATO-GROSSENSE'
        df_gabarito.loc[mascara_boa, 'Região_intermediaria'] = 'SINOP'
        df_gabarito.loc[mascara_boa, 'Microregião'] = 'ALTO TELES PIRES'
        df_gabarito.loc[mascara_boa, 'Região_imediata'] = 'SORRISO'

    print("Dicionário geográfico processado com sucesso.")
    return df_gabarito

def salvando(df_gabarito):
    escolha = int(input('Escolha o método de salvamento: 1 - parquet | 2 - CSV | 3 - EXCEL: '))
    if escolha == 1:
        df_gabarito.to_parquet('dicionario_municipios_ibge.parquet', index=False)
        print("✅ Arquivo Parquet salvo com sucesso!")    
    elif escolha == 2:
        df_gabarito.to_csv('dicionario_municipios_ibge.csv', index=False, encoding='utf-8-sig')
        print("✅ Arquivo CSV salvo com sucesso!")
    elif escolha == 3:
        df_gabarito.to_excel('dicionario_municipios_ibge.xlsx', index=False)
        print("✅ Arquivo Excel salvo com sucesso!")   
    else:
        print("⚠️ Opção inválida.")
        return # Evita imprimir a mensagem de sucesso se a opção for errada
        
    print("Arquivo criado!")

#------------------------------------------------------------
# Bloco de execução principal (Blindado contra importações)
if __name__ == "__main__":
    df_final = extrair_dicionario_ibge()
    
    # Só continua se a extração (API) não retornou erro
    if df_final is not None:
        df_save = limpar_texto_gabarito(df_final)
        salvando(df_save)