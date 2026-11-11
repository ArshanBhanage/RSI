SELECT EXTRACT(hour FROM tpep_pickup_datetime) AS hour, COUNT(*) AS trips FROM trips GROUP BY 1;
