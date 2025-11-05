"""
import pandas as pd
import psycopg2

import psycopg2
import sys # Hataları daha net görmek için

print("step1...")

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        dbname="weather_data",
        user="postgres",
        password="frost"
    )
    print("step2")

    conn.close()
    print("Done")

except Exception as e:
    print("error", file=sys.stderr)
    print(f"details: {e}", file=sys.stderr)

"""

import pandas as pd
import psycopg2
import numpy as np

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="weather_data",
    user="postgres",
    password="frost"
)

df_temperature = pd.read_sql("SELECT * FROM daily_temperature ORDER BY date", conn, parse_dates=["date"])

df_phenology = pd.read_sql("SELECT * FROM phenological_stage ORDER BY stage_code", conn)

df_temperature["day_of_year"] = df_temperature["date"].dt.dayofyear

def get_phenological_stage_code(day_of_year, phenology_df):
    for _, row in phenology_df.iterrows():
        if row["start_day"] <= day_of_year <= row["end_day"]:
            return row["stage_code"]
    return 0

df_temperature["phenological_stage_code"] = df_temperature["day_of_year"].apply(
    lambda doy: get_phenological_stage_code(doy, df_phenology))

df_temperature["temp_7day_mean"] = df_temperature["min_temperature"].rolling(window=7, min_periods=1).mean()

df_temperature["temp_3day_trend"] = df_temperature["min_temperature"].diff(periods=3)

df_temperature["frost_days_10"] = df_temperature["min_temperature"].rolling(window=10, min_periods=1).apply(lambda x: (x < 0).sum())

df_temperature["stage_day"] = (df_temperature.groupby("phenological_stage_code", group_keys=False).cumcount() + 1)

df_temperature["temp_stage_interaction"] = df_temperature["min_temperature"] * df_temperature["phenological_stage_code"]

# print(df_temperature.head(10))

phenology_thresholds = {
    row['stage_code']: {
        'mild': row['mild_frost_threshold'],
        'moderate': row['moderate_frost_threshold'],
        'severe': row['severe_frost_threshold']
    }
    for _, row in df_phenology.iterrows()
}

def assign_frost_label(row):
    stage_code = row['phenological_stage_code']
    temp = row['min_temperature']
    if stage_code == 0 or pd.isnull(temp):
        return 0
    thresholds = phenology_thresholds[stage_code]
    if temp <= thresholds['severe']:
        return 3
    elif temp <= thresholds['moderate']:
        return 2
    elif temp <= thresholds['mild']:
        return 1
    else:
        return 0

df_temperature['frost_damage'] = df_temperature.apply(assign_frost_label, axis=1)

print(df_temperature['frost_damage'].value_counts())
print(df_temperature['frost_damage'].value_counts(normalize=True))

