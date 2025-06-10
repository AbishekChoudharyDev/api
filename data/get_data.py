import ccxt
import json
import os
from datetime import datetime

def fetch_ohlcv(symbol="ETH/USDT", timeframe='15m', total_limit=100000):
    binance = ccxt.binance()
    print(f"📊 Fetching OHLCV data for {symbol} ({timeframe}) — up to {total_limit} candles")

    all_data = []
    since = binance.milliseconds() - binance.parse_timeframe(timeframe) * 1000 * total_limit

    while len(all_data) < total_limit:
        try:
            ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            break

        if not ohlcv:
            print("⚠️ No more data returned.")
            break

        all_data.extend(ohlcv)
        since = ohlcv[-1][0] + 1  # Move past last candle
        print(f"⏳ Fetched: {len(all_data)} / {total_limit}")

        if len(ohlcv) < 1000:
            break

    parsed_data = [{
        "timestamp": datetime.utcfromtimestamp(entry[0] / 1000).isoformat(),  # 👈 Fixed: was 100000
        "open": entry[1],
        "high": entry[2],
        "low": entry[3],
        "close": entry[4],
        "volume": entry[5]
    } for entry in all_data[:total_limit]]

    os.makedirs("data", exist_ok=True)
    filename = f"data/{symbol.replace('/', '_').lower()}_ohlcv.json"

    with open(filename, "w") as f:
        json.dump(parsed_data, f, indent=4)

    print(f"✅ Saved {len(parsed_data)} candles to {filename}")

if __name__ == "__main__":
    fetch_ohlcv("ETH/USDT", '15m', total_limit=100000)
    fetch_ohlcv("BTC/USDT", '15m', total_limit=100000)
    fetch_ohlcv("SOL/USDT", '15m', total_limit=100000)