from contextlib import closing
from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Analyst Setup Demo", layout="wide")
st.title("Your analyst workspace is ready")
st.info("Synthetic setup data only — not real ETF performance.")

db = Path(__file__).resolve().parent / "data" / "setup_demo.db"

if not db.exists():
    st.error("Run verify_setup.py first, then refresh this page.")
    st.stop()

with closing(sqlite3.connect(db)) as con:
    df = pd.read_sql_query(
        "SELECT date, symbol, index_value "
        "FROM demo_prices ORDER BY date, symbol",
        con,
    )

df["date"] = pd.to_datetime(df["date"])

st.subheader("Demo data loaded from SQLite")
st.dataframe(df, hide_index=True)

chart = df.pivot(
    index="date", columns="symbol", values="index_value"
)

st.subheader("Made-up index values; both start at 100")
st.line_chart(chart)
st.caption("Next: replace this demo with your research pipeline.")