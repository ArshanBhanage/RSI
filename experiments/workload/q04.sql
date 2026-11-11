SELECT EXTRACT(dow FROM tpep_pickup_datetime) AS weekday, COUNT(*) AS trips FROM trips GROUP BY 1;
