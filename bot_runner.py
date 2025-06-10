# bot_runner.py

import time
from datetime import datetime
import pandas as pd
from delta_api import place_market_order, get_balance, test_connection
from utils.helpers import load_data
from ema_400_strategy import apply_ema_400_strategy

SYMBOLS = ["ETH/USDT", "SOL/USDT"]
TRADE_QUANTITY = {
    "ETH/USDT": 0.25,
    "SOL/USDT": 1.0
}
RISK_PER_TRADE = 5   # max risk in USDT
CAPITAL = 30         # starting capital

def execute_trade_logic(symbol):
    df = load_data(symbol)
    trades = apply_ema_400_strategy(df)

    if not trades:
        print(f"⚠️ No trades found for {symbol}")
        return

    last_trade = trades[-1]
    current_time = datetime.utcnow()
    time_diff = current_time - pd.to_datetime(last_trade['entry_time'])

    # Only place trade if it's within the last 15 min
    if time_diff.total_seconds() < 900 and 'exit' not in last_trade:
        trade_type = last_trade['type'].lower()
        qty = TRADE_QUANTITY[symbol]

        usdt = get_balance("USDT")
        if usdt >= RISK_PER_TRADE:
            print(f"📈 Executing {trade_type.upper()} on {symbol} with qty {qty}")
            place_market_order(symbol, trade_type, qty)
        else:
            print(f"❌ Not enough balance to place trade. Available: {usdt}")
    else:
        print(f"🕓 No recent trade signal for {symbol}")

def main():
    print("🚀 Starting bot...")

    if not test_connection():
        print("❌ Bot cannot run without valid API key or connection.")
        return

    while True:
        print(f"\n⏰ Checking market at {datetime.utcnow().isoformat()}")

        for symbol in SYMBOLS:
            try:
                execute_trade_logic(symbol)
            except Exception as e:
                print(f"❌ Error processing {symbol}: {e}")

        print("🔁 Waiting 15 minutes...\n")
        time.sleep(900)

if __name__ == "__main__":
    main()
