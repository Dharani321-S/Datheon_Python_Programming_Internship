#!/usr/bin/env python3
"""Stock Portfolio Performance Tracker (Console)

Enter stock tickers, buy prices and share quantities. The program looks up
current prices from a CSV file, computes invested capital, market value and
gain/loss (absolute and %), then logs everything to 'portfolio_summary.csv'.

Run:  python portfolio.py
Price source: 'sample_prices.csv' (columns: Symbol/Ticker, Price/Close).
Point PRICES_FILE at the downloaded S&P 500 dataset to use it instead.
If a ticker is not found, you are asked to type the current price manually.
"""

import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICES_FILE = os.path.join(BASE_DIR, "sample_prices.csv")
SUMMARY_FILE = os.path.join(BASE_DIR, "portfolio_summary.csv")

FALLBACK_PRICES = {"AAPL": 228.50, "MSFT": 425.30, "GOOGL": 178.20, "TSLA": 255.40}

SYMBOL_HEADERS = ("symbol", "ticker")
PRICE_HEADERS = ("price", "close", "last", "current price", "adj close")


# ---------- price loading ----------
def load_prices(path=PRICES_FILE):
    """Return {TICKER: price}. Detects column names flexibly; falls back safely."""
    prices = {}
    if os.path.exists(path):
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                fields = {name.strip().lower(): name for name in (reader.fieldnames or [])}
                sym_col = next((fields[h] for h in SYMBOL_HEADERS if h in fields), None)
                price_col = next((fields[h] for h in PRICE_HEADERS if h in fields), None)
                if sym_col and price_col:
                    for row in reader:
                        try:
                            prices[row[sym_col].strip().upper()] = float(row[price_col])
                        except (ValueError, AttributeError, TypeError):
                            continue  # skip blank/bad rows
        except OSError:
            pass
    return prices or dict(FALLBACK_PRICES)


# ---------- input helpers ----------
def read_positive_float(prompt):
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            value = float(raw)
            if value > 0:
                return value
        except ValueError:
            pass
        print("  Please enter a number greater than 0.")


def read_ticker(prompt):
    while True:
        t = input(prompt).strip().upper()
        if t.isalpha() and 1 <= len(t) <= 6:
            return t
        print("  Enter a valid ticker symbol (letters only, e.g. AAPL).")


# ---------- portfolio logic ----------
def add_position(portfolio, prices):
    """Add a holding; merge with an existing one using weighted-average cost."""
    ticker = read_ticker("Ticker symbol: ")
    buy_price = read_positive_float("Buy price per share ($): ")
    shares = read_positive_float("Number of shares: ")

    if ticker in portfolio:
        old = portfolio[ticker]
        total_shares = old["shares"] + shares
        avg = (old["buy_price"] * old["shares"] + buy_price * shares) / total_shares
        portfolio[ticker] = {"buy_price": avg, "shares": total_shares}
        print(f"  Updated {ticker}: {total_shares:g} shares @ avg ${avg:,.2f}")
    else:
        portfolio[ticker] = {"buy_price": buy_price, "shares": shares}
        print(f"  Added {ticker}: {shares:g} shares @ ${buy_price:,.2f}")

    if ticker not in prices:
        print(f"  '{ticker}' not found in price data.")
        prices[ticker] = read_positive_float(f"  Enter current price for {ticker} ($): ")


def evaluate(portfolio, prices):
    """Return (rows, totals) with per-holding and overall performance."""
    rows = []
    total_invested = total_value = 0.0
    for ticker, pos in sorted(portfolio.items()):
        invested = pos["buy_price"] * pos["shares"]
        current = prices[ticker]
        value = current * pos["shares"]
        gain = value - invested
        pct = gain / invested * 100
        rows.append({
            "Ticker": ticker, "Shares": pos["shares"], "Buy Price": pos["buy_price"],
            "Current Price": current, "Invested": invested, "Market Value": value,
            "Gain/Loss": gain, "Gain/Loss %": pct,
        })
        total_invested += invested
        total_value += value
    total_gain = total_value - total_invested
    total_pct = (total_gain / total_invested * 100) if total_invested else 0.0
    totals = {"Invested": total_invested, "Market Value": total_value,
              "Gain/Loss": total_gain, "Gain/Loss %": total_pct}
    return rows, totals


# ---------- output ----------
def print_report(rows, totals):
    if not rows:
        print("\n  Portfolio is empty. Add a position first.")
        return
    header = (f"{'Ticker':<8}{'Shares':>9}{'Buy $':>11}{'Now $':>11}"
              f"{'Invested':>13}{'Value':>13}{'Gain/Loss':>13}{'%':>9}")
    line = "-" * len(header)
    print("\n" + line + "\n" + header + "\n" + line)
    for r in rows:
        print(f"{r['Ticker']:<8}{r['Shares']:>9,.2f}{r['Buy Price']:>11,.2f}"
              f"{r['Current Price']:>11,.2f}{r['Invested']:>13,.2f}"
              f"{r['Market Value']:>13,.2f}{r['Gain/Loss']:>+13,.2f}{r['Gain/Loss %']:>+8.2f}%")
    print(line)
    print(f"{'TOTAL':<8}{'':>9}{'':>11}{'':>11}{totals['Invested']:>13,.2f}"
          f"{totals['Market Value']:>13,.2f}{totals['Gain/Loss']:>+13,.2f}"
          f"{totals['Gain/Loss %']:>+8.2f}%")
    print(line)
    status = "PROFIT" if totals["Gain/Loss"] >= 0 else "LOSS"
    print(f"Overall portfolio status: {status}\n")


def save_summary(rows, totals, path=SUMMARY_FILE):
    """Write the performance log to CSV (with timestamp and a TOTAL row)."""
    if not rows:
        print("  Nothing to save yet.")
        return
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fields = ["Timestamp", "Ticker", "Shares", "Buy Price", "Current Price",
              "Invested", "Market Value", "Gain/Loss", "Gain/Loss %"]
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for r in rows:
                writer.writerow({"Timestamp": stamp, **{k: round(v, 2) if isinstance(v, float) else v
                                                         for k, v in r.items()}})
            writer.writerow({"Timestamp": stamp, "Ticker": "TOTAL",
                             **{k: round(v, 2) for k, v in totals.items()}})
        print(f"  Summary saved to: {os.path.basename(path)}")
    except OSError as err:
        print(f"  Could not write CSV: {err}")


def remove_position(portfolio):
    ticker = read_ticker("Ticker to remove: ")
    if portfolio.pop(ticker, None) is None:
        print(f"  {ticker} is not in your portfolio.")
    else:
        print(f"  Removed {ticker}.")


MENU = """
=== STOCK PORTFOLIO TRACKER ===
 1. Add a stock position
 2. View portfolio performance
 3. Remove a position
 4. Save summary to CSV
 5. Exit
"""


def main():
    prices = load_prices()
    portfolio = {}
    print(f"Loaded {len(prices)} ticker prices.")
    while True:
        print(MENU)
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_position(portfolio, prices)
        elif choice == "2":
            print_report(*evaluate(portfolio, prices))
        elif choice == "3":
            remove_position(portfolio)
        elif choice == "4":
            save_summary(*evaluate(portfolio, prices))
        elif choice == "5":
            if portfolio:
                save_summary(*evaluate(portfolio, prices))
            print("Goodbye!")
            break
        else:
            print("  Invalid option. Choose 1-5.")


if __name__ == "__main__":
    main()
