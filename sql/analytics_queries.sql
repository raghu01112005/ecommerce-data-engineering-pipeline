USE ecommerce_db;

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers
FROM cleaned_orders;


SELECT
    SUM(total_amount) AS completed_revenue
FROM cleaned_orders
WHERE status = 'Completed';


SELECT
    product,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM cleaned_orders
WHERE status = 'Completed'
GROUP BY product
ORDER BY units_sold DESC;


SELECT
    status,
    COUNT(*) AS number_of_orders
FROM cleaned_orders
GROUP BY status
ORDER BY number_of_orders DESC;

SELECT
    customer_id,
    COUNT(*) AS completed_orders,
    SUM(total_amount) AS total_spent
FROM cleaned_orders
WHERE status = 'Completed'
GROUP BY customer_id
ORDER BY total_spent DESC;