- criar app
```sh
heroku login

heroku container:login

# heroku create name_app
heroku create keras-fraud-detection

# construindo e checando se tudo certo com a imagem e container local
docker image build -t my_mlflow:1.0 -f Dockerfile.web .
docker container run -d --name my_mlflow my_mlflow:1.0

# --recursive para encontrar o Dockerfile.web
heroku container:push web --recursive --app keras-fraud-detection

heroku container:release web --app keras-fraud-detection

heroku open --app keras-fraud-detection
```

A maior parte dos problemas foram por conta da falta de conexão entre o \$PORT dinâmico do Heroku, add, foi necessário especificar o $PORT no CMD do dockerfile e também no UI do Procfile

```docker
CMD mlflow server --backend-store-uri ${BACKEND_URI} --serve-artifacts --artifacts-destination ${ARTIFACTS_DESTINATION} --host 0.0.0.0 -p ${PORT}
```

```Procfile
web: mlflow ui -p $PORT --host 0.0.0.0
```

Vale ressaltar que o Heroku requer nomes padrões para os dockerfiles, por padrão requer um Dockerfile.web ou Dockerfile.worker ou o próprio Dockerfile.
