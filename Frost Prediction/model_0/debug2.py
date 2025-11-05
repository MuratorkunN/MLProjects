import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="weather_data",
        user="postgres",
        password="frost"
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("DB Bağlantısı ve Version OK ->", cur.fetchone())
    cur.execute("SELECT COUNT(*) FROM daily_temperature;")
    print("daily_temperature satır:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("Bağlantı Hatası:", e)
