"""
Para Komuta Merkezi - Ana Web Sitesi
Tüm uygulamaları tek çatı altında toplayan merkezi portal
"""

from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = 'para-komuta-merkezi-2025'

# Uygulamaların bilgileri
APPLICATIONS = [
    {
        'id': 'portfoy',
        'name': 'Portföy Komuta Merkezi',
        'description': 'Portföy yönetimi, varlık takibi ve performans analizi',
        'icon': 'fa-wallet',
        'color': 'green',
        'port': 5000,
        'url': 'http://localhost:5000',
        'features': ['Varlık Takibi', 'Performans Analizi', 'Otomatik Güncellemeler']
    },
    {
        'id': 'kap',
        'name': 'KAP Arşivi',
        'description': 'KAP bildirimleri takibi ve arşivleme sistemi',
        'icon': 'fa-file-alt',
        'color': 'blue',
        'port': 5002,
        'url': 'http://localhost:5002',
        'features': ['Bildirim Takibi', 'Arşiv Yönetimi', 'Hızlı Arama']
    },
    {
        'id': 'hacim',
        'name': 'Hacim Analizi',
        'description': 'Hisse senedi hacim analizi ve anomali tespiti',
        'icon': 'fa-chart-bar',
        'color': 'purple',
        'port': 5003,
        'url': 'http://localhost:5003',
        'features': ['Hacim Takibi', 'Anomali Tespiti', 'Görsel Grafikler']
    },
    {
        'id': 'fk',
        'name': 'F/K Analizi',
        'description': 'Hisse değerleme ve F/K oranı analizi',
        'icon': 'fa-calculator',
        'color': 'yellow',
        'port': 5004,
        'url': 'http://localhost:5004',
        'features': ['Değerleme Analizi', 'Karşılaştırma', 'Trend Takibi']
    },
    {
        'id': 'trade',
        'name': 'Trade Asistanı',
        'description': 'Akıllı trading asistanı ve pozisyon yönetimi',
        'icon': 'fa-robot',
        'color': 'red',
        'port': 5005,
        'url': 'http://localhost:5005',
        'features': ['Strateji Kontrolü', 'Pozisyon Takibi', 'Tecrübe Bankası']
    },
    {
        'id': 'bilanco',
        'name': 'Bilanço Analizi',
        'description': 'Bilanço sonrası roket olacak hisseler analizi',
        'icon': 'fa-rocket',
        'color': 'orange',
        'port': 5006,
        'url': 'http://localhost:5006',
        'features': ['Bilanço Tarama', 'Performans Tahmini', 'Otomatik Sıralama']
    }
]


def check_app_status(port):
    """Uygulamanın çalışıp çalışmadığını kontrol et."""
    try:
        response = requests.get(f'http://localhost:{port}', timeout=1)
        return response.status_code == 200
    except:
        return False


@app.route('/')
def index():
    """Ana sayfa - Tüm uygulamaların listesi."""
    # Her uygulamanın durumunu kontrol et
    for app_info in APPLICATIONS:
        app_info['status'] = check_app_status(app_info['port'])

    return render_template('index.html', applications=APPLICATIONS)


@app.route('/app/<app_id>')
def redirect_to_app(app_id):
    """Seçilen uygulamaya yönlendir."""
    app_info = next((app for app in APPLICATIONS if app['id'] == app_id), None)

    if app_info:
        return redirect(app_info['url'])
    else:
        return redirect(url_for('index'))


@app.route('/status')
def status():
    """Tüm uygulamaların durumunu göster (API endpoint)."""
    status_data = []
    for app_info in APPLICATIONS:
        status_data.append({
            'name': app_info['name'],
            'port': app_info['port'],
            'status': 'online' if check_app_status(app_info['port']) else 'offline'
        })

    return {'applications': status_data}


if __name__ == '__main__':
    print("\n" + "="*70)
    print("PARA KOMUTA MERKEZI - ANA WEB SİTESİ")
    print("="*70)
    print("Web Sitesi: http://localhost:8000")
    print("Tüm uygulamaları tek yerden yönetin!")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=8000)
