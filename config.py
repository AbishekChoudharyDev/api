# config.py

# === General Settings ===
MODE = "backtest"  # Options: "backtest", "live", "paper"

# === Capital and Risk ===
INITIAL_CAPITAL = 50  # USD
RISK_PER_TRADE_PERCENT = 2  # % of capital per trade
DAILY_LOSS_LIMIT = 10  # USD
MAX_TRADES_PER_DAY = 5

# === Trading Pairs ===
TRADING_PAIRS = ["ETH/USDT", "BTC/USDT", "SOL/USDT"]

# === Strategy Settings ===
RISK_REWARD_RATIO = 3  # 1:3
STOP_LOSS_PERCENT = 1.5  # Percent of entry
TAKE_PROFIT_PERCENT = STOP_LOSS_PERCENT * RISK_REWARD_RATIO

# === Partial Exit + Trailing SL ===
ENABLE_TRAILING_SL = True
PARTIAL_PROFIT_PERCENT = 50  # Book 50% at 1:1, trail rest
TRAILING_STEP = 0.25  # Move SL every 0.25%

# === Reporting Settings ===
DAILY_REPORT = True
REPORT_FILE = "daily_report.json"

# === Exchange API Keys (for live mode) ===
DELTA_API_KEY = "gJ1xVmeyelRwvPyli3JnbLpnyIIA8Y"
DELTA_API_SECRET = "gKSkxPqSnt9Z3o8Xc14Q79KoC510N1S5yI7iiBgHwa4rayv4hCXXMh44aB3q"
