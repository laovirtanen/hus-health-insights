
SELECT gender, COUNT(*) AS num_patients
FROM patients
GROUP BY gender;

