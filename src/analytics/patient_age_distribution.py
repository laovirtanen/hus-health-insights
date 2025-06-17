import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# Yhdistetään tietokantaan
engine = create_engine('postgresql://postgres:postgres@localhost:5432/hus_health_insights')

# Haetaan taulut
patients = pd.read_sql('SELECT * FROM patients', engine)

patients['dob'] = pd.to_datetime(patients['dob'])


# Lasketaan potilaiden iät (MIMIC-III:ssa kaikki päivämäärät on anonymisoitu tulevaisuuteen)
analysis_year = 2100 # Jotta edes joidenkin potilaiden ikä olisi realistinen
patients['age'] = analysis_year - patients['dob'].dt.year


# Luodaan diagrammi

plt.figure(figsize=(10,6))
patients['age'].hist(bins=20)
plt.title("Potilaiden ikäjakauma (simuloitu)")
plt.xlabel("Ikä")
plt.ylabel("Potilaita")
plt.tight_layout()
plt.savefig("output/patient_age_distribution.png")
plt.show()