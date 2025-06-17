import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# Yhdistetään tietokantaan
engine = create_engine('postgresql://postgres:postgres@localhost:5432/hus_health_insights')

# Ladataan taulut
diagnoses = pd.read_sql('SELECT * FROM diagnoses_icd', engine)
icd9_dict = pd.read_sql('SELECT * FROM icd9_dict', engine)


# Lasketaan yleisimmät diagnoosit
top_diagnoses = (
    diagnoses.groupby('icd9_code')['subject_id']
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
    .rename(columns={'subject_id': 'num_patients'})
)

# Yhdistetään diagnoosin nimi mukaan
top_diagnoses = pd.merge(
    top_diagnoses,
    icd9_dict[['icd9_code', 'short_title']],
    on='icd9_code',
    how='left'
)


# Järjestetään sarakkeet
top_diagnoses = top_diagnoses[['icd9_code', 'short_title', 'num_patients']]
top_diagnoses.columns = ['ICD9-koodi', 'Diagnoosi', 'Potilaita']

print(top_diagnoses)

# Piirretään pylväsdiagrammi
plt.figure(figsize=(12,6))
plt.bar(top_diagnoses['Diagnoosi'], top_diagnoses['Potilaita'])
plt.title("10 yleisintä diagnoosia (potilasmäärä)")
plt.xlabel("Diagnoosi")
plt.ylabel("Potilaita")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("output/most_common_diagnoses_with_names.png")
plt.show()
