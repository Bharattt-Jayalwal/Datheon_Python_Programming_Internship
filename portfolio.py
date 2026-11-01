
import csv
import os
from datetime import datetime

import yfinance as yf

CSV_FILE = "portfolio_summary.csv"


def get_stock_price(symbol):
    """Fetch the latest available stock price."""
    try:
        stock = yf.Ticker(symbol)

        # Try intraday market data first
        data = stock.history(period="1d", interval="1m")

        # Fallback to the latest daily closing price
        if data.empty:
            data = stock.history(period="5d", interval="1d")

        if data.empty:
            return None

        return float(data["Close"].dropna().iloc[-1])

    except Exception as error:
        print(f"Price lookup failed for {symbol}: {error}")
        return None


def get_portfolio():
    """Collect stock details from the user."""
    portfolio = {}

    print("\n===== STUDENT PORTFOLIO TRACKER =====")
    print("Enter your stock details below.")
    print("Type DONE when you finish.\n")

    while True:
        symbol = input("Enter stock ticker: ").strip().upper()

        if symbol == "DONE":
            break

        if not symbol:
            print("Ticker cannot be empty.")
            continue

        try:
            buy_price = float(input("Enter purchase price: "))
            quantity = int(input("Enter number of shares: "))

            if buy_price <= 0 or quantity <= 0:
                print("Price and quantity must be positive.")
                continue

            portfolio.setdefault(symbol, []).append({
                "buy_price": buy_price,
                "quantity": quantity
            })

        except ValueError:
            print("Please enter valid numeric values.")

    return portfolio


def calculate_portfolio(portfolio):
    """Calculate investment and current portfolio value."""
    results = []
    total_invested = 0
    total_value = 0

    print("\n" + "=" * 75)
    print("             STUDENT INVESTMENT PORTFOLIO REPORT")
    print("=" * 75)

    print(
        f"{'STOCK':<12}{'BUY PRICE':>12}"
        f"{'CURRENT':>12}{'QUANTITY':>10}"
        f"{'P/L':>12}{'RETURN':>12}"
    )

    print("-" * 75)

    for symbol, holdings in portfolio.items():
        current_price = get_stock_price(symbol)

        if current_price is None:
            print(f"Could not retrieve price for {symbol}. Skipping.")
            continue

        for holding in holdings:
            buy_price = holding["buy_price"]
            quantity = holding["quantity"]

            invested = buy_price * quantity
            market_value = current_price * quantity
            profit_loss = market_value - invested
            percentage = (profit_loss / invested) * 100

            total_invested += invested
            total_value += market_value

            print(
                f"{symbol:<12}"
                f"{buy_price:>12.2f}"
                f"{current_price:>12.2f}"
                f"{quantity:>10}"
                f"{profit_loss:>12.2f}"
                f"{percentage:>11.2f}%"
            )

            results.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
                "buy_price": buy_price,
                "current_price": current_price,
                "quantity": quantity,
                "invested": invested,
                "market_value": market_value,
                "profit_loss": profit_loss,
                "return_percentage": percentage
            })

    total_profit = total_value - total_invested

    total_return = (
        (total_profit / total_invested) * 100
        if total_invested > 0 else 0
    )

    print("-" * 75)
    print(f"Total Investment : {total_invested:.2f}")
    print(f"Current Value    : {total_value:.2f}")
    print(f"Total Profit/Loss: {total_profit:.2f}")
    print(f"Overall Return   : {total_return:.2f}%")
    print("=" * 75)

    return results


def save_to_csv(results):
    """Append portfolio results to an external CSV file."""
    if not results:
        print("No results available to save.")
        return

    file_exists = os.path.isfile(CSV_FILE)

    fieldnames = [
        "date", "symbol", "buy_price", "current_price",
        "quantity", "invested", "market_value",
        "profit_loss", "return_percentage"
    ]

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writeheader()

        writer.writerows(results)

    print(f"\nPortfolio successfully saved to {CSV_FILE}")


def main():
    portfolio = get_portfolio()

    if not portfolio:
        print("No stocks entered. Exiting program.")
        return

    results = calculate_portfolio(portfolio)
    save_to_csv(results)


if __name__ == "__main__":
    main()
