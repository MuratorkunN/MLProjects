import pandas as pd
import numpy as np

df_temperature = pd.read_csv(
    "temperature.csv",
    parse_dates=["date"]
)

df_temperature["day_of_year"] = df_temperature["date"].dt.dayofyear

print(df_temperature)
