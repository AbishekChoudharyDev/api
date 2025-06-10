# ema_400_strategy.py

import pandas as pd
import ta

def apply_ema_400_strategy(df, capital=30, risk_per_trade=2.0, rr_ratio=2.0, trailing_step=0.5):
    df['ema_400'] = ta.trend.EMAIndicator(df['close'], window=400).ema_indicator()
    df.dropna(inplace=True)

    trades = []
    in_position = False
    entry_price = None
    direction = None
    sl = None
    tp = None
    quantity = None

    for i in range(1, len(df)):
        candle_close = df['close'].iloc[i]
        candle_time = df['timestamp'].iloc[i]
        ema_400 = df['ema_400'].iloc[i]

        if not in_position:
            if candle_close > ema_400:
                # Long Entry
                entry_price = candle_close
                sl = ema_400
                sl_distance = entry_price - sl
                if sl_distance <= 0:
                    continue  # Invalid setup
                quantity = round(risk_per_trade / sl_distance, 4)
                tp = entry_price + sl_distance * rr_ratio
                direction = 'LONG'
                in_position = True
                trades.append({
                    "entry_time": candle_time,
                    "type": direction,
                    "entry": entry_price,
                    "sl": sl,
                    "tp": tp,
                    "qty": quantity
                })

            elif candle_close < ema_400:
                # Short Entry
                entry_price = candle_close
                sl = ema_400
                sl_distance = sl - entry_price
                if sl_distance <= 0:
                    continue  # Invalid setup
                quantity = round(risk_per_trade / sl_distance, 4)
                tp = entry_price - sl_distance * rr_ratio
                direction = 'SHORT'
                in_position = True
                trades.append({
                    "entry_time": candle_time,
                    "type": direction,
                    "entry": entry_price,
                    "sl": sl,
                    "tp": tp,
                    "qty": quantity
                })

        elif in_position:
            # Trailing Stop Logic + Exit
            price = df['close'].iloc[i]

            if direction == 'LONG':
                if price <= sl:
                    trades[-1]["exit"] = price
                    trades[-1]["exit_time"] = candle_time
                    trades[-1]["result"] = "LOSS"
                    in_position = False

                elif price >= tp:
                    new_tp = price + (trailing_step / 100) * price
                    new_sl = price - (trailing_step / 100) * price
                    tp = new_tp
                    sl = new_sl

            elif direction == 'SHORT':
                if price >= sl:
                    trades[-1]["exit"] = price
                    trades[-1]["exit_time"] = candle_time
                    trades[-1]["result"] = "LOSS"
                    in_position = False

                elif price <= tp:
                    new_tp = price - (trailing_step / 100) * price
                    new_sl = price + (trailing_step / 100) * price
                    tp = new_tp
                    sl = new_sl

    return trades

def load_data(path):
    df = pd.read_json(path)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    elif 'time' in df.columns:
        df['timestamp'] = pd.to_datetime(df['time'], unit='ms')
    return df
