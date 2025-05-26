```python
import streamlit as st
import pandas as pd
import yfinance as yf

# Fetch and clean price data
def fetch_price_history(symbol, period='7d', interval='5m'):
    df = yf.download(symbol, period=period, interval=interval)
    df.reset_index(inplace=True)
    return df[['Date', 'Close']].dropna()

# Compute EMA34, EMA89, SMA50 and score
def compute_ma_scores(df):
    df['ema34'] = df['Close'].ewm(span=34, adjust=False).mean()
    df['ema89'] = df['Close'].ewm(span=89, adjust=False).mean()
    df['sma50'] = df['Close'].rolling(window=50).mean()

    latest = df.iloc[-1]
    score = 0
    details = {}
    if latest['Close'] > latest['ema34']:
        score += 1; details['Above EMA34'] = True
    if latest['Close'] > latest['ema89']:
        score += 1; details['Above EMA89'] = True
    if latest['Close'] > latest['sma50']:
        score += 1; details['Above SMA50'] = True
    if latest['ema34'] > latest['ema89']:
        score += 1; details['EMA34 > EMA89'] = True

    return score, details, df

# Streamlit UI layout
st.set_page_config(page_title="A++ Options Trading MA Dashboard", layout="wide")
st.title("A++ Options Trading MA Dashboard")

symbol = st.sidebar.text_input("Symbol", "SPY")
period = st.sidebar.selectbox("Period", ['1d','5d','7d','1mo'])
interval = st.sidebar.selectbox("Interval", ['1m','5m','15m','1h'])

with st.spinner("Fetching price data..."):
    price_df = fetch_price_history(symbol, period, interval)
score, details, df = compute_ma_scores(price_df)

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("MA Confluence Score", score)
    for k in details:
        st.write(f"- {k}")
with col2:
    df_plot = df.set_index('Date')[['Close', 'ema34', 'ema89', 'sma50']]
    st.line_chart(df_plot)

st.markdown("---")
st.info("This app uses yfinance for data and pandas for moving averages. Deploy on Streamlit Cloud!")
```
