import json
import pandas as pd

with open('min_temperature.json', 'r') as f:
    temperature_json = json.load(f)

with open('frost.json', 'r') as f:
    frost_json = json.load(f)


df_all = pd.DataFrame({
    'date': temperature_json['date'],
    'min_temperature': temperature_json['data']
})

df_all['date'] = pd.to_datetime(df_all['date'], format='%m-%d-%Y')
df = df_all[df_all['date'] >= '2014-01-01'].copy()

df['frost'] = 0
frost_lookup = {
    item['date']: item['severity']
    for item in frost_json['frost_days']
}

for date_str, severity in frost_lookup.items():
    df.loc[df['date'].dt.strftime('%m-%d-%Y') == date_str, 'frost'] = severity

df.to_csv('temp_and_frost_data.csv', index=False)
