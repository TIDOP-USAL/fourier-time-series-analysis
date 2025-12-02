import numpy as np
import pandas as pd


def export_sbas() -> None:
    ts_vertical = pd.read_csv("data/time_series_vertical.csv")

    FIDS_SBAS = [156,167,180,197,206,221]
    ts_vertical_filtered = ts_vertical[ts_vertical['point'].isin(FIDS_SBAS)]
    ts_vertical_filtered = ts_vertical_filtered.iloc[:, 0:-2]

    dates_str = ts_vertical_filtered.columns[1:]
    dates = pd.to_datetime(dates_str)

    pd.Series(dates).to_csv("data/dates_sbas.csv", index=False)

    velocities = []
    for _, row in ts_vertical_filtered.iterrows():
        values = row[1:].values.astype(float)
        velocities.append(values)

    velocities = np.array(velocities)
    np.save('data/time_series_sbas.npy', velocities)


def export_psi() -> None:
    psi_df = pd.read_csv("data/psi_series.csv")
    psi_df["date"] = pd.to_datetime(psi_df["date"])
    psi_df = psi_df.sort_values('date')

    dates = psi_df['date'].unique()
    dates = pd.to_datetime(dates)

    pd.Series(dates).to_csv("data/dates_psi.csv", index=False)

    velocities = []
    unique_ids = psi_df['id'].unique()

    for point_id in unique_ids:
        df_point = psi_df[psi_df['id'] == point_id].sort_values('date')
        values = df_point['date']
        velocities.append(values)

    velocities = np.array(velocities, dtype=float)
    np.save("data/time_series_psi.npy", velocities)

if __name__ == "__main__":

    export_sbas()

    time_series_sbas = np.load("data/time_series_sbas.npy")
    dates_sbas = pd.read_csv("data/dates_sbas.csv", header=None).to_numpy()[1:].flatten()
    print(time_series_sbas.shape)

    export_psi()

    time_series_psi = np.load("data/time_series_psi.npy")
    dates_psi = pd.read_csv("data/dates_psi.csv", header=None).to_numpy()[1:].flatten()
    print(time_series_psi.shape)