"""
Para Komuta Merkezi - Ana Web Sitesi
Tüm uygulamaları tek çatı altında toplayan merkezi portal
"""

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Permission
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'para-komuta-merkezi-2025-super-secret-key')

# Production'da PostgreSQL, development'ta SQLite
if os.environ.get('DATABASE_URL'):
    # Render PostgreSQL URL fix (postgresql:// -> postgresql+psycopg2://)
    db_url = os.environ.get('DATABASE_URL')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pkm_users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı başlat
db.init_app(app)

# Login manager başlat
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
@login_required
def index():
    """Ana sayfa - Tüm uygulamaların listesi (sadece giriş yapmış kullanıcılar)."""
    # Kullanıcının erişebildiği uygulamaları filtrele
    user_applications = []
    for app_info in APPLICATIONS.copy():
        app_copy = app_info.copy()
        app_copy['status'] = check_app_status(app_info['port'])
        app_copy['has_permission'] = current_user.has_permission(app_info['id']) or current_user.is_admin
        user_applications.append(app_copy)

    return render_template('index.html', applications=user_applications)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_approved():
                login_user(user, remember=True)
                flash('Başarıyla giriş yaptınız!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Hesabınız henüz onaylanmamış. Lütfen yönetici onayını bekleyin.', 'error')
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Kayıt sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Validasyon
        if not username or not email or not password:
            flash('Tüm alanları doldurun!', 'error')
            return render_template('register.html')

        if password != password_confirm:
            flash('Şifreler eşleşmiyor!', 'error')
            return render_template('register.html')

        # Kullanıcı zaten var mı?
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanılıyor!', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Bu email zaten kullanılıyor!', 'error')
            return render_template('register.html')

        # Yeni kullanıcı oluştur (otomatik beklemede durumunda)
        new_user = User(username=username, email=email, status='beklemede')
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarılı! Hesabınız yönetici tarafından onaylandıktan sonra giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Çıkış"""
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin():
    """Admin paneli - Sadece admin kullanıcılar erişebilir"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('index'))

    # Tüm kullanıcıları getir
    all_users = User.query.all()
    pending_users = User.query.filter_by(status='beklemede').all()
    approved_users = User.query.filter_by(status='onaylı').all()

    return render_template('admin.html',
                         all_users=all_users,
                         pending_users=pending_users,
                         approved_users=approved_users,
                         applications=APPLICATIONS)


@app.route('/admin/approve_user/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    """Kullanıcıyı onayla"""
    if not current_user.is_admin:
        flash('Yetkiniz yok!', 'error')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if user:
        user.status = 'onaylı'
        db.session.commit()
        flash(f'{user.username} kullanıcısı onaylandı!', 'success')
    else:
        flash('Kullanıcı bulunamadı!', 'error')

    return redirect(url_for('admin'))


@app.route('/admin/reject_user/<int:user_id>', methods=['POST'])
@login_required
def reject_user(user_id):
    """Kullanıcıyı reddet"""
    if not current_user.is_admin:
        flash('Yetkiniz yok!', 'error')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if user:
        user.status = 'reddedildi'
        db.session.commit()
        flash(f'{user.username} kullanıcısı reddedildi!', 'success')
    else:
        flash('Kullanıcı bulunamadı!', 'error')

    return redirect(url_for('admin'))


@app.route('/admin/update_permissions/<int:user_id>', methods=['POST'])
@login_required
def update_permissions(user_id):
    """Kullanıcının uygulama izinlerini güncelle"""
    if not current_user.is_admin:
        flash('Yetkiniz yok!', 'error')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if not user:
        flash('Kullanıcı bulunamadı!', 'error')
        return redirect(url_for('admin'))

    # Tüm uygulamalar için izinleri kontrol et
    for app in APPLICATIONS:
        app_id = app['id']
        has_permission = request.form.get(f'app_{app_id}') == 'on'

        # Mevcut izni bul veya oluştur
        permission = Permission.query.filter_by(user_id=user_id, app_id=app_id).first()

        if permission:
            permission.granted = has_permission
        else:
            permission = Permission(user_id=user_id, app_id=app_id, granted=has_permission)
            db.session.add(permission)

    db.session.commit()
    flash(f'{user.username} için izinler güncellendi!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Kullanıcıyı sil"""
    if not current_user.is_admin:
        flash('Yetkiniz yok!', 'error')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if user:
        if user.is_admin:
            flash('Admin kullanıcı silinemez!', 'error')
        else:
            username = user.username
            db.session.delete(user)
            db.session.commit()
            flash(f'{username} kullanıcısı silindi!', 'success')
    else:
        flash('Kullanıcı bulunamadı!', 'error')

    return redirect(url_for('admin'))


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


def init_database():
    """Veritabanını başlat ve admin kullanıcı oluştur"""
    with app.app_context():
        db.create_all()

        # Admin kullanıcı yoksa oluştur
        admin = User.query.filter_by(username='adminömer').first()
        if not admin:
            admin = User(
                username='adminömer',
                email='admin@parakomutamerkezi.com',
                status='onaylı',
                is_admin=True
            )
            admin.set_password('adminömer.pkm.2025')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Admin kullanici olusturuldu!")
            print("   Kullanici adi: adminömer")
            print("   Sifre: adminömer.pkm.2025")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("PARA KOMUTA MERKEZI - ANA WEB SİTESİ")
    print("="*70)

    # Veritabanını başlat
    init_database()

    print("Web Sitesi: http://localhost:8000")
    print("Tüm uygulamaları tek yerden yönetin!")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=8000)
