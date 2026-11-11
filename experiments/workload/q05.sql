SELECT PULocationID AS pickup, DOLocationID AS dropoff, COUNT(*) AS trips FROM trips WHERE EXTRACT(day FROM tpep_pickup_datetime) <= 7 GROUP BY 1, 2;
