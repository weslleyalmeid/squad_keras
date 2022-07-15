# pip install google-bigquery==3.2.0
# pip install db-dtypes

import pandas as pd
from google.cloud import bigquery
import os
import ipdb
import yaml
from datetime import datetime

# # load yml file to dictionary
# credentials = yaml.load(open('credentials.yml'))
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials['env_variables']['SECRET_GCP']

# LEITURA
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.abspath('.'), 'secrets/keras-356322-76c4c7c6a3ee.json')


query = f"""
SELECT * FROM `keras-356322.credit_fraud.raw_data`
LIMIT 5
"""

df =  bigquery.Client().query(query).to_dataframe()
df['dt_arquivo'] = datetime.today().date()


# ESCRITA
client = bigquery.Client()


job_config = bigquery.LoadJobConfig(
    schema = [
        bigquery.SchemaField('Time','float64'),
        bigquery.SchemaField('V1','float64'),
        bigquery.SchemaField('V2','float64'),
        bigquery.SchemaField('V3','float64'),
        bigquery.SchemaField('V4','float64'),
        bigquery.SchemaField('V5','float64'),
        bigquery.SchemaField('V6','float64'),
        bigquery.SchemaField('V7','float64'),
        bigquery.SchemaField('V8','float64'),
        bigquery.SchemaField('V9','float64'),
        bigquery.SchemaField('V10','float64'),
        bigquery.SchemaField('V11','float64'),
        bigquery.SchemaField('V12','float64'),
        bigquery.SchemaField('V13','float64'),
        bigquery.SchemaField('V14','float64'),
        bigquery.SchemaField('V15','float64'),
        bigquery.SchemaField('V16','float64'),
        bigquery.SchemaField('V17','float64'),
        bigquery.SchemaField('V18','float64'),
        bigquery.SchemaField('V19','float64'),
        bigquery.SchemaField('V20','float64'),
        bigquery.SchemaField('V21','float64'),
        bigquery.SchemaField('V22','float64'),
        bigquery.SchemaField('V23','float64'),
        bigquery.SchemaField('V24','float64'),
        bigquery.SchemaField('V25','float64'),
        bigquery.SchemaField('V26','float64'),
        bigquery.SchemaField('V27','float64'),
        bigquery.SchemaField('V28','float64'),
        bigquery.SchemaField('Amount','float64'),
        bigquery.SchemaField('Class','Int64'),
        bigquery.SchemaField('dt_arquivo', bigquery.enums.SqlTypeNames.DATE)
    ],
    time_partitioning = bigquery.TimePartitioning(field='dt_arquivo'),
    # write_disposition = 'WRITE_APPEND'
    write_disposition = 'WRITE_TRUNCATE'
)


table_id = 'keras-356322.credit_fraud.stremlit_data'
job = client.load_table_from_dataframe(
    df, table_id, job_config=job_config    
)

job.result()  # Wait for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)