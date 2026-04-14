import streamlit as st
import yfinance as yf

st.set_page_config(layout="wide")

# ส่วนรับค่า
ticker = st.text_input("🔍 พิมพ์ชื่อหุ้น (เช่น ICHI):", "").upper()

# อ่านไฟล์ HTML
with open("TFRS_Valuation_Live.html", "r", encoding="utf-8") as f:
    html = f.read()

if ticker:
    try:
        # ดึงข้อมูล
        stock = yf.Ticker(f"{ticker}.BK")
        info = stock.info
        
        # เตรียมข้อมูล (แก้ไขชื่อ ID ให้ตรงกับไฟล์ HTML ของคุณ)
        data_js = f"""
        <script>
            window.addEventListener('load', () => {{
                if(document.getElementById('ticker-input')) document.getElementById('ticker-input').value = '{ticker}';
                if(document.getElementById('company-name')) document.getElementById('company-name').value = '{info.get('longName', '')}';
                if(document.getElementById('current-price')) document.getElementById('current-price').value = '{info.get('currentPrice', 0)}';
                if(document.getElementById('shares-out')) document.getElementById('shares-out').value = '{info.get('sharesOutstanding', 0)}';
                if(document.getElementById('beta-input')) document.getElementById('beta-input').value = '{info.get('beta', 1.0)}';
                
                // สั่งคำนวณใหม่
                if(typeof calculateAll === 'function') calculateAll();
            }});
        </script>
        """
        html = html.replace("</body>", f"{data_js}</body>")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")

st.components.v1.html(html, height=1000, scrolling=True)
