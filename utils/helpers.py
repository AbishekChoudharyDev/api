# 🔧 helpers.py (Modified to fit the strategy and backtest you shared)

import json
import os
import pandas as pd

def load_data(pair):
    """
    Load historical OHLCV data from a file for backtesting.
    Handles both timestamp and millisecond "time" formats.
    """
    filename = f"data/{pair.replace('/', '_').lower()}_ohlcv.json"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Data file {filename} not found!")

    with open(filename, "r") as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)

    # Normalize timestamp
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    elif "time" in df.columns:
        df["timestamp"] = pd.to_datetime(df["time"], unit="ms")
    else:
        raise ValueError("Data must contain 'timestamp' or 'time' column")

    return df

def log_trade(trade):
    print(f"Trade executed: {trade['type']} | Entry: {trade['entry']} | Exit: {trade['exit']} | Result: {trade['result']} | PnL: {round(trade['exit'] - trade['entry'], 2)}")
