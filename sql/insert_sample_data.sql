INSERT INTO aq.station (name, latitude, longitude, zone)
VALUES ('Padova (Open-Meteo CAMS grid)', 45.408, 11.8859, 'city')


INSERT INTO aq.source (name, description, url)
VALUES ('Open-Meteo Air Quality (CAMS Europe)', 'Hourly air quality modeled data', 'https://open-meteo.com/')

INSERT INTO aq.pollutants (code, name, unit, description) VALUES
('pm10', 'Particulate Matter ≤10µm', 'µg/m³', 'Inhalable particles with a diameter of 10 micrometers or less.'),
('pm2_5', 'Particulate Matter ≤2.5µm', 'µg/m³', 'Fine inhalable particles with a diameter of 2.5 micrometers or less.'),
('nitrogen_dioxide', 'Nitrogen Dioxide (NO₂)', 'µg/m³', 'A toxic gas from high-temperature combustion, like vehicle engines.'),
('ozone', 'Ozone (O₃)', 'µg/m³', 'A reactive gas formed from chemical reactions in the presence of sunlight.'),
('sulphur_dioxide', 'Sulphur Dioxide (SO₂)', 'µg/m³', 'A colorless, pungent gas from the burning of sulfur-containing fossil fuels.'),
('carbon_monoxide', 'Carbon Monoxide (CO)', 'mg/m³', 'A colorless, odorless, and toxic gas from incomplete combustion.')

