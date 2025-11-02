CREATE TABLE frost_data (
    date DATE NOT NULL,
    min_temperature FLOAT,
    frost INTEGER
);

\COPY frost_data (date, min_temperature, frost)
FROM 'temp_and_frost_data.csv'
WITH (FORMAT csv, HEADER true);
