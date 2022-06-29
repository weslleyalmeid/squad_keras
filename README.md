Detecção de fraude em cartão de crédito
==============================


## Preparar o ambiente

**Clonar repositório**
```sh
# ssh
git clone git@github.com:weslleyalmeid/squad_keras.git

# https
git clone https://github.com/weslleyalmeid/squad_keras.git
```

Dentro da pasta que foi clonada *squad_keras* inicie a preparação do ambiente
```
cd squad_keras
```

**Criar e ativar ambiente virtual**
```sh
# criar ambiente virtual python==3.9
python -m venv .venv_keras

# ativar ambiente virtual
# unix
source .venv_keras/bin/activate
# windows
.venv_keras/Scripts/activate
```

**Instalar bibliotecas**
```sh
pip install -r requirements.txt
```

Pronto, o ambiente está pronto para iniciar o desenvolvimento.


**Organização do Projeto**
------------

    ├── LICENSE
    ├── Makefile           <- Makefile adicione abstração de comandos para execução
    ├── README.md          <- Explicação do projeto e principais etapas para execução
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Dados intermediários que podem sofrer alterações
    │   ├── processed      <- Dados finais, em perfeito estado para utilização do negócio
    │   └── raw            <- Dados em seu formato original
    │
    ├── models             <- Modelos serializados(joblib, pikle)
    │
    ├── notebooks          <- Jupyter notebooks. Por convensão adicionar número e funcionalidade (ex.: 01 - Exploração dos dados)
    │
    ├── references         <- Materiais de apoio e referências
    │
    ├── reports            <- Análises em HTML, PDF, LaTeX, etc.
    │   └── figures        <- Imagens utilizadas nos reports
    │
    ├── requirements.txt   <- Requisitos para preparação do ambiente
    │                        
    │
    ├── setup.py           <- Para instalar biblioteca local (pip install -e .)
    ├── src                <- Ambiente de codificação.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts para gerar ou realizar o download dos dados
        │   └── make_dataset.py
        │
        ├── features       <- Scripts para transformação dos dados em novas classes
        │   └── build_features.py
        │
        ├── models         <- Scripts para desenvolvimento do treinamento do modelo e predição
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── visualization  <- Scripts para criar visualizações
            └── visualize.py

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>