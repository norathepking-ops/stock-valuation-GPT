import streamlit as st
import yfinance as yf
import json

st.set_page_config(layout="wide")

# 1. สร้างช่องรับชื่อหุ้นในฝั่ง Streamlit
st.title("TFRS Equity Valuation")
ticker_input = st.text_input("🔍 ใส่ชื่อย่อหุ้นไทย (เช่น ICHI, TACC)", "")

# ตัวแปรเก็บข้อมูลที่จะส่งไป HTML
stock_data = {}

if ticker_input:
    # หุ้นไทยใน Yahoo Finance ต้องลงท้ายด้วย .BK เสมอ
    symbol = ticker_input.strip().upper()
    if not symbol.endswith(".BK"):
        symbol += ".BK"
    
    with st.spinner(f"กำลังดึงข้อมูล {symbol} จาก Yahoo Finance..."):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # 2. ดึงข้อมูลล่าสุด (ใส่เพิ่มเติมได้ตามต้องการ)
            stock_data = {
                "ticker": symbol.replace(".BK", ""),
                "name": info.get("longName", "-"),
                "industry": info.get("industry", "-"),
                "sector": info.get("sector", "-"),
                "currentPrice": info.get("currentPrice", 0),
                "sharesOutstanding": info.get("sharesOutstanding", 0),
                "beta": info.get("beta", 1.0), # สำหรับ WACC
                "marketCap": info.get("marketCap", 0)
            }
            
            # หมายเหตุ: สำหรับงบการเงินแบบละเอียด (Revenue, Net Income) 
            # สามารถดึงผ่าน stock.financials ได้ แต่ต้องจัดรูป format ให้ตรงกับ HTML
            
        except Exception as e:
            st.error(f"ไม่พบข้อมูล หรือเกิดข้อผิดพลาด: {e}")

# 3. อ่านไฟล์ HTML
with open("TFRS_Valuation_Live.html", "r", encoding="utf-8") as f:
    html = f.read()

# 4. นำข้อมูล JSON ฝังเข้าไปใน HTML ผ่าน <script>
if stock_data:
    json_data = json.dumps(stock_data)
    inject_script = f"""
    <script>
        // รับข้อมูลจาก Python
        window.stStockData = {json_data};
    </script>
    """
    # แทรก script ไว้ก่อนปิด </head>
    html = html.replace("</head>", f"{inject_script}</head>")

# แสดงผล HTML
st.components.v1.html(html, height=900, scrolling=True)
