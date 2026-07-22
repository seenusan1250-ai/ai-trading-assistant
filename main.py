from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- Telegram Credentials ---
TELEGRAM_BOT_TOKEN = "8992002085:AAGvMjDhDGmEt904ufAGBiAchqnZpJJix18"
TELEGRAM_CHAT_ID = "6669637975"

def send_bangla_telegram_alert(data):
    action = data.get("action", "BUY")
    symbol = data.get("symbol", "XAU/USD")
    price = float(data.get("price", 0.0))
    sl = float(data.get("sl", 0.0))
    tp = float(data.get("tp", 0.0))
    reason = data.get("reason", "ক্যান্ডেলস্টিক প্যাটার্ন ও কি-লেভেল কনফার্মেশন পাওয়া গেছে।")
    confidence = data.get("confidence", "85%")
    risk = data.get("risk", "1%")

    icon = "🟢" if action == "BUY" else "🔴"

    message = f"""
{icon} **AI TRADING ALERT: {action} ({symbol})**

📊 **এন্ট্রি প্রাইস:** {price:.2f}
🛑 **স্টপ লস (SL):** {sl:.2f}
🏁 **টেক প্রফিট (TP):** {tp:.2f}

🧠 **ট্রেড নেওয়ার কারণ:** {reason}
⚖️ **রিস্ক ম্যানেজমেন্ট:** {risk}
🔥 **কনফিডেন্স স্কোর:** {confidence}

🤖 *Chiku AI Assistant দ্বারা স্বয়ংক্রিয়ভাবে প্রসেস করা হয়েছে!*
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route('/')
def home():
    return "AI Trading Assistant Backend is Active 24/7!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if data:
            send_bangla_telegram_alert(data)
            return jsonify({"status": "success", "message": "Telegram Alert Sent!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
