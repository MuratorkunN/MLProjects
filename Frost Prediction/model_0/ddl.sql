CREATE TABLE daily_temperature(
    date DATE PRIMARY KEY,
    min_temperature REAL
);

CREATE TABLE phenological_stage(
    stage_code INTEGER PRIMARY KEY,
    stage_name VARCHAR(30) NOT NULL,
    start_day INTEGER,
    end_day INTEGER,
    mild_frost_threshold REAL,
    moderate_frost_threshold REAL,
    severe_frost_threshold REAL
);

CREATE TABLE model_predictions(
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL REFERENCES daily_temperature(date),
    min_temperature REAL,
    phenological_stage_code INTEGER NOT NULL REFERENCES phenological_stage(stage_code),
    temp_7day_mean REAL,
    temp_3day_trend REAL,
    frost_days_10 INTEGER,
    stage_day INTEGER,
    temp_stage_interaction REAL,
    predicted_frost_damage INTEGER NOT NULL,  -- 0: None, 1: Mild, 2: Moderate, 3: Severe
    model_version VARCHAR(20),                --'rf_v1', 'xgb_v1'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
