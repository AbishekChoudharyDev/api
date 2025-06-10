# backtest_15min.py

import pandas as pd
from ema_400_strategy import apply_ema_400_strategy
from utils.helpers import load_data
from datetime import datetime

RR_RATIO = 2.0
TRADE_SIZE = 50
MAX_TRADES_PER_DAY = 3

def backtest_ema_400(df):
    trades = []
    in_position = False
    entry_price, stop_loss, target = 0, 0, 0
    trailing_stop = None
    daily_trades = {}

    for i in range(1, len(df)):
        date = pd.to_datetime(df['timestamp'].iloc[i]).date()
        daily_trades.setdefault(date, 0)

        if daily_trades[date] >= MAX_TRADES_PER_DAY:
            continue

        signal = df['position'].iloc[i]
        price = df['close'].iloc[i]
        ema = df['ema_400'].iloc[i]

        # Entry logic
        if not in_position:
            if signal == 1:
                entry_price = price
                stop_loss = ema
                target = entry_price + (entry_price - stop_loss) * RR_RATIO
                trailing_stop = entry_price + (entry_price - stop_loss) * 1.0
                in_position = True
                daily_trades[date] += 1
                trades.append({
                    "type": "LONG",
                    "entry": entry_price,
                    "stop_loss": stop_loss,
                    "target": target,
                    "exit": None,
                    "result": None
                })
            elif signal == -1:
                entry_price = price
                stop_loss = ema
                target = entry_price - (stop_loss - entry_price) * RR_RATIO
                trailing_stop = entry_price - (stop_loss - entry_price) * 1.0
                in_position = True
                daily_trades[date] += 1
                trades.append({
                    "type": "SHORT",
                    "entry": entry_price,
                    "stop_loss": stop_loss,
                    "target": target,
                    "exit": None,
                    "result": None
                })

        elif in_position:
            trade = trades[-1]
            if trade['type'] == "LONG":
                if price <= stop_loss:
                    trade['exit'] = price
                    trade['result'] = "LOSS"
                    in_position = False
                elif price >= target:
                    trade['exit'] = price
                    trade['result'] = "WIN"
                    in_position = False
                elif price > trailing_stop:
                    trailing_stop = price - (entry_price - stop_loss) * 0.5
                elif price < trailing_stop:
                    trade['exit'] = price
                    trade['result'] = "WIN"
                    in_position = False

            elif trade['type'] == "SHORT":
                if price >= stop_loss:
                    trade['exit'] = price
                    trade['result'] = "LOSS"
                    in_position = False
                elif price <= target:
                    trade['exit'] = price
                    trade['result'] = "WIN"
                    in_position = False
                elif price < trailing_stop:
                    trailing_stop = price + (stop_loss - entry_price) * 0.5
                elif price > trailing_stop:
                    trade['exit'] = price
                    trade['result'] = "WIN"
                    in_position = False

    return trades

def generate_report(symbol, trades):
    wins = [t for t in trades if t["result"] == "WIN"]
    losses = [t for t in trades if t["result"] == "LOSS"]

    total_trades = len(trades)
    win_rate = (len(wins) / total_trades) * 100 if total_trades else 0
    profit = len(wins) * (TRADE_SIZE * RR_RATIO)
    loss = len(losses) * TRADE_SIZE
    net = profit - loss

    print(f"\n==== BACKTESTING {symbol.upper()} ====")
    print(f"--- BACKTEST REPORT for {symbol.upper()} ---")
    print(f"Total Trades : {total_trades}")
    print(f"Wins         : {len(wins)}")
    print(f"Losses       : {len(losses)}")
    print(f"Win Rate     : {win_rate:.2f}%")
    print(f"Net P&L      : ${net:.2f}")
    print("-----------------------------------")

if __name__ == "__main__":
    symbols = ["ETH/USDT", "BTC/USDT", "SOL/USDT"]

    for symbol in symbols:
        try:
            df = load_data(symbol)  # symbol passed, path handled in helpers.py
            df = apply_ema_400_strategy(df)
            trades = backtest_ema_400(df)
            generate_report(symbol.replace("/", "_"), trades)
        except FileNotFoundError as e:
            print(f"❌ Error for {symbol}: {e}")
