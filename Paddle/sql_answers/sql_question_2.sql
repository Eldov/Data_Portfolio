WITH top_3_categories
AS (
	SELECT p.PRODUCT_CATEGORY_NAME AS product_category
		,COUNT(DISTINCT o.ORDER_ID) AS total_quantity
	FROM orders o
	JOIN order_items oi ON o.order_id = oi.order_id
	JOIN products p ON oi.product_id = p.product_id
	WHERE DATE_TRUNC('MONTH', o.ORDER_PURCHASE_TIMESTAMP) = '2017-11-01'
	GROUP BY product_category
	ORDER BY total_quantity DESC LIMIT 3
	)
	,weekly_sales
AS (
	SELECT p.PRODUCT_CATEGORY_NAME AS product_category
		,DATE_TRUNC('WEEK', o.ORDER_PURCHASE_TIMESTAMP) AS week
		,SUM(oi.price) AS weekly_gmv
	FROM orders o
	JOIN order_items oi ON o.order_id = oi.order_id
	JOIN products p ON oi.product_id = p.product_id
	WHERE DATE_TRUNC('YEAR', o.ORDER_PURCHASE_TIMESTAMP) = '2017-01-01'
		AND product_category IN (
			SELECT product_category
			FROM top_3_categories
			)
	GROUP BY product_category
		,week
	)
	,yearly_sales
AS (
	SELECT p.PRODUCT_CATEGORY_NAME AS product_category
		,SUM(oi.price) AS yearly_gmv
	FROM orders o
	JOIN order_items oi ON o.order_id = oi.order_id
	JOIN products p ON oi.product_id = p.product_id
	WHERE DATE_TRUNC('YEAR', o.ORDER_PURCHASE_TIMESTAMP) = '2017-01-01'
		AND product_category IN (
			SELECT product_category
			FROM top_3_categories
			)
	GROUP BY product_category
	)
	,weekly_sales_lag
AS (
	SELECT w1.week
		,w1.product_category
		,w1.weekly_gmv AS gmv
		,
		//w2.weekly_gmv AS weekly_gmv_lag,
		CAST(ROUND(((w1.weekly_gmv / w2.weekly_gmv) - 1) * 100) AS TEXT) || '%' AS gmv_growth_rate
	FROM weekly_sales w1
	JOIN weekly_sales w2 ON w1.product_category = w2.product_category
		AND w1.week > w2.week
		AND DATEDIFF('DAY', w2.week, w1.week) <= 7
	ORDER BY w1.product_category
		,w1.week DESC
	)
SELECT *
FROM weekly_sales_lag
//HAVING product_category = 'cama_mesa_banho'
ORDER BY week
	,product_category;
