from contextlib import closing
from pathlib import Path
import importlib
import sqlite3
import pandas as pd

for name in ["pandas", "numpy", "plotly", "streamlit",
             "yfinance", "pytest"]:
    importlib.import_module(name)
    print(f"OK: {name}")

root = Path(__file__).resolve().parent
data_dir = root / "data"
data_dir.mkdir(exist_ok=True)

# Made-up values used only to check your setup.
rows = [
    ("2025-01-02", "SPY", 100.0),
    ("2025-01-03", "SPY", 101.0),
    ("2025-01-06", "SPY", 100.5),
    ("2025-01-02", "QQQ", 100.0),
    ("2025-01-03", "QQQ", 102.0),
    ("2025-01-06", "QQQ", 101.0),
]

df = pd.DataFrame(rows, columns=["date", "symbol", "index_value"])

with closing(sqlite3.connect(data_dir / "setup_demo.db")) as con:
    df.to_sql("demo_prices", con, if_exists="replace", index=False)
    result = pd.read_sql_query(
        "SELECT symbol, COUNT(*) AS rows "
        "FROM demo_prices GROUP BY symbol ORDER BY symbol",
        con,
    )

print(result.to_string(index=False))
print("Setup check passed. Demo database created.")