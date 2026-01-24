import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
from matplotlib.ticker import MaxNLocator, MultipleLocator

def get_historical_data(date, df, col1, col2):
    # plotting historical min temperature and fitting a distribution.

    try:
        target_day, target_month = map(int, date.split('.'))
    except ValueError:
        print("date format dd.mm")
        return

    data_df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(data_df[col1]):
        data_df[col1] = pd.to_datetime(data_df[col1])

    historical_obs = data_df[(data_df[col1].dt.day == target_day) & (data_df[col1].dt.month == target_month)][col2].dropna()

    if len(historical_obs) < 2:
        print(f"insufficient data for {date}: {len(historical_obs)}")
        return

    is_integer = pd.api.types.is_integer_dtype(historical_obs) or np.all(np.mod(historical_obs, 1) == 0)

    # fitting
    df_deg, loc_t, scale_t = t.fit(historical_obs)

    x_min, x_max = historical_obs.min(), historical_obs.max()
    buffer = (x_max - x_min) * 0.3 if x_max != x_min else 1.0
    x_vals = np.linspace(x_min - buffer, x_max + buffer, 500)
    pdf_t = t.pdf(x_vals, df_deg, loc_t, scale_t)


    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))

    if is_integer:
        min_val = int(historical_obs.min())
        max_val = int(historical_obs.max())
        bins = np.arange(min_val - 0.5, max_val + 1.5, 1)

        ax.hist(historical_obs, bins=bins, density=True,
                color='#2e7d32', edgecolor='black', alpha=0.7, label='Observed')
    else:
        ax.hist(historical_obs, bins='auto', density=True,
                color='#1565c0', edgecolor='black', alpha=0.7, label='Observed')

    ax.plot(x_vals, pdf_t, color='cyan', lw=2.5,
            label=f'T Fit ($\mu$={loc_t:.1f}, $\sigma$={scale_t:.1f})')


    ax.xaxis.set_major_locator(MultipleLocator(2))

    ax.set_title(f'Historical Temperature: {date}', fontsize=16, color='white', pad=15)
    ax.set_xlabel('Temperature', fontsize=12)
    ax.set_ylabel('Prob Density', fontsize=12)
    ax.axvline(loc_t, color='white', linestyle='--', linewidth=1, alpha=0.5, label='Mean')
    ax.grid(axis='y', alpha=0.2)
    ax.legend(loc='upper right', fontsize='medium')

    plt.tight_layout()
    plt.show()

    print(f"{date} with {len(historical_obs)} samples")
    print(f"t dist with mean {loc_t:.4f}, scale: {scale_t:.4f}")


df_hist = pd.read_csv("era5/era5-temperature.csv")
df_hist['date'] = pd.to_datetime(df_hist['date'])
get_historical_data("25.01", df_hist, 'date', 'min_temp')