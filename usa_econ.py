import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class EconomicAnalyzer:
    """
    ABD Ekonomik Veri Analizi ve Tahmin Sistemi
    FRED API kullanarak güncel ekonomik verileri çeker ve analiz eder
    """
    
    def __init__(self, fred_api_key: str):
        """
        API anahtarı https://fred.stlouisfed.org/docs/api/api_key.html adresinden alınabilir
        """
        self.fred_api_key = fred_api_key
        self.base_url = "https://api.stlouisfed.org/fred"
        
        self.indicators = {
            'UNRATE': 'İşsizlik Oranı (%)',
            'CPIAUCSL': 'Enflasyon (CPI)',
            'GDPC1': 'Reel GSYİH',
            'FEDFUNDS': 'Fed Faiz Oranı (%)',
            'PAYEMS': 'İstihdam Dışı Tarım Sektörü (NFP)',
            'INDPRO': 'Sanayi Üretimi',
            'HOUST': 'Konut Başlangıçları',
            'UMCSENT': 'Tüketici Güven Endeksi',
            'DEXUSEU': 'USD/EUR Kuru',
            'DGS10': '10 Yıllık Tahvil Faizi (%)',
            'MANEMP': 'İmalat Sektörü İstihdamı',
            'CIVPART': 'İş Gücüne Katılım Oranı',
            'GPDI': 'Brüt Özel Yatırım',
            'PCEC96': 'Reel Kişisel Tüketim Harcamaları'
        }
        
        self.risk_levels = {
            'LOW': '🟢 Düşük Risk',
            'MEDIUM': '🟡 Orta Risk', 
            'HIGH': '🔴 Yüksek Risk'
        }
    
    def get_fred_data(self, series_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """FRED API'den veri çek"""
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            url = f"{self.base_url}/series/observations"
            params = {
                'series_id': series_id,
                'api_key': self.fred_api_key,
                'file_type': 'json',
                'start_date': start_date,
                'end_date': end_date,
                'sort_order': 'desc',
                'limit': 100
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'observations' in data:
                df = pd.DataFrame(data['observations'])
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df.dropna(subset=['value'])
                df = df.sort_values('date')
                return df
            else:
                print(f"⚠️ {series_id} için veri bulunamadı")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"❌ {series_id} verisi çekilirken hata: {str(e)}")
            return pd.DataFrame()
    
    def calculate_trend(self, df: pd.DataFrame, periods: int = 3) -> str:
        """Trend analizi yap"""
        if len(df) < periods:
            return "Yetersiz veri"
        
        recent_values = df.tail(periods)['value'].values
        
        if len(recent_values) < 2:
            return "Kararsız"
        
        changes = np.diff(recent_values)
        avg_change = np.mean(changes)
        
        if avg_change > 0.1:
            return "📈 Güçlü Yükseliş"
        elif avg_change > 0.01:
            return "🔼 Hafif Yükseliş"
        elif avg_change < -0.1:
            return "📉 Güçlü Düşüş"
        elif avg_change < -0.01:
            return "🔽 Hafif Düşüş"
        else:
            return "➡️ Stabil"
    
    def analyze_volatility(self, df: pd.DataFrame) -> str:
        if len(df) < 10:
            return "Yetersiz veri"
        
        returns = df['value'].pct_change().dropna()
        volatility = returns.std()
        
        if volatility > 0.1:
            return "⚡ Yüksek Volatilite"
        elif volatility > 0.05:
            return "🌊 Orta Volatilite"
        else:
            return "🌊 Düşük Volatilite"
    
    def get_market_sentiment(self, data_dict: Dict) -> Tuple[str, str]:
        positive_signals = 0
        negative_signals = 0
        total_signals = 0
        
        key_indicators = {
            'UNRATE': 'negative',  # İşsizlik yüksek = negatif
            'CPIAUCSL': 'negative',  # Enflasyon yüksek = negatif
            'FEDFUNDS': 'negative',  # Faiz yüksek = negatif
            'PAYEMS': 'positive',  # İstihdam artışı = pozitif
            'UMCSENT': 'positive',  # Tüketici güveni = pozitif
            'INDPRO': 'positive'   # Sanayi üretimi = pozitif
        }
        
        for indicator, effect in key_indicators.items():
            if indicator in data_dict:
                df = data_dict[indicator]
                if len(df) >= 2:
                    recent_change = df.iloc[-1]['value'] - df.iloc[-2]['value']
                    if effect == 'positive':
                        if recent_change > 0:
                            positive_signals += 1
                        else:
                            negative_signals += 1
                    else:
                        if recent_change > 0:
                            negative_signals += 1
                        else:
                            positive_signals += 1
                    total_signals += 1
        
        if total_signals == 0:
            return "🤷 Belirsiz", "MEDIUM"
        
        positive_ratio = positive_signals / total_signals
        
        if positive_ratio >= 0.7:
            return "🟢 Pozitif", "LOW"
        elif positive_ratio >= 0.4:
            return "🟡 Nötr", "MEDIUM"
        else:
            return "🔴 Negatif", "HIGH"
    
    def generate_trading_signals(self, data_dict: Dict) -> List[str]:
        signals = []
        
        try:
            if 'FEDFUNDS' in data_dict and len(data_dict['FEDFUNDS']) >= 3:
                fed_data = data_dict['FEDFUNDS']
                recent_fed = fed_data.tail(3)['value'].values
                if len(recent_fed) >= 2:
                    fed_trend = recent_fed[-1] - recent_fed[-2]
                    if fed_trend < -0.25:
                        signals.append("🟢 AL: Fed faiz indirimi - risk iştahı artabilir")
                    elif fed_trend > 0.25:
                        signals.append("🔴 SAT: Fed faiz artışı - risk iştahı azalabilir")
            
            if 'UNRATE' in data_dict and 'CPIAUCSL' in data_dict:
                unemployment_trend = self.calculate_trend(data_dict['UNRATE'])
                inflation_trend = self.calculate_trend(data_dict['CPIAUCSL'])
                
                if "Düşüş" in unemployment_trend and "Düşüş" in inflation_trend:
                    signals.append("🟢 AL: İşsizlik ve enflasyon düşüyor - ideal makro ortam")
                elif "Yükseliş" in unemployment_trend and "Yükseliş" in inflation_trend:
                    signals.append("🔴 SAT: Stagflasyon riski - ekonomik zorluk")
            
            if 'UMCSENT' in data_dict and len(data_dict['UMCSENT']) >= 2:
                consumer_data = data_dict['UMCSENT']
                recent_consumer = consumer_data.tail(2)['value'].values
                if len(recent_consumer) >= 2:
                    consumer_change = recent_consumer[-1] - recent_consumer[-2]
                    if consumer_change > 5:
                        signals.append("🟢 AL: Tüketici güveni güçlü artış")
                    elif consumer_change < -5:
                        signals.append("🔴 SAT: Tüketici güveni zayıflıyor")
            
            if 'PAYEMS' in data_dict and len(data_dict['PAYEMS']) >= 2:
                employment_data = data_dict['PAYEMS']
                recent_employment = employment_data.tail(2)['value'].values
                if len(recent_employment) >= 2:
                    employment_change = recent_employment[-1] - recent_employment[-2]
                    if employment_change > 200:  # 200K üzeri istihdam artışı
                        signals.append("🟢 AL: Güçlü istihdam artışı")
                    elif employment_change < -50:
                        signals.append("🔴 SAT: İstihdam kaybı")
            
        except Exception as e:
            print(f"Sinyal üretiminde hata: {str(e)}")
        
        if not signals:
            signals.append("🟡 BEKLE: Net sinyal yok - dikkatli ol")
        
        return signals
    
    def predict_next_day_events(self, data_dict: Dict) -> List[str]:
        predictions = []
        
        try:
            for indicator, name in self.indicators.items():
                if indicator in data_dict:
                    df = data_dict[indicator]
                    if len(df) >= 5:
                        trend = self.calculate_trend(df, periods=5)
                        volatility = self.analyze_volatility(df)
                        
                        if "Güçlü Yükseliş" in trend:
                            predictions.append(f"📈 {name}: Yükseliş devam edebilir")
                        elif "Güçlü Düşüş" in trend:
                            predictions.append(f"📉 {name}: Düşüş devam edebilir")
                        elif "Yüksek Volatilite" in volatility:
                            predictions.append(f"⚡ {name}: Yüksek volatilite beklentisi")
            
            sentiment, risk = self.get_market_sentiment(data_dict)
            
            if "Pozitif" in sentiment:
                predictions.append("🌟 Genel görünüm: Pozitif momentum sürebilir")
            elif "Negatif" in sentiment:
                predictions.append("⚠️ Genel görünüm: Negatif baskı devam edebilir")
            
            # Fed politika tahmini
            if 'FEDFUNDS' in data_dict and 'CPIAUCSL' in data_dict:
                fed_data = data_dict['FEDFUNDS']
                inflation_data = data_dict['CPIAUCSL']
                
                if len(fed_data) >= 2 and len(inflation_data) >= 2:
                    current_fed_rate = fed_data.iloc[-1]['value']
                    inflation_trend = self.calculate_trend(inflation_data)
                    
                    if current_fed_rate > 4.5 and "Düşüş" in inflation_trend:
                        predictions.append("🔮 Fed tahmini: Faiz indirimi sinyalleri güçlenebilir")
                    elif current_fed_rate < 3.0 and "Yükseliş" in inflation_trend:
                        predictions.append("🔮 Fed tahmini: Faiz artışı beklentisi artabilir")
            
        except Exception as e:
            print(f"Tahmin üretiminde hata: {str(e)}")
        
        if not predictions:
            predictions.append("🔮 Mevcut verilerle net tahmin zor - piyasa takibi önemli")
        
        return predictions[:5]
    
    def run_daily_analysis(self) -> str:
        """Günlük analiz raporu oluştur"""
        print("🔄 Ekonomik veri analizi başlatılıyor...")
        print("📊 Veriler çekiliyor...")
        
        data_dict = {}
        for indicator in self.indicators.keys():
            df = self.get_fred_data(indicator)
            if not df.empty:
                data_dict[indicator] = df
            time.sleep(0.1)  # API rate limiting
        
        print("🧮 Analiz yapılıyor...")
        
        report = []
        report.append("=" * 80)
        report.append("📈 ABD EKONOMİK VERİ ANALİZİ RAPORU")
        report.append("=" * 80)
        report.append(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("📊 GÜNCEL EKONOMİK GÖSTERGELER")
        report.append("-" * 50)
        
        for indicator, name in self.indicators.items():
            if indicator in data_dict:
                df = data_dict[indicator]
                if not df.empty:
                    latest_value = df.iloc[-1]['value']
                    latest_date = df.iloc[-1]['date'].strftime('%Y-%m-%d')
                    trend = self.calculate_trend(df)
                    
                    report.append(f"{name}: {latest_value:.2f} ({latest_date}) - {trend}")
        
        report.append("")
        
        sentiment, risk_level = self.get_market_sentiment(data_dict)
        report.append("🎯 PİYASA DUYARLILIĞI")
        report.append("-" * 50)
        report.append(f"Genel Durum: {sentiment}")
        report.append(f"Risk Seviyesi: {self.risk_levels[risk_level]}")
        report.append("")
        
        signals = self.generate_trading_signals(data_dict)
        report.append("🎯 AL/SAT SİNYALLERİ")
        report.append("-" * 50)
        for signal in signals:
            report.append(f"• {signal}")
        report.append("")
        
        predictions = self.predict_next_day_events(data_dict)
        report.append("🔮 YARIN İÇİN TAHMİNLER")
        report.append("-" * 50)
        for prediction in predictions:
            report.append(f"• {prediction}")
        report.append("")
        
        report.append("💡 STRATEJİK ÖNERİLER")
        report.append("-" * 50)
        
        if risk_level == "HIGH":
            report.append("• ⚠️ Yüksek risk ortamı - pozisyon boyutlarını küçült")
            report.append("• 🛡️ Hedge stratejileri değerlendir")
            report.append("• 📰 Fed açıklamalarını yakından takip et")
        elif risk_level == "MEDIUM":
            report.append("• ⚖️ Dengeli yaklaşım - makro verileri izle")
            report.append("• 📊 Teknik analiz ile kombine et")
            report.append("• 🎯 Seçici olmaya odaklan")
        else:
            report.append("• 🟢 Düşük risk ortamı - fırsatları değerlendir")
            report.append("• 📈 Trend takibi stratejileri uygula")
            report.append("• 💪 Pozisyon boyutlarını artırabilirsin")
        
        report.append("")
        report.append("=" * 80)
        report.append("⚡ Analiz tamamlandı! Başarılı yatırımlar dilerim.")
        report.append("=" * 80)
        
        return "\n".join(report)

if __name__ == "__main__":
    FRED_API_KEY = "YOUR_FRED_API_KEY_HERE"

    
    if FRED_API_KEY == "YOUR_FRED_API_KEY_HERE":
        print("❌ FRED API anahtarı gerekli!")
        print("📝 https://fred.stlouisfed.org/docs/api/api_key.html adresinden API anahtarı alın")
        print("🔧 Kodu düzenleyerek API anahtarınızı girin")
    else:
        analyzer = EconomicAnalyzer(FRED_API_KEY)
        
        report = analyzer.run_daily_analysis()
        print(report)
        
        # Raporu dosyaya kaydet
        with open(f"economic_report_{datetime.now().strftime('%Y%m%d')}.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n📄 Rapor kaydedildi: economic_report_{datetime.now().strftime('%Y%m%d')}.txt")
