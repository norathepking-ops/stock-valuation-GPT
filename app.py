import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="TFRS Valuation Live")

# 1. ส่วนดึงข้อมูลหุ้น (Python)
ticker = st.text_input("กรอกชื่อหุ้น (เช่น ICHI, PTT):", "").upper()
stock_data = {}

if ticker:
    try:
        if not ticker.endswith(".BK"):
            search_ticker = f"{ticker}.BK"
        else:
            search_ticker = ticker
            
        data = yf.Ticker(search_ticker)
        info = data.info
        
        # เตรียมข้อมูลเพื่อส่งไปให้ HTML
        stock_data = {
            "symbol": ticker,
            "shortName": info.get('shortName', ticker),
            "currentPrice": info.get('currentPrice', 0),
            "marketCap": info.get('marketCap', 0) / 1_000_000, # หน่วยล้าน
            "shares": info.get('sharesOutstanding', 0) / 1_000_000,
            "beta": info.get('beta', 1.0)
        }
    except Exception as e:
        st.error(f"ไม่พบข้อมูลหุ้น {ticker}")

# 2. อ่านไฟล์ HTML ของคุณ
with open("TFRS_Valuation_Live.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 3. ใส่ JavaScript เพื่อเอาข้อมูลจาก Python ไปหยอดลงช่องใน HTML
if stock_data:
    inject_js = f"""
    <script>
        window.addEventListener('load', function() {{
            // หยอดข้อมูลลงใน ID ต่างๆ ของคุณ
            document.getElementById('a_ticker').value = "{stock_data['symbol']}";
            document.getElementById('a_company').value = "{stock_data['shortName']}";
            document.getElementById('a_price').value = {stock_data['currentPrice']};
            document.getElementById('a_mktcap').value = {stock_data['marketCap']};
            document.getElementById('a_shares').value = {stock_data['shares']};
            document.getElementById('a_beta').value = {stock_data['beta']};
            
            // สั่งให้ HTML คำนวณใหม่ทันที
            if(typeof calculateAll === 'function') calculateAll();
        }});
    </script>
    """
    html_content = html_content.replace("</body>", f"{inject_js}</body>")

# 4. แสดงผล
st.components.v1.html(html_content, height=1200, scrolling=True)
