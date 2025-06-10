# backtester.py

import json
from config import *
from utils.helpers import load_data, log_trade
import strategy

results = []

def backtest(data):
    balance = INITIAL_CAPITAL
    trade_count = 0

    for candle in data:
        if trade_count >= MAX_TRADES_PER_DAY:
            break

        signal = strategy.generate_signal(candle)

        if signal == "buy":
            entry = candle["close"]
            stop_loss = entry - (entry * STOP_LOSS_PERCENT / 100)
            take_profit = entry + (entry * TAKE_PROFIT_PERCENT / 100)

            trade_result = simulate_trade(candle, entry, stop_loss, take_profit)

            if trade_result["status"] != "skipped":
                balance += trade_result["pnl"]
                results.append(trade_result)
                trade_count += 1

    return balance

def simulate_trade(candle, entry, sl, tp):
    low = candle["low"]
    high = candle["high"]

    if low <= sl:
        return {"entry": entry, "exit": sl, "pnl": -entry * RISK_PER_TRADE_PERCENT / 100, "status": "loss"}
    elif high >= tp:
        return {"entry": entry, "exit": tp, "pnl": entry * RISK_PER_TRADE_PERCENT / 100 * RISK_REWARD_RATIO, "status": "win"}
    else:
        return {"status": "skipped"}

def run_backtest():
    data = load_data("ETH/USDT")  # from utils/helpers
    final_balance = backtest(data)

    with open(REPORT_FILE, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Initial Capital: ${INITIAL_CAPITAL}")
    print(f"Final Capital: ${round(final_balance, 2)}")
    print(f"Total Trades: {len(results)}")

if __name__ == "__main__":
    run_backtest()
