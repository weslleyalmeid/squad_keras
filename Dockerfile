FROM python:3.9

ENV VIRTUAL_ENV=.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Instalando requirements
RUN pip3 install --upgrade pip && pip3 install mlflow==1.27.0
RUN mkdir ./mlruns
RUN chmod 777 -R ./mlruns

VOLUME ./mlruns