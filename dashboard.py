import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Trade Predictor",
    page_icon="📈",
    layout="wide"
)

st_autorefresh(interval=60000, key="refresh")

# --------------------------------------------------
# POSTGRES CONNECTION
# --------------------------------------------------

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = pd.read_sql("""
        SELECT *
        FROM scans
        ORDER BY scan_time DESC
    """, engine)

except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

if df.empty:
    st.warning("No scan results available")
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📈 Trade Predictor Dashboard")

st.markdown("Real-time Stock Ranking Dashboard")

selected = st.sidebar.selectbox(
    "Select Stock",
    sorted(df["symbol"].unique())
)

# --------------------------------------------------
# SIGNAL LOGIC
# --------------------------------------------------

def signal(score):
    if score >= 80:
        return "🟢 BUY"
    elif score >= 60:
        return "🟡 WATCH"
    else:
        return "🔴 EXIT"

df["signal"] = df["score"].apply(signal)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

st.subheader("Market Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Stocks Ranked", len(df))
c2.metric("Highest Score", round(df["score"].max(), 2))
c3.metric("Average Score", round(df["score"].mean(), 2))
c4.metric("Last Scan", str(df["scan_time"].max()))

st.divider()

# --------------------------------------------------
# TOP OPPORTUNITIES
# --------------------------------------------------

st.subheader("🔥 Top Opportunities")

top10 = df.sort_values("score", ascending=False).head(10)

st.dataframe(
    top10[["symbol", "signal", "score", "close", "rsi", "macd"]],
    use_container_width=True
)

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

st.subheader("📊 Top Ranked Stocks")

fig = px.bar(top10, x="symbol", y="score", color="score", text="score")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 RSI vs Score")

fig2 = px.scatter(
    top10,
    x="rsi",
    y="score",
    color="score",
    size="score",
    hover_name="symbol"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.divider()
st.subheader("🔍 Search Stock")

search_symbol = st.text_input("Enter Symbol", placeholder="Example: RELIANCE")

if search_symbol:
    search_df = df[df["symbol"].str.contains(search_symbol.upper(), na=False)]
    st.dataframe(search_df, use_container_width=True)

# --------------------------------------------------
# WATCHLIST
# --------------------------------------------------

WATCHLIST = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "SBIN.NS", "BEL.NS"]

st.divider()
st.subheader("⭐ Watchlist")

watchlist_df = df[df["symbol"].isin(WATCHLIST)]

if len(watchlist_df):
    st.dataframe(
        watchlist_df[["symbol", "signal", "score", "close", "rsi"]],
        use_container_width=True
    )
else:
    st.info("No watchlist stocks found")

# --------------------------------------------------
# ALL STOCKS
# --------------------------------------------------

st.divider()
st.subheader("📋 Complete Ranking")

st.dataframe(
    df.sort_values("score", ascending=False),
    use_container_width=True,
    height=600
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption("Trade Predictor | PostgreSQL Dashboard")