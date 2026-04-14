import streamlit as st
import yfinance as yf
import json

st.set_page_config(layout="wide")

# ส่วนที่ 1: รับชื่อหุ้นจาก Streamlit
ticker = st.text_input("🔍 กรอกชื่อหุ้น (เช่น ICHI, PTT):", "").upper()

# อ่านไฟล์ HTML ของคุณขึ้นมา
try:
    with open("TFRS_Valuation_Live.html", "r", encoding="utf-8") as f:
        html_content = f.read()
except FileNotFoundError:
    st.error("ไม่พบไฟล์ TFRS_Valuation_Live.html ในโฟลเดอร์เดียวกัน")
    st.stop()

if ticker:
    try:
        # ส่วนที่ 2: ดึงข้อมูลจาก Yahoo Finance
        stock = yf.Ticker(f"{ticker}.BK")
        info = stock.info
        
        # จัดเตรียมข้อมูลที่จะส่งไป
        stock_data = {
            "ticker": ticker,
            "name": info.get('longName', 'ไม่พบชื่อบริษัท'),
            "currentPrice": info.get('currentPrice', 0),
            "sharesOutstanding": info.get('sharesOutstanding', 0) / 1_000_000, # ทำเป็นหน่วยล้านหุ้น
            "beta": info.get('beta', 1.0)
        }
        
        # ส่วนที่ 3: ฝัง JavaScript ลงใน HTML เพื่อเอาข้อมูลไปกรอกในช่อง
        js_injection = f"""
        <script>
            window.addEventListener('load', function() {{
                const data = {json.dumps(stock_data)};
                if(document.getElementById('ticker-input')) document.getElementById('ticker-input').value = data.ticker;
                if(document.getElementById('company-name')) document.getElementById('company-name').value = data.name;
                if(document.getElementById('current-price')) document.getElementById('current-price').value = data.currentPrice;
                if(document.getElementById('shares-out')) document.getElementById('shares-out').value = data.sharesOutstanding;
                if(document.getElementById('beta-input')) document.getElementById('beta-input').value = data.beta;
                
                // สั่งให้ฟังก์ชันคำนวณใน HTML ทำงานทันที
                if(typeof calculateAll === 'function') calculateAll();
            }});
        </script>
        """
        # ใส่ JavaScript เข้าไปก่อนปิด </body>
        html_content = html_content.replace("</body>", f"{js_injection}</body>")
        
    except Exception as e:
        st.warning(f"ดึงข้อมูลหุ้น {ticker} ไม่สำเร็จ: {e}")

# แสดงผลหน้า HTML
st.components.v1.html(html_content, height=1200, scrolling=True)
