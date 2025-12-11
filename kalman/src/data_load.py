import pandas as pd

def load_sensor_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    return df
