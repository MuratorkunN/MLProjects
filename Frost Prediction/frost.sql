create table min_temp (
    id serial PRIMARY KEY,
    data JSONB
);

COPY weather_data(data)
FROM 'frost.json'
WITH (FORMAT json);