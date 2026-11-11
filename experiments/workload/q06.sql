SELECT CAST(tpep_pickup_datetime AS DATE) AS day, SUM(total_amount) AS revenue FROM trips GROUP BY 1;
