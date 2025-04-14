import requests
import json
import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt

API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
API_URL = "https://www.alphavantage.co/query"
PORTFOLIO_FILE = "portfolio.json"
console = Console()

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, 'w') as file:
        json.dump(portfolio, file, indent=4)

def get_stock_price(symbol):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    try:
        price = float(data["Global Quote"]["05. price"])
        return price
    except KeyError:
        return None

def display_portfolio(portfolio):
    if not portfolio:
        console.print("[bold red]Your portfolio is empty.[/bold red]")
        return

    table = Table(title="📈 Stock Portfolio", show_lines=True)
    table.add_column("Symbol", justify="center")
    table.add_column("Shares", justify="right")
    table.add_column("Buy Price", justify="right")
    table.add_column("Current Price", justify="right")
    table.add_column("Gain/Loss", justify="right")

    total_value = 0
    total_cost = 0

    for symbol, data in portfolio.items():
        current_price = get_stock_price(symbol)
        if current_price is None:
            console.print(f"[red]Failed to retrieve data for {symbol}[/red]")
            continue

        shares = data['shares']
        buy_price = data['buy_price']
        cost = shares * buy_price
        value = shares * current_price
        gain_loss = value - cost

        table.add_row(
            symbol,
            str(shares),
            f"${buy_price:.2f}",
            f"${current_price:.2f}",
            f"[green if gain_loss >= 0 else 'red']${gain_loss:.2f}[/]"
        )

        total_value += value
        total_cost += cost

    overall_gain = total_value - total_cost
    console.print(table)
    console.print(f"\n[bold]Total Investment:[/bold] ${total_cost:.2f}")
    console.print(f"[bold]Current Value:[/bold] ${total_value:.2f}")
    console.print(f"[bold]{'Gain' if overall_gain >= 0 else 'Loss'}:[/bold] [green if overall_gain >= 0 else 'red']${overall_gain:.2f}[/]")

def add_stock(portfolio):
    symbol = Prompt.ask("Enter stock symbol").upper()
    shares = IntPrompt.ask(f"How many shares of {symbol}?")
    buy_price = FloatPrompt.ask(f"What was the buy price per share for {symbol}?")
    portfolio[symbol] = {"shares": shares, "buy_price": buy_price}
    save_portfolio(portfolio)
    console.print(f"[green]Added {shares} shares of {symbol} at ${buy_price:.2f} each.[/green]")

def remove_stock(portfolio):
    symbol = Prompt.ask("Enter stock symbol to remove").upper()
    if symbol in portfolio:
        del portfolio[symbol]
        save_portfolio(portfolio)
        console.print(f"[red]Removed {symbol} from portfolio.[/red]")
    else:
        console.print("[bold red]Stock not found in portfolio.[/bold red]")

def main():
    portfolio = load_portfolio()

    while True:
        console.print("\n[bold cyan]Stock Portfolio Manager[/bold cyan]")
        console.print("1. View Portfolio")
        console.print("2. Add Stock")
        console.print("3. Remove Stock")
        console.print("4. Exit")

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])

        if choice == "1":
            display_portfolio(portfolio)
        elif choice == "2":
            add_stock(portfolio)
        elif choice == "3":
            remove_stock(portfolio)
        elif choice == "4":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break

if __name__ == "__main__":
    main()
