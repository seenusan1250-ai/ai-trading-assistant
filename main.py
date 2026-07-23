from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# --- Telegram Credentials ---
TELEGRAM_BOT_TOKEN = "8992002085:AAGvMjDhDGmEt904ufAGBiAchqnZpJJix"
TELEGRAM_CHAT_ID = "6669637975"

def send_bangla_telegram_alert(data):
    action = data.get("action", "BUY")
    symbol = data.get("symbol", "XAU/USD")
    price = float(data.get("price", 0.0))
    sl = float(data.get("sl", 0.0))
    tp = float(data.get("tp", 0.0))
    reason = data.get("reason", "ক্যান্ডেলস্টিক প্যাটার্ন ও কি-লেভেল কনফার্মেশন")
    confidence = data.get("confidence", "85%")
    risk = data.get("risk", "1%")

    icon = "🟢" if action == "BUY" else "🔴"

    message = f"""
{icon} **AI TRADING ALERT: {action} ({symbol})**

📍 **Entry Price:** {price}
🛡️ **Stop Loss (SL):** {sl}
🎯 **Take Profit (TP):** {tp}

💡 **সিম্পল ট্রেড এনালাইসিস (কারণ):**
{reason}

📊 **কনফিডেন্স লেভেল:** {confidence}
⚠️ **রিকমেন্ডেড রিস্ক:** {risk}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending telegram message: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        send_bangla_telegram_alert(data)
        return jsonify({"status": "success", "message": "Telegram Alert Sent!"}), 200
    return jsonify({"status": "error", "message": "No data received"}), 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
