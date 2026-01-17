import pandas as pd

def standardize_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def parse_date(df, col="date"):
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df
