import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Ladataan ympäristömuuttujat .env-tiedostosta
load_dotenv()


# Määritetään tietokannan yhteysparametrit
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Ladataan CSV-tiedostot
patients = pd.read_csv('data/PATIENTS.csv')
admissions = pd.read_csv('data/ADMISSIONS.csv')
diagnoses_icd = pd.read_csv('data/DIAGNOSES_ICD.csv')
labs = pd.read_csv('data/LABEVENTS.csv')
icd9_dict = pd.read_csv('data/D_ICD_DIAGNOSES.csv')
lab_dict = pd.read_csv("data/D_LABITEMS.csv")


# Luodaan SQLAlchemy-tietokantayhteys
engine = create_engine(DATABASE_URL)

# Muutetaan dataframet SQL-tauluiksi
patients.to_sql('patients', engine, if_exists='replace', index=False)
admissions.to_sql('admissions', engine, if_exists='replace', index=False)
diagnoses_icd.to_sql('diagnoses_icd', engine, if_exists='replace', index=False)
labs.to_sql('labs', engine, if_exists='replace', index=False)
icd9_dict.to_sql('icd9_dict', engine, if_exists='replace', index=False)
lab_dict.to_sql('lab_dict', engine, if_exists='replace', index=False)


print("Data ladattiin onnistuneesti PostgreSQL-tietokantaan.")