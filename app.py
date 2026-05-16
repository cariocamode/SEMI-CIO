from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime

app = Flask(__name__)
CORS(app)

TICKERS = {
    "SEMI":  "SEMI",
    "SMH":   "SMH",
    "ASML":  "ASML",
    "AMAT":  "AMAT",
    "KLAC":  "KLAC",
    "TSM":   "TSM",
    "MU":    "MU",
    "SMSN":  "0593.HK",
    "LRCX":  "LRCX",
    "AVGO":  "AVGO",
    "NVDA":  "NVDA",
}

@app.route("/")
def home():
    return "Semi CIO — Live Tracker actif", 200

@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "time": datetime.now().strftime("%H:%M:%S")}), 200

@app.route("/prices")
def get_prices():
    results = {}
    for name, sym in TICKERS.items():
        try:
            t = yf.Ticker(sym)
            info = t.fast_info
            price = round(float(info["last_price"]), 2)
            prev  = round(float(info["previous_close"]), 2)
            chg   = round(((price - prev) / prev) * 100, 2)
            results[name] = {
                "price": price,
                "prev":  prev,
                "chg":   chg,
                "ok":    True
            }
        except Exception as e:
            results[name] = {"price": None, "ok": False, "error": str(e)}

    return jsonify({
        "prices":  results,
        "updated": datetime.now().strftime("%H:%M:%S"),
        "date":    datetime.now().strftime("%d/%m/%Y")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
