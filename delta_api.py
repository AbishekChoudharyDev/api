# delta_api.py

import ccxt
import os
from dotenv import load_dotenv

# Load .env credentials
load_dotenv()

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")

# Setup Delta Exchange via CCXT
exchange = ccxt.delta({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
})


print("API KEY :",API_KEY)
print("API CODE :",API_SECRET)
# === Place Market Order ===
def place_market_order(symbol, side, quantity):
    """
    side: 'buy' or 'sell'
    """
    try:
        order = exchange.create_market_order(symbol, side, quantity)
        print(f"✅ {side.upper()} ORDER PLACED: {order['id']} | {symbol} | Qty: {quantity}")
        return order
    except Exception as e:
        print(f"❌ Failed to place order: {e}")
        return None

# === Get Balance ===
def get_balance(asset="USDT"):
    try:
        balance = exchange.fetch_balance()
        total = balance['total'].get(asset, 0)
        print(f"💰 Available {asset} Balance: {total}")
        return total
    except Exception as e:
        print(f"❌ Error fetching balance: {e}")
        return 0

def test_connection():
    try:
        balance = get_balance("USDT")
        print(f"🔗 Connected to Delta Exchange. USDT Balance: {balance}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
       
# === Test Usage ===
if __name__ == "__main__":
    get_balance("USDT")
    # place_market_order("ETH/USDT", "buy", 0.25)
