````markdown
# 🧠 US Economic Insights

A Python-based analysis tool that retrieves key macroeconomic indicators from the FRED API (like CPI, NFP, interest rates), analyzes today's data, forecasts possible market behavior for the next day, and generates **basic trading signals** based on macro trends and sentiment.

---

## 🚀 Features

- 📊 Real-time economic data retrieval via [FRED API](https://fred.stlouisfed.org/)
- 🔎 Trend and volatility analysis of major indicators
- 📈 Market sentiment evaluation
- 💡 Buy/Sell signal generation based on macro context
- 🔮 Forecasts on upcoming economic data impact
- 📝 Saves full daily report in `.txt` format

---

## 📦 Dependencies

Install required packages:

```bash
pip install requests pandas numpy
````

If you're using a fresh environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt  # (optional if you create one)
```

---

## 🔑 FRED API Key Setup

You need an API key from the Federal Reserve Economic Data (FRED):

1. Go to [https://fred.stlouisfed.org/docs/api/api\_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Register (free) and get your API key.
3. Replace this line in the script:

```python
FRED_API_KEY = "YOUR_FRED_API_KEY_HERE"
```

---

## 🧪 How to Use

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/us-economic-insights.git
cd us-economic-insights
```

2. Edit the script and paste your FRED API key:

```python
FRED_API_KEY = "your_actual_fred_key"
```

3. Run the script:

```bash
python economic_analyzer.py
```

4. Output:

* A detailed analysis will be printed in the terminal.
* The same content will be saved to a file like:
  `economic_report_20250703.txt`

---

## 📁 Output Example

```
📈 ABD EKONOMİK VERİ ANALİZİ RAPORU
📅 Tarih: 2025-07-03 14:30:02

📊 GÜNCEL EKONOMİK GÖSTERGELER
İstihdam Dışı Tarım Sektörü: 152300.0 (2025-06-01) - 📈 Güçlü Yükseliş
Fed Faiz Oranı: 5.25 (2025-06-01) - ➡️ Stabil
...

🎯 AL/SAT SİNYALLERİ
• 🔴 SAT: Fed faiz artışı - risk iştahı azalabilir
• 🟢 AL: Tüketici güveni güçlü artış

🔮 YARIN İÇİN TAHMİNLER
• 📈 Enflasyon (CPI): Yükseliş devam edebilir
• ⚡ Tüketici Güven Endeksi: Yüksek volatilite beklentisi

💡 STRATEJİK ÖNERİLER
• ⚠️ Yüksek risk ortamı - pozisyon boyutlarını küçült
• 🛡️ Hedge stratejileri değerlendir
```

---

## 📌 Notes

* There are short delays between API calls (0.1s) to comply with FRED's rate limits.
* Code comments are written in Turkish, while data structures and analysis logic follow standard English terminology and conventions.
---

## 📃 License

MIT License

---

## 🤝 Contributions

Pull requests are welcome. If you'd like to improve indicator coverage or add new models (e.g., ML-based forecast), feel free to contribute!
---

## ⚠️ Disclaimer

This project is for **educational and informational purposes only** and should **not be considered investment advice**. Always do your own research and consult with a qualified financial advisor before making any investment decisions.
---

## ⚠️ Uyarı

Bu proje **yalnızca eğitim ve bilgilendirme amacıyla** hazırlanmıştır, **yatırım tavsiyesi değildir**. Her zaman kendi araştırmanızı yapmalı ve yatırım kararlarınızı almadan önce uzman bir danışmana başvurmalısınız.
