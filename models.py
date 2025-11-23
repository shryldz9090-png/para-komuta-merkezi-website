"""
Veritabanı Modelleri
Kullanıcı yönetimi ve uygulama izinleri için SQLAlchemy modelleri
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Kullanıcı modeli"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='beklemede')  # beklemede, onaylı, reddedildi
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkiler
    permissions = db.relationship('Permission', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Şifreyi hash'leyerek kaydet"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Şifreyi kontrol et"""
        return check_password_hash(self.password_hash, password)

    def is_approved(self):
        """Kullanıcı onaylı mı?"""
        return self.status == 'onaylı'

    def has_permission(self, app_id):
        """Kullanıcının belirli bir uygulamaya erişim izni var mı?"""
        permission = Permission.query.filter_by(user_id=self.id, app_id=app_id).first()
        return permission and permission.granted

    def __repr__(self):
        return f'<User {self.username}>'


class Permission(db.Model):
    """Uygulama izinleri modeli"""
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    app_id = db.Column(db.String(50), nullable=False)  # portfoy, kap, hacim, fk, trade, bilanco
    granted = db.Column(db.Boolean, default=False)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Permission user={self.user_id} app={self.app_id} granted={self.granted}>'
