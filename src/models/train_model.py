import pandas as pd
import os.path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import pickle
from sklearn.metrics import roc_auc_score


MODEL_DIR = os.path.join( os.path.abspath('.') )
MODEL_DIR = os.path.dirname( os.path.abspath(__file__) )
SRC_DIR = os.path.dirname(MODEL_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
DATA_DIR = os.path.join(ROOT_DIR, 'data', '{folder}')

data_file = os.path.join(DATA_DIR.format(folder='external'), 'creditcard.csv')
df = pd.read_csv(data_file)
df.columns = df.columns.str.lower()

smote = SMOTE(sampling_strategy=0.4, random_state=42)

df_fraud = df.loc[df['class'] == 1].sample(5).drop(['class'], axis=1)
df_legal = df.loc[df['class'] == 0].sample(5).drop(['class'], axis=1)

# garantindo dados para teste sem vazamento
df.drop(df_fraud.index, axis=0, inplace=True)
df.drop(df_legal.index, axis=0, inplace=True)
df_noleakage = pd.concat([df_fraud, df_legal]).reset_index(drop=True)
data_file = os.path.join(DATA_DIR.format(folder='processed'), 'creditcard_test.csv')
df_noleakage.to_csv(data_file ,index=False)

X = df.drop(labels=['class'], axis=1)
y = df['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

X_res, y_res = smote.fit_resample(X_train, y_train)

model = RandomForestClassifier()
model.fit(X_train, y_train)

model = pd.Series( {
    "model":model,
    "features":X.columns }
)

model.to_pickle( os.path.join(MODELS_DIR, 'model.pkl') )