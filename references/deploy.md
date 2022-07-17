- instalar heroku cli
- fazer login
```sh
heroku login
```
- fazer login no heroku container
```sh
heroku container:login
```

- criar app
```sh
# heroku create name_app
heroku create keras-fraud-detection
```

docker image build -t my_mlflow:1.0 -f mlflow.Dockerfile .

docker iage build -t my_mlflow:1.0 -f mlflow.Dockerfile --mount type=volume,source=/secrets,destination=/secrets


docker container run -ti --mount type=volume,src=/secrets,dst=/secrets my_mlflow:1.0


CMD ["sh","-c","mkdir -p ~/my/new/directory/ && cd ~/my/new/directory && touch new.file"]


docker container run -d --name my_mlflow my_mlflow:1.0

CMD ["sh","-c","mlflow server --backend-store-uri ${BACKEND_URI} \
    --serve-artifacts --artifacts-destination ${ARTIFACTS_DESTINATION} \
    --host 0.0.0.0 && cd ~/my/new/directory && touch new.file \ 
    && mlflow models serve -m 'models:/fraud_detection/Production' -p 5002 --env-manager=local"
    ]


