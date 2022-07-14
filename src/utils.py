from csv import excel
import pandas as pd
import numpy as np
import time
import plotly.express as px
import ipdb
import mlflow
import os.path
from sqlalchemy import create_engine

class Utils():

    def __init__(self):
        self.SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.SRC_DIR)
        self.MODELS_DIR = os.path.join( self.ROOT_DIR, 'models')
        self.DATA_DIR = os.path.join(self.ROOT_DIR, 'data', '{folder}')
        self.DB_DIR = os.path.join(self.DATA_DIR.format(folder='interim'), 'tmp.db')

        self.engine = create_engine(f'sqlite:///{self.DB_DIR}', echo=False)

    def save_db(self, df):
        print('estou em save')
        ipdb.set_trace
        try:
            df.to_sql('data_stream', con=self.engine, if_exists='append')
            print('sucess')
        except:
            print('error')

    def read_file(self, file):
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()
            return df

        except:
            df = pd.read_excel(file)
            df.columns = df.columns.str.lower()
            return df

    def get_model(self, text:str, params:dict):

        if 'local' in text:
            name = 'Local'
            model = pd.read_pickle( os.path.join(self.MODELS_DIR, "modelRF.pkl") )
            features = model['features'].str.lower()
            model = model['model']

            return model, features, name


        elif 'mlflow' in text:
            name = 'MLFlow'
            uri = params['uri']
            name_registry = params['name_registry']
            name_experiment = params['name_registry']

            client = mlflow.tracking.MlflowClient(tracking_uri=uri)
            model_production = client.get_latest_versions(name=name_registry, stages=['production'])[0]
            model = mlflow.sklearn.load_model(model_production.source)
            features = model.feature_names_in_
        
            return model, features, name

        