def generate_daily_report(trades):
    wins = [t for t in trades if t["result"] == "WIN"]
    losses = [t for t in trades if t["result"] == "LOSS"]
    net = len(wins) * 10 - len(losses) * 5  # Example calc

    print(f"\n📊 Daily Report")
    print(f"Trades: {len(trades)}, Wins: {len(wins)}, Losses: {len(losses)}, Net: ${net}")
