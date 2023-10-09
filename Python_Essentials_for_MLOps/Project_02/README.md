# Projeto 02: Um pipeline de dados de Airflow para fazer download de podcasts

<!-- Shields Exemplo, existem N diferentes shield em https://shields.io/ -->
![GitHub last commit](https://img.shields.io/github/last-commit/matheusslr/mlops2023)
![GitHub language count](https://img.shields.io/github/languages/count/matheusslr/mlops2023)
![Github repo size](https://img.shields.io/github/repo-size/matheusslr/mlops2023)
![Github stars](https://img.shields.io/github/stars/matheusslr/mlops2023?style=social)

![Capa do Projeto](imgs\airflow.jpg)

> Neste projeto, foi criado um pipeline de dados de quatro etapas usando o Airflow, uma popular ferramenta em Python para definir e executar pipelines de dados avançados. O pipeline fez o download de episódios de podcast e os armazenou em um banco de dados SQLite para consulta.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter as seguintes dependências instaladas:

- Python: 3.8+
    - apache-airflow: 2.3+
    - pandas: 2.0.3
    - pydub: 0.25.1
    - pytest: 7.4.2
    - vosk: 0.3.45
    - xmltodict: 0.13.0
- Docker
- Sqlite3

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
python .\dags\podcast_summary.py
```

Alternativamente, você pode rodar o projeto com:
```bash
docker-compose up
```

o Airflow será iniciado na instância ``localhost:8080``

## Estrutura de Pastas

A estrutura de pastas do projeto é organizada da seguinte maneira:

```text
/
|-- Project_02/
|   |-- dags/
|   |   |-- podcast_summary.py
|   |-- tests/
|   |   |-- podcast_summary_test.py
|   |   |-- base_functions/
|   |   |   |-- podcast_functions.py
|   |-- docker-compose.yml
|   |-- Dockerfile
|-- ...
```

## Referências

- [Build an Airflow Data Pipeline to Download Podcasts - Dataquest](https://github.com/dataquestio/project-walkthroughs/tree/master/podcast_summary)
- [Sqlite3 download page](https://www.sqlite.org/download.html)
- [Install Docker Engine](https://docs.docker.com/engine/install/)
- [Airflow docker-compose.yml](https://airflow.apache.org/docs/apache-airflow/2.7.1/docker-compose.yaml)