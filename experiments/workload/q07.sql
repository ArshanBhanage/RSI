SELECT z.Borough AS borough, COUNT(*) AS trips FROM trips t LEFT JOIN zones z ON t.PULocationID = z.LocationID GROUP BY 1;
