# 🚀 parakomutamerkezi.com YAYINLAMA REHBERİ

## ⏱️ Toplam Süre: 30-45 dakika
## 💰 Maliyet: İLK 3 AY ÜCRETSİZ

---

## 📋 ADIM 1: GİTHUB HESABI AÇ (5 dakika)

### Ne Yapacaksın:
1. https://github.com adresine git
2. Sağ üstteki **"Sign Up"** butonuna tıkla
3. Bilgileri doldur:
   - Email adresin
   - Kullanıcı adı seç (örn: mustafayilmaz)
   - Güçlü bir şifre belirle
4. Email'ine gelecek doğrulama linkine tıkla
5. ✅ GitHub hesabın hazır!

---

## 📋 ADIM 2: GITHUB DESKTOP İNDİR (5 dakika)

### Ne Yapacaksın:
1. https://desktop.github.com adresine git
2. **"Download for Windows"** butonuna tıkla
3. İndirilen dosyayı çalıştır
4. Yükle (Next, Next, Finish)
5. Açıldığında **"Sign in to GitHub.com"** butonuna tıkla
6. Tarayıcıda GitHub'a giriş yap
7. ✅ GitHub Desktop hazır!

---

## 📋 ADIM 3: PROJEYİ GITHUB'A YÜKLE (10 dakika)

### Ne Yapacaksın:
1. **GitHub Desktop**'ı aç
2. Sol üstteki **"File"** → **"Add Local Repository"** tıkla
3. **"Choose"** butonuna tıkla
4. Şu klasörü seç:
   ```
   C:\Users\LENOVO\Desktop\PARA KOMUTA MERKEZİ WEB SİTESİ
   ```
5. **"Add Repository"** tıkla
6. Eğer hata verirse **"create a repository"** linkine tıkla
7. Sol altta şunu yaz:
   ```
   İlk yükleme - Para Komuta Merkezi
   ```
8. **"Commit to main"** butonuna tıkla
9. Üstte **"Publish repository"** butonuna tıkla
10. Açılan pencerede:
    - Name: `para-komuta-merkezi`
    - **"Keep this code private"** TIKINI KALDIR (public olsun)
    - **"Publish Repository"** tıkla
11. ✅ Kodlar GitHub'da!

---

## 📋 ADIM 4: RENDER.COM HESABI AÇ (5 dakika)

### Ne Yapacaksın:
1. https://render.com adresine git
2. Sağ üstteki **"Get Started"** butonuna tıkla
3. **"GitHub"** ile giriş yap seçeneğini seç
4. GitHub hesabınla giriş yap
5. Render'ın GitHub'a erişim istemesini **"Authorize"** ile onayla
6. ✅ Render hesabın hazır!

---

## 📋 ADIM 5: WEB SERVİSİ OLUŞTUR (10 dakika)

### Ne Yapacaksın:
1. Render Dashboard'da sağ üstte **"New +"** butonuna tıkla
2. **"Web Service"** seç
3. GitHub repo listesinde **"para-komuta-merkezi"** reposunu bul
4. Yanındaki **"Connect"** butonuna tıkla
5. Ayarları şöyle yap:

   ```
   Name: para-komuta-merkezi
   Region: Frankfurt (EU Central)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   Instance Type: Free
   ```

6. **En alttaki "Advanced"** butonuna tıkla
7. **"Add Environment Variable"** tıkla:
   ```
   Key: PYTHON_VERSION
   Value: 3.11.0
   ```
8. **"Create Web Service"** butonuna tıkla
9. ⏳ Render şimdi siteyi kuruyor... 5-10 dakika bekle
10. ✅ Yeşil "Live" yazısını gördüğünde hazır!

---

## 📋 ADIM 6: DOMAİN BAĞLAMA (5 dakika)

### Ne Yapacaksın:
1. Render'da oluşturduğun service'e tıkla
2. Üstteki **"Settings"** sekmesine git
3. Aşağı kaydır, **"Custom Domains"** bölümünü bul
4. **"Add Custom Domain"** butonuna tıkla
5. Şunu yaz: `parakomutamerkezi.com`
6. **"Save"** tıkla
7. Ekranda çıkan bilgileri not al:
   ```
   Type: A Record
   Name: @
   Value: [bir IP adresi gösterecek, örn: 123.45.67.89]
   ```

### Domain ayarlarını yap:
1. Domain aldığın yere git (GoDaddy, Natro, vb.)
2. **"DNS Ayarları"** veya **"DNS Management"** bölümüne git
3. Yeni bir **A Record** ekle:
   - Type: `A`
   - Name: `@`
   - Value: Render'dan aldığın IP
   - TTL: `600` veya `Auto`
4. Kaydet
5. ⏳ 10-30 dakika bekle (DNS yayılması)
6. ✅ parakomutamerkezi.com sitene erişebilir!

---

## 📋 ADIM 7: HTTPS (SSL) AKTIF ET (Otomatik)

### Ne Yapacaksın:
- Hiçbir şey! 🎉
- Render otomatik olarak SSL sertifikası ekleyecek
- 1-2 saat içinde `https://parakomutamerkezi.com` çalışacak

---

## ⚠️ ÖNEMLİ NOTLAR

### Ücretsiz Plan Limitleri:
- ✅ 750 saat/ay ücretsiz (bir ay 24/7 çalışır)
- ✅ 100 GB bandwidth
- ✅ Otomatik uyku modu (15 dk hareketsizlikten sonra)
- ⚠️ İlk ziyarette 10-20 saniye yavaş açılır (uykudan uyandırma)

### Ücretli Plana Ne Zaman Geçmeli:
- Siteniz çok kullanılıyorsa (günde 100+ ziyaretçi)
- Uyku modunu istemiyorsanız
- **Ücret**: $7/ay (~220 TL/ay) - bütçen dahilinde!

---

## 🎯 SONUÇ

✅ Domain: parakomutamerkezi.com
✅ Hosting: Render.com (ücretsiz)
✅ SSL: Otomatik (ücretsiz)
✅ Toplam Maliyet: 0 TL/ay (ilk 3 ay)

---

## ❓ SORUN ÇÖZME

### Site açılmıyor?
1. Render'da "Live" yazıyor mu kontrol et
2. DNS ayarlarını doğru yaptın mı kontrol et
3. 30 dakika daha bekle (DNS yayılması)

### GitHub'a yükleyemedim?
1. GitHub Desktop'ta "Sign in" yaptın mı?
2. Klasör yolunu doğru seçtin mi?
3. Ekran görüntüsü at, yardım edeyim

### Render'da hata aldım?
1. Build logs'a bak (sol menüde "Logs")
2. Hatayı kopyala, bana gönder
3. Birlikte çözeriz!

---

## 📞 YARDIM

Herhangi bir adımda takıldın mı?
Ekran görüntüsü at, adım adım yardımcı olayım! 💪

---

© 2025 Para Komuta Merkezi
