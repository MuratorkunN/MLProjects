import pandas as pd
import numpy as np

df = pd.read_csv("temp_and_frost_data.csv", parse_dates=["date"])

df['frost'] = df['frost'].apply(lambda x: 1 if x > 0 else 0)

phenology_matrix = [
    {"stage_code": 1, "stage_name": "Dinlenme", "start_day": 1, "end_day": 45, "mild_frost_threshold": -18.0, "moderate_frost_threshold": -20.0, "severe_frost_threshold": -25.0},
    {"stage_code": 2, "stage_name": "Tomurcuk Kabarma", "start_day": 46, "end_day": 69, "mild_frost_threshold": -3.89, "moderate_frost_threshold": -6.0, "severe_frost_threshold": -9.44},
    {"stage_code": 3, "stage_name": "Pembe Tomurcuk", "start_day": 70, "end_day": 79, "mild_frost_threshold": -3.33, "moderate_frost_threshold": -4.5, "severe_frost_threshold": -6.11},
    {"stage_code": 4, "stage_name": "Tam Çiçeklenme", "start_day": 80, "end_day": 90, "mild_frost_threshold": -2.78, "moderate_frost_threshold": -3.5, "severe_frost_threshold": -4.44},
    {"stage_code": 5, "stage_name": "Çiçeklenme Sonu", "start_day": 91, "end_day": 105, "mild_frost_threshold": -2.22, "moderate_frost_threshold": -3.0, "severe_frost_threshold": -3.89},
    {"stage_code": 6, "stage_name": "Küçük Meyve", "start_day": 106, "end_day": 120, "mild_frost_threshold": -1.0, "moderate_frost_threshold": -1.3, "severe_frost_threshold": -1.7}
]
df_phenology = pd.DataFrame(phenology_matrix)

df["day_of_year"] = df["date"].dt.day_of_year

def get_phenological_stage_code(day_of_year, phenology_df):
    for _, row in phenology_df.iterrows():
        if row["start_day"] <= day_of_year <= row["end_day"]:
            return row["stage_code"]
    return 0

df["phenological_stage_code"] = df["day_of_year"].apply(
    lambda doy: get_phenological_stage_code(doy, df_phenology)
)

df["temp_7day_mean"] = df["min_temp"].rolling(window=7, min_periods=1).mean()
df["temp_3day_trend"] = df["min_temp"].diff(periods=3)
df["frost_days_10"] = df["min_temp"].rolling(window=10, min_periods=1).apply(lambda x: (x < 0).sum())
df["stage_day"] = (df.groupby("phenological_stage_code", group_keys=False).cumcount() + 1)

phenology_thresholds = {
    row['stage_code']: {
        'mild': row['mild_frost_threshold'],
        'moderate': row['moderate_frost_threshold'],
        'severe': row['severe_frost_threshold']
    }
    for _, row in df_phenology.iterrows()
}

def temp_minus_critical(row):
    code = row["phenological_stage_code"]
    temp = row["min_temp"]
    if code == 0 or pd.isnull(temp):
        return np.nan
    return temp - phenology_thresholds[code]['mild']

df["temp_minus_critical"] = df.apply(temp_minus_critical, axis=1)

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
X = df[feature_cols]
y = df['frost']

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
