WITH worksheet1
AS (
	SELECT DATE_TRUNC('month', o.ORDER_PURCHASE_TIMESTAMP) AS month
		,ARRAY_AGG(DISTINCT oi.SELLER_ID) AS sellers
		,COUNT(DISTINCT oi.seller_id) AS seller_count
	FROM "TAKE_HOME_CHALLENGE"."ECOMMERCE"."ORDER_ITEMS" oi
	JOIN "TAKE_HOME_CHALLENGE"."ECOMMERCE"."ORDERS" o ON oi.ORDER_ID = o.ORDER_ID
	WHERE YEAR(o.ORDER_PURCHASE_TIMESTAMP) = 2017
	GROUP BY month
	HAVING COUNT(DISTINCT oi.ORDER_ID) >= 25
	ORDER BY month
	)
	,worksheet2
AS (
	WITH weekly_orders AS (
			SELECT DATE_TRUNC('week', o.ORDER_PURCHASE_TIMESTAMP) AS week
				,ARRAY_AGG(DISTINCT oi.SELLER_ID) AS seller
				,COUNT(DISTINCT oi.seller_id) AS seller_count
			FROM "TAKE_HOME_CHALLENGE"."ECOMMERCE"."ORDER_ITEMS" oi
			JOIN "TAKE_HOME_CHALLENGE"."ECOMMERCE"."ORDERS" o ON oi.ORDER_ID = o.ORDER_ID
			WHERE YEAR(o.ORDER_PURCHASE_TIMESTAMP) = 2017
			GROUP BY week
			HAVING COUNT(DISTINCT oi.ORDER_ID) >= 5
			ORDER BY week
			)
	SELECT DATE_TRUNC('month', week) AS month
		,ROUND(AVG(seller_count)) AS avg
	FROM weekly_orders
	GROUP BY DATE_TRUNC('month', week)
	)
	,worksheet3
AS (
	WITH daily_orders AS (
			SELECT DATE_TRUNC('day', o.ORDER_PURCHASE_TIMESTAMP) AS day
				,ARRAY_AGG(DISTINCT oi.SELLER_ID) AS seller
				,COUNT(DISTINCT oi.seller_id) AS seller_count
			FROM "TAKE_HOME_CHALLENGE"."ECOMMERCE"."ORDER_ITEMS" oi
			JOIN "TAKE_HOME_CHALLENGE"."ECOMMERCE"."ORDERS" o ON oi.ORDER_ID = o.ORDER_ID
			WHERE YEAR(o.ORDER_PURCHASE_TIMESTAMP) = 2017
			GROUP BY day
			HAVING COUNT(DISTINCT oi.ORDER_ID) >= 1
			ORDER BY day
			)
	SELECT DATE_TRUNC('month', day) AS month
		,ROUND(AVG(seller_count)) AS avg
	FROM daily_orders
	GROUP BY DATE_TRUNC('month', day)
	)
SELECT w1.month
	,w1.seller_count AS monthly_active_sellers
	,w2.avg AS avg_weekly_active_sellers
	,w3.avg AS avg_daily_active_sellers
FROM worksheet1 w1
JOIN worksheet2 w2 ON w1.month = w2.month
JOIN worksheet3 w3 ON w1.month = w3.month
ORDER BY month;