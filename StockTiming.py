from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf


def get_history(ticker: str, buy_date: datetime) -> pd.Series:
    ticker_history = yf.Ticker(ticker).history(period="max", start=buy_date)
    ticker_history["Close"] = (
        ticker_history["Close"] / ticker_history["Close"].iloc[0]
    ) - 1

    return ticker_history["Close"]


def main() -> None:

    df = pd.read_csv(
        "StockList.txt",
        sep=",",
        parse_dates=["buy_date"],
        dayfirst=True,
    )

    df_history = pd.DataFrame(
        {
            row_values["ticker"]: get_history(
                row_values["ticker"], row_values["buy_date"]
            )
            for _, row_values in df.iterrows()
        }
    )

    data = pd.melt(
        df_history.reset_index(),
        id_vars="Date",
        var_name="ticker",
        value_name="price_change",
    )

    fgrid = sns.FacetGrid(data, col="ticker", col_wrap=4, despine=False)
    fgrid.map(sns.lineplot, "Date", "price_change")
    fgrid.refline(y=0)
    fgrid.set(xticklabels=[])
    fgrid.figure.subplots_adjust(wspace=0)
    plt.show()


if __name__ == "__main__":
    main()
