from delta_api import place_order, get_balance

def calculate_lot_size(sl_distance, risk_per_trade=5.0):  # $5 risk per trade
    capital = get_balance()
    qty = round(risk_per_trade / sl_distance, 3)
    return min(qty, capital / 10)  # Basic sanity cap

def execute_trade(symbol, signal, entry, sl):
    sl_distance = abs(entry - sl)
    quantity = calculate_lot_size(sl_distance)

    side = 'buy' if signal == 'LONG' else 'sell'
    place_order(symbol, side, quantity)
    print(f"✅ Trade Executed: {side.upper()} {quantity} {symbol} | Entry: {entry}, SL: {sl}")
