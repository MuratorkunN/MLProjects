import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="weather_data",
    user="postgres",
    password="frost"
)
cur = conn.cursor()

df_temp = pd.read_csv(
    "temperature.csv",
    parse_dates=["date"],
    date_parser=lambda x: pd.to_datetime(x, format="%m-%d-%Y")
)

for _, row in df_temp.iterrows():
    if pd.isnull(row["min_temp"]):
        continue
    cur.execute("""
        INSERT INTO daily_temperature (date, min_temperature)
        VALUES (%s, %s)
        ON CONFLICT (date) DO NOTHING
    """, (row["date"].strftime("%Y-%m-%d"), float(row["min_temp"])))

phenology = [
    (1, "Dinlenme", 1, 45, -18.0, -20.0, -25.0),
    (2, "Tomurcuk Kabarma", 46, 69, -3.89, -6.0, -9.44),
    (3, "Pembe Tomurcuk", 70, 79, -3.33, -4.5, -6.11),
    (4, "Tam Ciceklenme", 80, 90, -2.78, -3.5, -4.44),
    (5, "Ciceklenme Sonu", 91, 105, -2.22, -3.0, -3.89),
    (6, "Kucuk meyve", 106, 120, -1.0, -1.3, -1.7),
]
cur.executemany("""
    INSERT INTO phenological_stage(
        stage_code, stage_name, start_day, end_day,
        mild_frost_threshold, moderate_frost_threshold, severe_frost_threshold
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (stage_code) DO NOTHING
""", phenology)

conn.commit()
cur.close()
conn.close()
