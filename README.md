# Detecção de fraude em cartão de crédito
==============================


Projeto desenvolvido como resolução do desafio proposto pela equipe do [Stack Labs](https://stacktecnologias.com.br/cursos/)

## Integrantes

**Engenharia de Dados**

[Bianca de Moura Pasetto](https://www.linkedin.com/in/biancamk)

[Enzo  Niro](https://www.linkedin.com/in/enzo-niro-59a11537)

**Ciência de Dados**

[Marco Craveiro](https://www.linkedin.com/in/marco-craveiro-ab577310)

[Weslley Almeida](https://www.linkedin.com/in/weslleyalmeid)

## Etapas de desenvolvimento
<details>
<summary>Preparar o ambiente</summary>

```sh
git clone https://github.com/weslleyalmeid/squad_keras.git
cd squad_keras

# criar ambiente virtual python==3.9
python -m venv .venv_keras

# ativar ambiente virtual
# unix
source .venv_keras/bin/activate
# windows
.venv_keras/Scripts/activate

# instalar requisitos
pip install -r requirements.txt
```
Pronto, o ambiente está pronto para iniciar o desenvolvimento.
</details>


<details>
<summary>Execução em ambiente local</summary>

O Dataset utilizado para treinamento é o [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

Nota: As credenciais e caminhos do GCP devem ser personalizados pelo usuário

**Credenciais**
```bash
# na raiz do projeto crie a pasta secrets e adicione suas chaves ou utilize o export
mkdir secrets
```

**Execução do pipeline**
```sh
# construindo as imagens do mlflow e streamlit
docker-compose build mlflow
docker-compose build streamlit

# executando ambos os containers
docker-compose up mlflow
docker-compose up streamlit

# quando executar a primeira vez, lembre-se de first_run em train_moedl para True para retirar amostra
# executando o treinamento do modelo
python src/models/train_model.py

# talvez seja nessário habilitar escrita no volume compartilhado
sudo chmod 777 -R ./mlruns
```
Pronto, o ambiente está pronto para iniciar o desenvolvimento.
</details>




<details>
<summary>Deploy Streamlit</summary>

Para deploy do app streamlit foi utilizado o [Streamlit Cloud](https://streamlit.io/cloud)

Nota: As credenciais da GCP devem ser adicionandos no secrets do app no settings

```md
- Faça o upload do app no github
- Em Streamlit Cloud clique em New app
- Víncule o repositório e a branch
- Clique em configuração avançadas, selecione python 3.9
- Adicione as credencias em formato toml
      ```toml
      [name_key]
      key = value
      ```
- Clique em Deploy e aguarde, em alguns minutos o app estará disponível.
```
</details>


<details>
<summary>Deploy MlFlow</summary>

Para deploy do MLFlow foi utilizado o [Heroku](https://www.heroku.com/), por isso, garanta que você esteja cadastrado

```sh
heroku login

heroku container:login

# heroku create name_app
heroku create keras-fraud-detection

# construindo e checando se tudo certo com a imagem e container local
# observe que o Dockerfile.web é o streamlit.Dockerfile porém com alguns ajustes específicos para o Heroku
docker image build -t my_mlflow:1.0 -f Dockerfile.web .
docker container run -d --name my_mlflow my_mlflow:1.0

# --recursive para encontrar o Dockerfile.web
heroku container:push web --recursive --app keras-fraud-detection

heroku container:release web --app keras-fraud-detection

heroku open --app keras-fraud-detection
```

A maior parte dos problemas foram por conta da falta de conexão entre o \$PORT dinâmico do Heroku, assim, foi necessário especificar o $PORT no CMD do dockerfile e também no UI do [Procfile](https://github.com/weslleyalmeid/squad_keras/blob/main/Procfile)

```docker
CMD mlflow server --backend-store-uri ${BACKEND_URI} --serve-artifacts --artifacts-destination ${ARTIFACTS_DESTINATION} --host 0.0.0.0 -p ${PORT}
```

```Procfile
web: mlflow ui -p $PORT --host 0.0.0.0
```

Vale ressaltar que o Heroku requer nomes padrões para os dockerfiles, por padrão requer um Dockerfile.web ou Dockerfile.worker ou o próprio Dockerfile.
</details>

## Link do deploy

[Data APP - Fraud Detection](https://weslleyalmeid-squad-keras-app-560pwk.streamlitapp.com/)

[Dados test](https://github.com/weslleyalmeid/squad_keras/tree/main/data_test)

[Demo - Squad Keras [Stack Labs 2022.2] - Credit Card Fraud Detection](https://youtu.be/-Rs4DqrCFvU)

## Estrutura dos diretórios
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
    ├── secrets             <- Adicione suas credenciais .env, .json ou .yaml
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