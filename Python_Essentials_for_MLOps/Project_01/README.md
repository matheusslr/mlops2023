# Projeto 01: Sistema de recomendação de filmes

<!-- Shields Exemplo, existem N diferentes shield em https://shields.io/ -->
![GitHub last commit](https://img.shields.io/github/last-commit/matheusslr/mlops2023)
![GitHub language count](https://img.shields.io/github/languages/count/matheusslr/mlops2023)
![Github repo size](https://img.shields.io/github/repo-size/matheusslr/mlops2023)
![Github stars](https://img.shields.io/github/stars/matheusslr/mlops2023?style=social)

![Capa do Projeto](https://www.fatosdesconhecidos.com.br/wp-content/uploads/2022/03/interestelar-07-1920x1080.jpg)

> Neste projeto, foi criado um sistema interativo de recomendação de filmes que permite que você digite o nome de um filme e receba imediatamente dez recomendações de outros filmes que talvez queira assistir

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter as seguintes dependências instaladas:

- Python: 3.8+
    - ipywidgets: 8.1.1
    - numpy: 1.24.3
    - pandas: 2.0.3
    - pytest: 7.4.2
    - scipy: 1.11.2
    - scikit-learn: 1.2.2

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
python .\movie_recommendations.py
```

### Execute os testes

```bash
pytest .\movie_recommendations_test.py
```

## Estrutura de Pastas

A estrutura de pastas do projeto é organizada da seguinte maneira:

```text
/
|-- Project_01/
|   |-- movie_recommendations.py
|   |-- movie_recommendations_test.py
|   |-- exceptions/
|   |   |-- ResourceNotFound.py
|   |-- util/
|   |   |-- data_util.py
|-- ...
```

## Referências

- [Build a Movie Recommendation System in Python - Dataquest](https://github.com/dataquestio/project-walkthroughs/tree/master/movie_recs)