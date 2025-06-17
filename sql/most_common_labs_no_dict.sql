

SELECT itemid, COUNT(*) AS num_tests
FROM labs
GROUP BY itemid
ORDER BY num_tests DESC
LIMIT 10;
-- Tämä kysely hakee 10 yleisintä laboratoriotestiä