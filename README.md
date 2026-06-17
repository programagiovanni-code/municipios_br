# ETL - Dicionário Geográfico Brasileiro (IBGE)

Pipeline de dados desenvolvido em Python para extração, tratamento e consolidação da hierarquia regional brasileira. 

Este projeto cria uma base de dados unificada que mapeia todos os 5.570 municípios do Brasil, conectando a divisão regional histórica (Mesorregiões e Microrregiões) com a divisão regional moderna (Regiões Intermediárias e Imediatas), solucionando problemas comuns de cruzamento de dados governamentais e financeiros.

## O Problema

Bases de dados públicas e privadas no Brasil frequentemente divergem no formato de localização. Planilhas anteriores a 2017 utilizam o sistema de Meso/Microrregiões, enquanto sistemas recentes utilizam Regiões Intermediárias/Imediatas. Além disso, bibliotecas geográficas comuns (como o geobr) dependem de servidores instáveis para retornar metadados simples, quebrando pipelines de dados.

## A Solução

Este script contorna bibliotecas de terceiros e consome diretamente a API de Localidades do IBGE. Ele extrai a árvore genealógica completa de cada município e gera um dicionário estático consolidado, otimizado para operações de merge em análises de dados.

### Desafios Técnicos Resolvidos

* **Estabilidade de Pipeline:** Substituição de chamadas a shapefiles pesados e servidores instáveis (IPEA) por requisições leves via API RESTful do IBGE.
* **Atualizações Legislativas Restritas:** Inserção manual e mapeamento hierárquico de emancipações recentes (ex: Boa Esperança do Norte - MT, criado no final de 2023 e ainda não totalmente indexado na malha do IBGE).
* **Data Quality e Padronização:** Aplicação de rotinas de limpeza via Pandas (remoção de acentos via NFKD, padronização em maiúsculas e remoção de espaços invisíveis) para garantir chaves primárias à prova de falhas durante cruzamentos de tabelas.
* **Prevenção de Colisão:** Estruturação da base para evitar erros de agregação com municípios homônimos (cidades com o mesmo nome em estados diferentes).

## Tecnologias Utilizadas

* **Python:** Orquestração do script.
* **Pandas:** Manipulação de DataFrames, tratamento de strings e tipagem.
* **Requests:** Consumo da API do IBGE.
* **PyArrow/Fastparquet:** Exportação colunar otimizada.

## Como Utilizar

O script principal exporta o dicionário consolidado em três formatos para diferentes casos de uso:
1.  `.parquet`: Formato colunar de alta performance para pipelines em Python/Pandas.
2.  `.csv` (UTF-8): Formato universal para bancos de dados.
3.  `.xlsx`: Formato de visualização rápida para áreas de negócio.