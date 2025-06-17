

SELECT EXTRACT(YEAR FROM admittime) AS year, COUNT(*) AS admissions
FROM admissions
GROUP BY year
ORDER BY year;
-- Tämä kysely hakee potilaiden sairaalahoitojen lukumäärän vuosittain.