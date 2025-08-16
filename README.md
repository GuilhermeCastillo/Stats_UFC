# UFC Stats ETL & Analytics

## Objetivo do Projeto

O objetivo deste projeto é construir um **pipeline de ETL** completo utilizando dados públicos do site [UFC Stats](http://ufcstats.com). Através deste pipeline, busco:

- **Extrair** informações detalhadas de eventos e lutas de MMA, incluindo lutadores, resultados, métodos de vitória e estatísticas de combate.
- **Transformar** os dados brutos em tabelas normalizadas, prontas para análise, usando **DuckDB** para limpeza, padronização e criação de chaves relacionais.
- **Carregar** os dados transformados em um banco de dados relacional ( **PostgreSQL** ) para consultas, análises e dashboards.

Este projeto tem como finalidade:

1. **Treinar habilidades de engenharia de dados** : web scraping, transformação de dados, modelagem relacional e carregamento em banco.
2. **Aprender e praticar SQL** em contexto real, com dados estruturados para análise.
3. **Construir um portfólio robusto** para futuras entrevistas, demonstrando a capacidade de extrair, transformar e analisar dados de fontes externas.
4. **Gerar insights de performance de lutadores** para análises estatísticas, gráficos e dashboards futuros.

---

## Tecnologias e Ferramentas Utilizadas

- **Python** : para scraping, transformação e manipulação de dados.
- **BeautifulSoup & Requests** : para coleta de dados do site UFC Stats.
- **DuckDB** : para transformação e normalização de dados de forma eficiente localmente.
- **PostgreSQL** : para armazenamento final e consultas analíticas.
- **Pandas** : manipulação e limpeza de dados intermediários.
- **TQDM** : monitoramento de progresso em loops longos.
