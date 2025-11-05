import pandas as pd
import numpy as np

df_temperature = pd.read_csv(
    "temperature.csv",
    parse_dates=["date"]
)

phenology_matrix = [
    {"stage_code": 1, "stage_name": "Dinlenme", "start_day": 1, "end_day": 45, "mild_frost_threshold": -18.0, "moderate_frost_threshold": -20.0, "severe_frost_threshold": -25.0},
    {"stage_code": 2, "stage_name": "Tomurcuk Kabarma", "start_day": 46, "end_day": 69, "mild_frost_threshold": -3.89, "moderate_frost_threshold": -6.0, "severe_frost_threshold": -9.44},
    {"stage_code": 3, "stage_name": "Pembe Tomurcuk", "start_day": 70, "end_day": 79, "mild_frost_threshold": -3.33, "moderate_frost_threshold": -4.5, "severe_frost_threshold": -6.11},
    {"stage_code": 4, "stage_name": "Tam Çiçeklenme", "start_day": 80, "end_day": 90, "mild_frost_threshold": -2.78, "moderate_frost_threshold": -3.5, "severe_frost_threshold": -4.44},
    {"stage_code": 5, "stage_name": "Çiçeklenme Sonu", "start_day": 91, "end_day": 105, "mild_frost_threshold": -2.22, "moderate_frost_threshold": -3.0, "severe_frost_threshold": -3.89},
    {"stage_code": 6, "stage_name": "Küçük Meyve", "start_day": 106, "end_day": 120, "mild_frost_threshold": -1.0, "moderate_frost_threshold": -1.3, "severe_frost_threshold": -1.7}
]
df_phenology = pd.DataFrame(phenology_matrix)

df_temperature["day_of_year"] = df_temperature["date"].dt.dayofyear

def get_phenological_stage_code(day_of_year, phenology_df):
    for _, row in phenology_df.iterrows():
        if row["start_day"] <= day_of_year <= row["end_day"]:
            return row["stage_code"]
    return 0

df_temperature["phenological_stage_code"] = df_temperature["day_of_year"].apply(
    lambda doy: get_phenological_stage_code(doy, df_phenology)
)

df_temperature["temp_7day_mean"] = df_temperature["min_temp"].rolling(window=7, min_periods=1).mean()
df_temperature["temp_3day_trend"] = df_temperature["min_temp"].diff(periods=3)
df_temperature["frost_days_10"] = df_temperature["min_temp"].rolling(window=10, min_periods=1).apply(lambda x: (x < 0).sum())
df_temperature["stage_day"] = (df_temperature.groupby("phenological_stage_code", group_keys=False).cumcount() + 1)

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
    temp = row['min_temp']
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
df_temperature['frost_damage'] = df_temperature['frost_damage'].apply(lambda x: 1 if x > 0 else 0)

def temp_minus_critical(row):
    code = row["phenological_stage_code"]
    temp = row["min_temp"]
    if code == 0 or pd.isnull(temp):
        return np.nan
    return temp - phenology_thresholds[code]['mild']

df_temperature["temp_minus_critical"] = df_temperature.apply(temp_minus_critical, axis=1)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix

feature_cols = [
    'min_temp',
    'phenological_stage_code',
    'day_of_year',
    'temp_7day_mean',
    'temp_3day_trend',
    'frost_days_10',
    'stage_day',
    'temp_minus_critical'
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




test_df = pd.read_csv("temp_and_frost_data.csv", parse_dates=["date"])
test_df["date"] = pd.to_datetime(test_df["date"])

test_df['frost'] = test_df['frost'].apply(lambda x: 1 if x > 0 else 0)

test_df["day_of_year"] = test_df["date"].dt.day_of_year
test_df["phenological_stage_code"] = test_df["day_of_year"].apply(
    lambda doy: get_phenological_stage_code(doy, df_phenology)
)
test_df["temp_7day_mean"] = test_df["min_temp"].rolling(window=7, min_periods=1).mean()
test_df["temp_3day_trend"] = test_df["min_temp"].diff(periods=3)
test_df["frost_days_10"] = test_df["min_temp"].rolling(window=10, min_periods=1).apply(lambda x: (x < 0).sum())
test_df["stage_day"] = (test_df.groupby("phenological_stage_code", group_keys=False).cumcount() + 1)

def temp_minus_critical_test(row):
    code = row["phenological_stage_code"]
    temp = row["min_temp"]
    if code == 0 or pd.isnull(temp):
        return np.nan
    return temp - phenology_thresholds[code]['mild']

test_df["temp_minus_critical"] = test_df.apply(temp_minus_critical_test, axis=1)

external_feature_cols = [
    'min_temp',
    'phenological_stage_code',
    'day_of_year',
    'temp_7day_mean',
    'temp_3day_trend',
    'frost_days_10',
    'stage_day',
    'temp_minus_critical'
]

X_external = test_df[external_feature_cols]
y_external = test_df['frost']

rf_pred = rf_model.predict(X_external)
xgb_pred = xgb_model.predict(X_external)

from sklearn.metrics import classification_report, confusion_matrix
print("\nRandom Forest: GERÇEK LABEL İLE DIŞ TEST SONUCU")
print(classification_report(y_external, rf_pred))
print("XGBoost: GERÇEK LABEL İLE DIŞ TEST SONUCU")
print(classification_report(y_external, xgb_pred))
print("\nRandom Forest confusion matrix:")
print(confusion_matrix(y_external, rf_pred))
print("\nXGBoost confusion matrix:")
print(confusion_matrix(y_external, xgb_pred))
