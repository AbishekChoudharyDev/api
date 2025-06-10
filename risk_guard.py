MAX_RISK = 5  # $5 per trade

def validate_risk(entry, sl, capital=30):
    sl_distance = abs(entry - sl)
    risk = sl_distance * (capital / sl_distance)
    return risk <= MAX_RISK
