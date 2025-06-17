import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('postgresql://postgres:postgres@localhost:5432/hus_health_insights')
patients = pd.read_sql('SELECT * FROM patients', engine)

gender_counts = patients['gender'].value_counts()

plt.figure(figsize=(7,5))
gender_counts.plot(kind='bar')
plt.title("Potilaiden sukupuolijakauma")
plt.xlabel("Sukupuoli")
plt.ylabel("Potilaita")
plt.tight_layout()
plt.savefig("output/patient_gender_distribution.png")
plt.show()
