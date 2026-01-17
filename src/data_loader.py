import os
import glob
import pandas as pd
from dotenv import load_dotenv
from src.cleaning import standardize_columns, parse_date

load_dotenv()

DATASET_PATH = os.getenv("DATASET_PATH", "dataset")

def load_csv_folder(folder):
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")

    files = glob.glob(os.path.join(folder, "*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files in {folder}")

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df = standardize_columns(df)
        df = parse_date(df)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

def load_all_datasets():
    enrolment = load_csv_folder(os.path.join(DATASET_PATH, "enrolment"))
    biometric = load_csv_folder(os.path.join(DATASET_PATH, "biometric"))
    demographic = load_csv_folder(os.path.join(DATASET_PATH, "demographic"))
    return enrolment, biometric, demographic
