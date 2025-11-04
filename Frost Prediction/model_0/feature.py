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

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix

feature_cols = [
    'min_temperature',
    'phenological_stage_code',
    'day_of_year',
    'temp_7day_mean',
    'temp_3day_trend',
    'frost_days_10',
    'stage_day',
    'temp_stage_interaction'
]
X = df_temperature[feature_cols]
y = df_temperature['frost_damage']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=8,
    class_weight='balanced',
    random_state=42
)
rf_model.fit(X_train, y_train)

xgb_model = XGBClassifier(
    n_estimators=150,
    max_depth=6,
    learning_rate=0.08,
    random_state=42
)
xgb_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
xgb_pred = xgb_model.predict(X_test)

print("Random Forest Report:")
print(classification_report(y_test, rf_pred))

print("XGBoost Report:")
print(classification_report(y_test, xgb_pred))

import pandas as pd
feat_imp_rf = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nRandom Forest Feature Importances:\n")
print(feat_imp_rf)

feat_imp_xgb = pd.DataFrame({
    'feature': feature_cols,
    'importance': xgb_model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nXGBoost Feature Importances:\n")
print(feat_imp_xgb)

