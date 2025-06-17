import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('postgresql://postgres:postgres@localhost:5432/hus_health_insights')
labs = pd.read_sql('SELECT * FROM labs', engine)
lab_dict = pd.read_sql('SELECT * FROM lab_dict', engine)

# Lasketaan yleisimmät laboratoriotestit
top_labs = labs['itemid'].value_counts().head(10).reset_index()
top_labs.columns = ['itemid', 'num_tests']

# Yhdistetään laboratoriotestien nimet
top_labs = pd.merge(
    top_labs,
    lab_dict[['itemid', 'label']],
    on='itemid',
    how='left'
)

# Järjestetään sarakkeet
top_labs = top_labs[['itemid', 'label', 'num_tests']]
top_labs.columns = ['ItemID', 'Testin nimi', 'Testikertoja']

plt.figure(figsize=(12,6))
plt.bar(top_labs['Testin nimi'], top_labs['Testikertoja'])
plt.title("10 yleisintä laboratoriotestiä")
plt.xlabel("Labratesti")
plt.ylabel("Testikertoja")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("output/most_common_labs_with_names.png")
plt.show()
