WITH cte_null AS(
SELECT
	COUNT(*) "rows", event_date "evtime"
FROM myschema.mytable 
WHERE count_null_rows_field IS NULL
	AND event_date BETWEEN '2021-11-04' AND '2021-11-08'
GROUP BY 2
), cte_not_null AS(
SELECT 
	COUNT(*) "rows", event_date "evtime"
FROM myschema.mytable
WHERE count_not_null_rows_field IS NOT NULL
	AND event_date BETWEEN '2021-11-04' AND '2021-11-08'
GROUP BY 2
), cte_all AS(
SELECT
	COUNT(*) "rows", event_date "evtime"
FROM myschema.mytable 
	WHERE event_date BETWEEN '2021-11-04' AND '2021-11-08'
GROUP BY 2
) SELECT 
	cn.rows "null_rows",
	cnn.rows "not_null_rows",
	ca.rows "total_rows",
	round((cn.rows::decimal * 100::decimal)/ca.rows::decimal,2) "%null_rows",
	round((cnn.rows::decimal * 100::decimal)/ca.rows::decimal,2) "%not_null_rows",
	ca.evtime "event_time"
FROM cte_null cn
JOIN cte_not_null cnn
	ON cn.evtime = cnn.evtime
JOIN cte_all ca
	ON cn.evtime = ca.evtime
ORDER BY ca.evtime DESC;
