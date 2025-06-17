import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('postgresql://postgres:postgres@localhost:5432/hus_health_insights')
admissions = pd.read_sql('SELECT * FROM admissions', engine)

admissions['admittime'] = pd.to_datetime(admissions['admittime'])
admissions['year'] = admissions['admittime'].dt.year
visits_per_year = admissions.groupby('year').size()

plt.figure(figsize=(10,6))
visits_per_year.plot(kind='bar')
plt.title("Sairaalakäynnit vuosittain")
plt.xlabel("Vuosi")
plt.ylabel("Käyntejä")
plt.tight_layout()
plt.savefig("output/admissions_per_year.png")
plt.show()
