import pandas as pd
import os.path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_auc_score, recall_score, f1_score
import mlflow
import ipdb
from mlflow.models.signature import infer_signature
from google.cloud import bigquery

MODEL_DIR = os.path.join( os.path.abspath('.') )
MODEL_DIR = os.path.dirname( os.path.abspath(__file__) )
SRC_DIR = os.path.dirname(MODEL_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
DATA_DIR = os.path.join(ROOT_DIR, 'data', '{folder}')
SECRETS_DIR = os.path.join(ROOT_DIR, 'secrets')

  
def initial_data(foldername:str, filename:str, cloud=True, first_run=False) -> pd.DataFrame:

    if cloud:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(SECRETS_DIR, 'keras-356322-76c4c7c6a3ee.json')
        query = f"""
            SELECT * FROM `keras-356322.credit_fraud.raw_data`
        """
        df = bigquery.Client().query(query).to_dataframe()
        col_float = df.select_dtypes(include=['float64']).columns
        col_int = df.select_dtypes(include=['int64']).columns
        df[col_float] = df[col_float].astype('float64')
        df[col_int] = df[col_int].astype('int64')

    else:
        data_file = os.path.join(DATA_DIR.format(folder=foldername), filename)
        df = pd.read_csv(data_file)
    
    df.columns = df.columns.str.lower()
    smote = SMOTE(sampling_strategy=0.4, random_state=42)

    if first_run:
        df_fraud = df.loc[df['class'] == 1].sample(2).drop(['class'], axis=1)
        df_legal = df.loc[df['class'] == 0].sample(998).drop(['class'], axis=1)


        df_sample = pd.concat([df_fraud, df_legal], ignore_index=True)
        filename_aux = os.path.join(DATA_DIR.format(folder='processed'), 'sample.csv')
        df_sample.to_csv(filename_aux, index=False)

        # garantindo dados para teste sem vazamento
        df.drop(df_fraud.index, axis=0, inplace=True)
        df.drop(df_legal.index, axis=0, inplace=True)
        filename_aux = os.path.join(DATA_DIR.format(folder='external'), 'creditcard.csv')
        df = df.reset_index(drop=True)
        df.to_csv(filename_aux, index=False)


    X = df.drop(labels=['class'], axis=1)
    y = df['class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    X_res, y_res = smote.fit_resample(X_train, y_train)
    return X_res, X_test, y_res, y_test

def upgrade_stage(roc_auc, recall, f1, uri, name_registry, name_experiment):
    
    # aqui pega o modelo ja no tracking
    client = mlflow.tracking.MlflowClient(tracking_uri=uri)

    # pegar o id do experimento por nome do projeto
    id_experiment = client.get_experiment_by_name(name_experiment).experiment_id


    for mv in client.search_model_versions(f"name='{name_registry}'"):

        if mv.current_stage == 'Production':
            # pegar o id de execucao do experimento que esta em producao
            id_run = mv.run_id
            
            # runs vai receber um dataframe com os valores do experimento para todos os experimentos
            runs = mlflow.search_runs(experiment_ids=id_experiment)
            df_experiment = runs[runs['run_id'] == id_run]         

            roc_auc_old = float(df_experiment['metrics.roc_auc'].values)
            recall_old = float(df_experiment['metrics.recall'].values)
            f1_old = float(df_experiment['metrics.f1_score'].values)

            if roc_auc > roc_auc_old and recall > recall_old and f1 > f1_old:
                return 'Production'
            else:
                return None
        
    return 'Production'


def model_registry(roc_auc, recall, f1, name_registry, name_experiment):

    promoved = upgrade_stage(roc_auc, recall, f1, uri, name_registry, name_experiment)
    if promoved:
        client = mlflow.tracking.MlflowClient(tracking_uri=uri)


        version = client.get_latest_versions(name_registry)[-1]
        current_version = version.version

        client.transition_model_version_stage(
            name=name_registry,
            version=current_version,
            stage="Production",
            archive_existing_versions=True
        )

        return 'Model in Production'

    return 'Refused model in Production'

def train_model(X_train, y_train):
    model = RandomForestClassifier(max_depth=4, min_samples_leaf=3, verbose=2, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    return model


def mlflow_tracking(name_experiment:str, uri:str, model_name:str, X_train, X_test, y_train, y_test):
    mlflow.set_tracking_uri(uri)
    mlflow.set_experiment(name_experiment)

    with mlflow.start_run():
        name_registry = f'model_{model_name}'
        mlflow.sklearn.autolog(registered_model_name=name_registry)
        
        
        model = train_model(X_train, y_train)

        y_pred = model.predict(X_test)

        roc_auc = roc_auc_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_metric('roc_auc', roc_auc)
        mlflow.log_metric('recall', recall)
        mlflow.log_metric('f1_score', f1)


        signature = infer_signature(X_test, y_pred)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=name_registry,
            registered_model_name=name_registry,
            signature=signature,
        )

        return roc_auc, recall, f1, name_registry


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(SECRETS_DIR, 'keras-356322-76c4c7c6a3ee.json')
    
    X_train, X_test, y_train, y_test = initial_data(foldername='external', filename='creditcard.csv', cloud=False, first_run=True)

    name_experiment = "fraud_detection"
    # uri = "http://172.18.0.2:5000"
    uri = "https://keras-fraud-detection.herokuapp.com/"
    model_name = 'clf'

    roc_auc, recall, f1, name_registry = mlflow_tracking(name_experiment, uri, model_name, X_train, X_test, y_train, y_test)

    model_registry(roc_auc, recall, f1, name_registry, name_experiment)