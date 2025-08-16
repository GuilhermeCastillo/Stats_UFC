import duckdb
import os
import pandas as pd
import re
from datetime import datetime

os.makedirs("data/staging", exist_ok=True)
os.makedirs("duckdb", exist_ok=True)

con = duckdb.connect(database="duckdb/ufc.duckdb", read_only=False)


def clean_text(text):
    if pd.isna(text):
        return None
    return re.sub(r"\s+", " ", text).strip()


fights_raw = pd.read_csv("data/raw/fights.csv")
fight_stats_raw = pd.read_csv("data/raw/fight_stats.csv")
