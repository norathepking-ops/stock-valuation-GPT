import streamlit as st
import yfinance as yf
import json

st.set_page_config(layout="wide")

ticker = st.text_input("ใส่ Ticker (เช่น ICHI, TACC)")

data = {}

if ticker:
    try:
        symbol = ticker.upper() + ".BK"
        stock = yf.Ticker(symbol)

        info = stock.info
        fin = stock.financials
        bs = stock.balance_sheet
        cf = stock.cashflow

        data = {
            "name": info.get("longName"),
            "price": info.get("currentPrice"),
            "shares": info.get("sharesOutstanding"),
            "marketCap": info.get("marketCap"),
            "sector": info.get("sector"),
            "beta": info.get("beta"),
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "divYield": info.get("dividendYield"),
        }

    except Exception as e:
        st.error(f"Error: {e}")

# โหลด HTML
with open("TFRS_Valuation_Live.html", "r", encoding="utf-8") as f:
    html = f.read()

# inject data เข้า HTML
html = html.replace(
    "/*PYTHON_DATA_HERE*/",
    f"const PY_DATA = {json.dumps(data)};"
)

st.components.v1.html(html, height=900, scrolling=True)
