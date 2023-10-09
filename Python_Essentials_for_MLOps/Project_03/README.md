# Projeto 03: Web Scraping de jogos de futebol da English Premier League (EPL) em Python

<!-- Shields Exemplo, existem N diferentes shield em https://shields.io/ -->
![GitHub last commit](https://img.shields.io/github/last-commit/matheusslr/mlops2023)
![GitHub language count](https://img.shields.io/github/languages/count/matheusslr/mlops2023)
![Github repo size](https://img.shields.io/github/repo-size/matheusslr/mlops2023)
![Github stars](https://img.shields.io/github/stars/matheusslr/mlops2023?style=social)

![Capa do Projeto](https://theanalyst.com/wp-content/uploads/2022/06/epl-sir-analyst-banner.jpg)

> Neste projeto, empregaremos técnicas de web scraping para extrair as informações essenciais sobre os resultados dos jogos da EPL. Em seguida, importaremos esses dados para o pandas, organizando-os em uma tabela limpa e pronta para ser utilizada no contexto de aprendizado de máquina.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter as seguintes dependências instaladas:

- Python: 3.8+
    - beautifulsoup4: 4.12.2
    - pandas: 2.0.3
    - html5lib: 1.1

## Como executar o projeto

Siga as etapas abaixo para executar o projeto em sua máquina local:

Execute os seguintes comandos a partir da pasta raiz do projeto:

### Clone este repositório

```bash
git clone https://github.com/matheusslr/mlops2023
```

Este link pode ser encontrado no botão verde acima `Code`.

### Instale as dependências

```bash
pip install -r requirements.txt
```

### Execute o Projeto

```bash
python .\scraping.py
```

### Execute os testes

```bash
pytest .\scraping_tests.py
```

## Estrutura de Pastas

A estrutura de pastas do projeto é organizada da seguinte maneira:

```text
/
|-- Project_03/
|   |-- scraping.py
|   |-- scraping_tests.py
|   |-- requirements.txt
|-- ...
```

## Referências

- [Web Scraping Football Matches From The EPL in Python - Dataquest](https://github.com/dataquestio/project-walkthroughs/tree/master/football_matches)
- [FBREF - Premier League Stats](https://fbref.com/en/comps/9/Premier-League-Stats)