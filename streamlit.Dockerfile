FROM python:3.9 AS keras_streamlit

WORKDIR /streamlit

ENV VIRTUAL_ENV=.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./app.py ./
COPY ./src/utils.py ./src/utils.py
COPY ./models ./models
COPY ./requirements-dev.txt ./

RUN pip3 install --upgrade pip && pip3 install -r requirements-dev.txt

VOLUME ./data
VOLUME ./mlruns