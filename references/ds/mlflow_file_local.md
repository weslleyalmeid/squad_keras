Para permitir a escrita do Client mlflow na pasta central do volume do container é necessário
```
sudo chmod 777 -R ./mlruns
```



tips: sqlite
```
Valid SQLite URL forms are:
 sqlite:///:memory: (or, sqlite://)
 sqlite:///relative/path/to/file.db
 sqlite:////absolute/path/to/file.db
```