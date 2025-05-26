# streamlit_app.py
# requirements.txt
# ------------
# streamlit
# pandas
# yfinance
# ta

# A++ Options Trading MA Dashboard - Streamlit Deployment Instructions
# A++ Options Trading MA Dashboard - Streamlit Deployment Instructions
# ---------------------------------------------------------------
# LOCAL RUN INSTRUCTIONS:
# 1. Ensure Python 3.8+ is installed.
# 2. Create a virtual environment:
#    python3 -m venv venv
#    source venv/bin/activate  # on Windows: venv\\Scripts\\activate
# 3. Install dependencies:
#    pip install -r requirements.txt
# 4. Run the app:
#    streamlit run streamlit_app.py
#
# DEPLOYMENT TO STREAMLIT CLOUD:
# 1. Create a GitHub repo and add this file as streamlit_app.py.
# 2. Add requirements.txt with:
#      streamlit
#      pandas
#      yfinance
#      ta
# 3. (Optional) runtime.txt with `python-3.10` to pin version.
# 4. Push to GitHub and connect on Streamlit Community Cloud.
# 5. Set main file: streamlit_app.py. Enjoy zero-config free hosting!

import streamlit as st
import pandas as pd
import yfinance as yf
from ta.trend import EMAIndicator, SMAIndicator

st.set_page_config(page_title="A++ Options Dashboard", layout="wide")

# Caching data fetches for minimal config
def fetch_price_history(symbol, period='7d', interval='5m'):
    data = yf.download(symbol, period=period, interval=interval)
    data.reset_index(inplace=True)
    return data

# Compute MA scores inline
def compute_ma_scores(df):
    df['ema34'] = EMAIndicator(df['Close'], window=34).ema_indicator()
    df['ema89'] = EMAIndicator(df['Close'], window=89).ema_indicator()
    df['sma50'] = SMAIndicator(df['Close'], window=50).sma_indicator()
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

# UI layout
st.title("A++ Options Trading MA Dashboard")
symbol = st.sidebar.text_input("Symbol", value="SPY")
period = st.sidebar.selectbox("Period", ['1d','5d','7d','1mo'])
interval = st.sidebar.selectbox("Interval", ['1m','5m','15m','1h'])

# Fetch and compute
with st.spinner("Fetching price data..."):
    price_df = fetch_price_history(symbol, period, interval)
score, details, df = compute_ma_scores(price_df)

# Display metrics
col1, col2 = st.columns([1,2])
with col1:
    st.metric("MA Confluence Score", score)
    for k,v in details.items(): st.write(f"- {k}")
with col2:
    st.line_chart(df[['Close','ema34','ema89','sma50']].set_index('Date'))

st.markdown("---")
st.info("This free Streamlit app uses yfinance for price data and TA for moving average indicators. No configuration needed—just deploy on Streamlit Cloud!")
