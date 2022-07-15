FROM python:3.9 AS mlflow

ENV VIRTUAL_ENV=.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip && pip3 install mlflow==1.27.0

RUN mkdir ./mlruns
RUN chmod 777 -R ./mlruns

VOLUME ./mlruns


FROM python:3.9 AS streamlit

WORKDIR /streamlit

ENV VIRTUAL_ENV=.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./app.py ./
COPY ./src/utils.py ./src/utils.py
COPY ./models ./models
COPY requirements-dev.txt ./


RUN pip3 install --upgrade pip && pip3 install -r requirements-dev.txt

EXPOSE 8501
VOLUME ./data