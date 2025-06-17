

SELECT l.itemid, d.label AS test_name, COUNT(*) AS num_tests
FROM labs l
LEFT JOIN lab_dict d ON l.itemid = d.itemid
GROUP BY l.itemid, d.label
ORDER BY num_tests DESC
LIMIT 10;

-- Tämä kysely hakee 10 yleisintä laboratoriotestiä