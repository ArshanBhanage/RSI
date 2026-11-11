SELECT EXTRACT(hour FROM tpep_pickup_datetime) AS hour, MEDIAN(trip_distance) AS distance FROM trips WHERE trip_distance >= 0 GROUP BY 1;
