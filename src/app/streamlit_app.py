import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Tietokantayhteys
engine = create_engine('postgresql://postgres:postgres@localhost:5432/hus_health_insights')

st.title("HUS Health Insights – Sairaaladatan tietopalvelu")

# Sivupalkin analyysivalinta
analyysi = st.sidebar.selectbox(
    "Valitse analyysi",
    [
        "Yleisimmät diagnoosit",
        "Potilaiden ikäjakauma",
        "Sairaalakäynnit vuosittain",
        "Yleisimmät laboratoriotestit"
    ]
)

if analyysi == "Yleisimmät diagnoosit":
    st.subheader("Yleisimmät diagnoosit")
    # Ladataan tarvittavat taulut
    admissions = pd.read_sql('SELECT * FROM admissions', engine)
    diagnoses = pd.read_sql('SELECT * FROM diagnoses_icd', engine)
    icd9_dict = pd.read_sql('SELECT * FROM icd9_dict', engine)

    # Lisätään vuosi admissions-tauluun
    admissions['admittime'] = pd.to_datetime(admissions['admittime'])
    admissions['year'] = admissions['admittime'].dt.year

    # Yhdistetään diagnoses ja admissions hadm_id:llä, jotta saadaan mukaan vuosi
    merged = pd.merge(diagnoses, admissions[['hadm_id', 'year']], on='hadm_id', how='left')

    # Filtteri: valitse vuosi (tai "Kaikki")
    years = merged['year'].dropna().unique()
    years.sort()
    year_selected = st.selectbox("Valitse vuosi", options=["Kaikki"] + list(years.astype(int)))

    if year_selected != "Kaikki":
        filtered = merged[merged['year'] == int(year_selected)]
    else:
        filtered = merged

    # Lasketaan top-diagnoses valitulle vuodelle
    top_diagnoses = (
        filtered.groupby('icd9_code')['subject_id']
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .rename(columns={'subject_id': 'num_patients'})
    )
    top_diagnoses = pd.merge(
        top_diagnoses,
        icd9_dict[['icd9_code', 'short_title']],
        on='icd9_code',
        how='left'
    )
    top_diagnoses = top_diagnoses[['icd9_code', 'short_title', 'num_patients']]
    top_diagnoses.columns = ['ICD9-koodi', 'Diagnoosi', 'Potilaita']

    st.dataframe(top_diagnoses)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(top_diagnoses['Diagnoosi'], top_diagnoses['Potilaita'])
    ax.set_xlabel("Diagnoosi")
    ax.set_ylabel("Potilaita")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

elif analyysi == "Potilaiden ikäjakauma":
    st.subheader("Potilaiden ikäjakauma")
    patients = pd.read_sql('SELECT * FROM patients', engine)
    patients['dob'] = pd.to_datetime(patients['dob'])
    analysis_year = 2100
    patients['age'] = analysis_year - patients['dob'].dt.year
    fig, ax = plt.subplots(figsize=(10,5))
    ax.hist(patients['age'], bins=20)
    ax.set_xlabel("Ikä")
    ax.set_ylabel("Potilaita")
    st.pyplot(fig)

elif analyysi == "Sairaalakäynnit vuosittain":
    st.subheader("Sairaalakäynnit vuosittain")
    admissions = pd.read_sql('SELECT * FROM admissions', engine)
    admissions['admittime'] = pd.to_datetime(admissions['admittime'])
    admissions['year'] = admissions['admittime'].dt.year
    visits_per_year = admissions.groupby('year').size().reset_index(name='admissions')
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(visits_per_year['year'], visits_per_year['admissions'])
    ax.set_xlabel("Vuosi")
    ax.set_ylabel("Käyntejä")
    st.pyplot(fig)

elif analyysi == "Yleisimmät laboratoriotestit":
    st.subheader("Yleisimmät laboratoriotestit")
    labs = pd.read_sql('SELECT * FROM labs', engine)
    lab_dict = pd.read_sql('SELECT * FROM lab_dict', engine)
    top_labs = labs['itemid'].value_counts().head(10).reset_index()
    top_labs.columns = ['itemid', 'num_tests']
    top_labs = pd.merge(
        top_labs,
        lab_dict[['itemid', 'label']],
        on='itemid',
        how='left'
    )
    top_labs = top_labs[['itemid', 'label', 'num_tests']]
    top_labs.columns = ['ItemID', 'Testin nimi', 'Testikertoja']
    st.dataframe(top_labs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(top_labs['Testin nimi'], top_labs['Testikertoja'])
    ax.set_xlabel("Labratesti")
    ax.set_ylabel("Testikertoja")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
