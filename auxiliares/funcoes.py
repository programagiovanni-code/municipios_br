import pandas as pd

def analise_dados(df):
    '''Investiga dados nulos, unicos e duplicados e sua distribuição no DataFrame'''
    tabela_resumo = pd.DataFrame({
        'Tipos de Dados': df.dtypes,        
        'Qtd_Não_Nulos': df.notna().sum(),
        'Valores Únicos': df.nunique(), 
        'Qtd_Nulos': df.isna().sum(),
        '% Nulos': ((df.isna().sum()) / len(df) * 100).round(2).astype(str) + '%', 
        'Duplicados': df.duplicated().sum()
    })

    return tabela_resumo

def resumo_estatistico(df):
    resumo_completo = df.describe(include='all').round(2)
    resumo_completo = resumo_completo.fillna('-')

    return resumo_completo

def contagem_valores(df):
    '''Checagem de valores unicos, suas proporções e formatação'''
    print("--- RELATÓRIO DE VALORES ÚNICOS E CONTAGENS ---")
    for column in df.columns:
        # Se todos os valores forem únicos (ex: IDs), ele omite para não travar a tela
        if df[column].nunique() == len(df[column]):
            print(f"\n[ {column.upper()} ] -> {df[column].nunique()} valores únicos. (Omitido)")
            continue 
            
        # AQUI ESTÁ A CORREÇÃO: Mostrando o total de valores únicos da coluna
        print(f"\n[ {column.upper()} ] -> {df[column].nunique()} valores únicos")
        
        textos_itens = [f"'{chave}' ({len(str(chave))} caracteres): {valor}" for chave, valor in df[column].value_counts().items()]
        
        tamanho_bloco = 3
        for i in range(0, len(textos_itens), tamanho_bloco):
            pedaco = textos_itens[i : i + tamanho_bloco]
            print("  |  ".join(pedaco))
            