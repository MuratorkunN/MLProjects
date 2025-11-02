CREATE TABLE frost_data (
    date DATE NOT NULL,
    min_temperature FLOAT,
    frost INTEGER
);

\COPY frost_data (date, min_temperature, frost)
FROM 'temp_and_frost_data.csv'
WITH (FORMAT csv, HEADER true);


CREATE TABLE frost_data_all (
    date DATE NOT NULL,
    min_temperature FLOAT
);

\COPY frost_data_all (date, min_temperature)
FROM 'temperature.csv'
WITH (FORMAT csv, HEADER true);