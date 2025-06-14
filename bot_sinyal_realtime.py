import requests
import datetime
import os
import schedule
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = os.environ.get("CHANNEL")

def get_xau_price():
    try:
        resp = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=XAU")
        data = resp.json()
        # 1 XAU = x USD, dibalik untuk 1 USD = x AU
        price_usd = 1 / data["rates"]["XAU"]
        return round(price_usd, 2)
    except Exception as e:
        print("Error ambil XAU:", e)
        return None

def send_update():
    now = datetime.datetime.now().strftime('%d %b %Y – %H:%M WIB')
    xau = get_xau_price()
    if not xau:
        msg = f"❌ Gagal ambil harga XAU pada {now}"
    else:
        sinyal = "BUY 💹" if xau < 2300 else "SELL 🟢"
        support = round(xau - 10, 2)
        resistant = round(xau + 10, 2)
        msg = f"""
📊 Update Pasar: {now}

🔥 Pasangan: XAU/USD  
💰 Harga Saat Ini: {xau} USD

📈 Sinyal: {sinyal}  
📉 Support: {support}  
📊 Resistance: {resistant}

📌 Gunakan analisa tambahan & money management.
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHANNEL, 'text': msg}
    try:
        requests.post(url, data=payload)
        print("✅ Sinyal berhasil dikirim")
    except Exception as e:
        print("❌ Gagal kirim:", e)

# Jadwal otomatis kirim 3x sehari
schedule.every().day.at("06:00").do(send_update)
schedule.every().day.at("16:00").do(send_update)
schedule.every().day.at("19:00").do(send_update)

if __name__ == "__main__":
    send_update()
    while True:
        schedule.run_pending()
        time.sleep(30)
