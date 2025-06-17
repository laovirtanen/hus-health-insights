

SELECT d.icd9_code, s.short_title AS diagnosis_name, COUNT(DISTINCT d.subject_id) AS num_patients
FROM diagnoses_icd d
LEFT JOIN icd9_dict s ON d.icd9_code = s.icd9_code
GROUP BY d.icd9_code, s.short_title
ORDER BY num_patients DESC
LIMIT 10;


-- Tämä kysely hakee 10 yleisintä diagnoosia (ICD-9-koodia) potilaille, jotka on kirjattu diagnoses_icd-tauluun.