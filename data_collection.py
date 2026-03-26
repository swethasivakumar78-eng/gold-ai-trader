import yfinance as yf
import pandas_datareader.data as web
import pandas as pd
from datetime import date, timedelta
import time
# -----------------------------
# Define ticker and date range
# -----------------------------
gold_ticker = "GLD"

end_date = date.today()
start_date = end_date - timedelta(days=10*365)  # 10 years data

print("Fetching historical gold data...")

try:
    gold_data = yf.download(
        gold_ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    # Handle MultiIndex columns safely
    if isinstance(gold_data.columns, pd.MultiIndex):
        gold_data.columns = gold_data.columns.get_level_values(0)

    print("Gold data fetched successfully")

except Exception as e:
    print("Error fetching gold data:", e)
    gold_data = pd.DataFrame()


# -----------------------------
# Fetch macroeconomic data
# -----------------------------
print("Fetching macroeconomic data from FRED...")

try:

    # Inflation (Consumer Price Index)
    inflation_data = web.DataReader(
        "CPIAUCSL",
        "fred",
        start=start_date,
        end=end_date
    )

    # Interest Rate (Federal Funds Rate)
    interest_rate_data = web.DataReader(
        "DFF",
        "fred",
        start=start_date,
        end=end_date
    )

    print("Macroeconomic data fetched successfully")

except Exception as e:

  print("Fetching macroeconomic data from FRED...")

try:

    # retry if timeout happens
    for i in range(3):

        try:
            inflation_data = web.DataReader(
                "CPIAUCSL",
                "fred",
                start=start_date,
                end=end_date
            )

            interest_rate_data = web.DataReader(
                "DFF",
                "fred",
                start=start_date,
                end=end_date
            )

            print("Macroeconomic data fetched successfully")
            break

        except Exception as e:
            print("Retrying FRED download...", i+1)
            time.sleep(5)

except Exception as e:
    print("Error fetching macro data:", e)
    inflation_data = pd.DataFrame()
    interest_rate_data = pd.DataFrame()


# -----------------------------
# Merge datasets
# -----------------------------
if not gold_data.empty and not inflation_data.empty and not interest_rate_data.empty:

    all_data = gold_data.join(inflation_data, how="left")
    all_data = all_data.join(interest_rate_data, how="left")

    # Save dataset
    all_data.to_csv("gold_and_macro_data.csv")

    print("Dataset saved as gold_and_macro_data.csv")

else:
    print("Data merging failed due to missing data")