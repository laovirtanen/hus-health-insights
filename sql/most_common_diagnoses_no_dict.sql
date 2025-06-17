

SELECT icd9_code, COUNT(DISTINCT subject_id) AS num_patients
FROM diagnoses_icd
GROUP BY icd9_code
ORDER BY num_patients DESC
LIMIT 10;

-- Tämä kysely hakee 10 yleisintä diagnoosia (ICD-9-koodia) potilaille, jotka on kirjattu diagnoses_icd-tauluun.