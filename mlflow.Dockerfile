FROM python:3.9 AS keras_mlflow

ENV VIRTUAL_ENV=.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV MLFLOW_GCS_DEFAULT_TIMEOUT=-1
ENV GOOGLE_APPLICATION_CREDENTIALS=./secrets/keras-356322-76c4c7c6a3ee.json

COPY ./requirements-mlflow.txt ./

RUN pip3 install --upgrade pip && pip3 install -r requirements-mlflow.txt

RUN mkdir ./mlruns
RUN chmod 777 -R ./mlruns

VOLUME ./mlruns
VOLUME ./secrets