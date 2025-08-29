CREATE SCHEMA IF NOT EXISTS aq;

CREATE TABLE IF NOT EXISTS aq.stations (
    station_id BIGSERIAL PRIMARY KEY, 
    name VARCHAR(255), 
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    zone VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS aq.pollutants (
    pollutant_id BIGSERIAL PRIMARY KEY,  
    code VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    unit VARCHAR(255),
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS aq.sources (
    source_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS aq.fact_air_quality_hourly (
    measurement_id BIGSERIAL PRIMARY KEY,
    station_id BIGINT NOT NULL REFERENCES aq.stations(station_id),
    pollutant_id BIGINT NOT NULL REFERENCES aq.pollutants(pollutant_id),
    source_id BIGINT NOT NULL REFERENCES aq.sources(source_id),
    date_time TIMESTAMP NOT NULL,
    date DATE NOT NULL,
    hour SMALLINT NOT NULL CHECK (hour BETWEEN 0 AND 23),
    value REAL
);

CREATE TABLE IF NOT EXISTS aq.stg_openmeteo_hourly (
    stg_id BIGSERIAL PRIMARY KEY,
    time TIMESTAMP,
    pm10 FLOAT,
    pm2_5 FLOAT,
    no2 FLOAT,
    so2 FLOAT,
    co FLOAT,
    benzene FLOAT,
    ipa FLOAT
);
