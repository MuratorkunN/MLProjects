import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
from matplotlib.ticker import MaxNLocator, MultipleLocator

class HistoricalData:
    def __init__(self, date, df, col1, col2):
        self.date = date
        try:
            self.target_day, self.target_month = map(int, date.split('.'))
        except ValueError:
            print("date format dd.mm")
            return

        data_df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(data_df[col1]):
            data_df[col1] = pd.to_datetime(data_df[col1])

        self.historical_obs = data_df[(data_df[col1].dt.day == self.target_day) & (data_df[col1].dt.month == self.target_month)][col2].dropna()

        if len(self.historical_obs) < 2:
            print(f"insufficient data for {date}: {len(self.historical_obs)}")
            return

        self.df_deg, self.loc_t, self.scale_t = t.fit(self.historical_obs)
        self.mean = self.loc_t
        self.stdev = self.scale_t

    def get_mean(self):
        return self.mean

    def get_stdev(self):
        return self.stdev

    def plot(self):
        if not hasattr(self, 'historical_obs') or len(self.historical_obs) < 2:
            return

        is_integer = pd.api.types.is_integer_dtype(self.historical_obs) or np.all(np.mod(self.historical_obs, 1) == 0)

        x_min, x_max = self.historical_obs.min(), self.historical_obs.max()
        buffer = (x_max - x_min) * 0.3 if x_max != x_min else 1.0
        x_vals = np.linspace(x_min - buffer, x_max + buffer, 500)
        pdf_t = t.pdf(x_vals, self.df_deg, self.mean, self.stdev)

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 6))

        if is_integer:
            min_val = int(self.historical_obs.min())
            max_val = int(self.historical_obs.max())
            bins = np.arange(min_val - 0.5, max_val + 1.5, 1)

            ax.hist(self.historical_obs, bins=bins, density=True,
                    color='#2e7d32', edgecolor='black', alpha=0.7, label='Observed')
        else:
            ax.hist(self.historical_obs, bins='auto', density=True,
                    color='#1565c0', edgecolor='black', alpha=0.7, label='Observed')

        ax.plot(x_vals, pdf_t, color='cyan', lw=2.5,
                label=f'T Fit ($\mu$={self.mean:.1f}, $\sigma$={self.stdev:.1f})')

        ax.xaxis.set_major_locator(MultipleLocator(2))

        ax.set_title(f'Historical Temperature: {self.date}', fontsize=16, color='white', pad=15)
        ax.set_xlabel('Temperature', fontsize=12)
        ax.set_ylabel('Prob Density', fontsize=12)
        ax.axvline(self.mean, color='white', linestyle='--', linewidth=1, alpha=0.5, label='Mean')
        ax.grid(axis='y', alpha=0.2)
        ax.legend(loc='upper right', fontsize='medium')

        plt.tight_layout()
        plt.show()

        print(f"{self.date} with {len(self.historical_obs)} samples")
        print(f"mean: {self.mean:.4f}, stdev: {self.stdev:.4f}")

df_hist = pd.read_csv("era5/era5-temperature.csv")
df_hist['date'] = pd.to_datetime(df_hist['date'])

hd = HistoricalData("26.01", df_hist, 'date', 'min_temp')
hd.plot()
print(hd.mean, hd.stdev)
