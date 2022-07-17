import pandas as pd
import ipdb
import mlflow
import os.path
from sqlalchemy import create_engine
from google.cloud import bigquery

class Utils():

    def __init__(self):
        self.SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.SRC_DIR)
        self.MODELS_DIR = os.path.join( self.ROOT_DIR, 'models')
        self.DATA_DIR = os.path.join(self.ROOT_DIR, 'data', '{folder}')
        self.DB_DIR = os.path.join(self.DATA_DIR.format(folder='interim'), 'predict.db')
        self.SECRETS = os.path.join(self.ROOT_DIR, 'secrets')

        self.engine = create_engine(f'sqlite:///{self.DB_DIR}', echo=False)

    def save_db(self, df, cloud=True):
        if cloud:
            try:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(self.SECRETS, 'keras-356322-76c4c7c6a3ee.json')
                client = bigquery.Client()
                job_config = bigquery.LoadJobConfig(
                    schema = [
                        bigquery.SchemaField('class','int64'),
                        bigquery.SchemaField('class_percent_1','float64'),
                        bigquery.SchemaField('class_percent_0','float64'),
                        bigquery.SchemaField('time','float64'),
                        bigquery.SchemaField('v1','float64'),
                        bigquery.SchemaField('v2','float64'),
                        bigquery.SchemaField('v3','float64'),
                        bigquery.SchemaField('v4','float64'),
                        bigquery.SchemaField('v5','float64'),
                        bigquery.SchemaField('v6','float64'),
                        bigquery.SchemaField('v7','float64'),
                        bigquery.SchemaField('v8','float64'),
                        bigquery.SchemaField('v9','float64'),
                        bigquery.SchemaField('v10','float64'),
                        bigquery.SchemaField('v11','float64'),
                        bigquery.SchemaField('v12','float64'),
                        bigquery.SchemaField('v13','float64'),
                        bigquery.SchemaField('v14','float64'),
                        bigquery.SchemaField('v15','float64'),
                        bigquery.SchemaField('v16','float64'),
                        bigquery.SchemaField('v17','float64'),
                        bigquery.SchemaField('v18','float64'),
                        bigquery.SchemaField('v19','float64'),
                        bigquery.SchemaField('v20','float64'),
                        bigquery.SchemaField('v21','float64'),
                        bigquery.SchemaField('v22','float64'),
                        bigquery.SchemaField('v23','float64'),
                        bigquery.SchemaField('v24','float64'),
                        bigquery.SchemaField('v25','float64'),
                        bigquery.SchemaField('v26','float64'),
                        bigquery.SchemaField('v27','float64'),
                        bigquery.SchemaField('v28','float64'),
                        bigquery.SchemaField('amount','float64'),
                        bigquery.SchemaField('model','string'),
                        bigquery.SchemaField('dt_arquivo', bigquery.enums.SqlTypeNames.DATE)
                    ],
                    time_partitioning = bigquery.TimePartitioning(field='dt_arquivo'),
                    # write_disposition = 'WRITE_APPEND'
                    write_disposition = 'WRITE_TRUNCATE'
                )

                table_id = 'keras-356322.credit_fraud.predict'
                job = client.load_table_from_dataframe(
                    df, table_id, job_config=job_config    
                )

                job.result()  # Wait for the job to complete.
                print('Salvo com sucesso')

            except:
                print('Error')
        else:
            try:
                df.to_sql('data_stream', con=self.engine, if_exists='append', index=False)
                print('Salvo com sucesso')
                
            except:
                print('Error')

    def read_file(self, file):
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()
            return df

        except:
            df = pd.read_excel(file)
            df.columns = df.columns.str.lower()
            return df

    def check_features(self, model, features):
        fi = model.feature_importances_
        l = len(features)
        aux = []
        for i in range(0,l):
            print('{:.<20} {:3}'.format(features[i], fi[i]))
            aux.append(features[i])

        importances = pd.Series(data=fi, index=aux)
        return importances.sort_values(ascending=False)

    def get_model(self, text:str, params:dict):

        if 'local' in text:
            name = 'Local'
            model = pd.read_pickle( os.path.join(self.MODELS_DIR, "modelRF.pkl") )

            features = model['features'].str.lower()
            model = model['model']
            importance = self.check_features(model, features)
            return model, features, name, importance


        elif 'mlflow' in text:
            name = 'MLFlow'
            uri = params['uri']
            name_registry = params['name_registry']
            name_experiment = params['name_registry']

            mlflow.set_tracking_uri(uri)
            client = mlflow.tracking.MlflowClient(tracking_uri=uri)
            model_production = client.get_latest_versions(name=name_registry, stages=['production'])[0]
            model = mlflow.sklearn.load_model(model_production.source)
            features = model.feature_names_in_
            importance = self.check_features(model, features)
            return model, features, name, importance

    def get_data_predict(self, cloud=True):
        if cloud:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(self.SECRETS, 'keras-356322-76c4c7c6a3ee.json')
            query = f"""
                SELECT * FROM `keras-356322.credit_fraud.predict`
            """
            return bigquery.Client().query(query).to_dataframe()
        
        return pd.read_sql(sql='SELECT * FROM data_stream', con=self.engine)
        