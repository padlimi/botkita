# 🤖 KlikIndomaret Telegram Bot

Bot Telegram canggih untuk KlikIndomaret dengan fitur login, pencarian produk, keranjang belanja, checkout, dan tracking pesanan.

## ✨ Fitur Utama

- 🔐 **Login Akun** - Support email/phone + OTP
- 🔍 **Search Produk** - Cari produk dengan filter
- 🛒 **Keranjang Belanja** - Manage cart dengan mudah
- 💳 **Checkout** - Multiple payment methods
- 📦 **Tracking Pesanan** - Real-time order tracking
- ❤️ **Wishlist** - Simpan produk favorit
- 👤 **Profile** - Manage akun

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Telegram Bot Token (dari @BotFather)

### Installation

1. **Clone repository:**
```bash
git clone https://github.com/padlimiGunakan/botkita.git
cd botkita
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env dengan kredensial Anda
```

5. **Run locally:**
```bash
python main.py
```

## 📊 Database Setup

```bash
# Create database
createdb botkita_db

# Update DATABASE_URL di .env
DATABASE_URL=postgresql://username:password@localhost:5432/botkita_db
```

## 🚂 Deploy ke Railway

1. **Push ke GitHub:**
```bash
git add .
git commit -m "Initial commit"
git push
```

2. **Deploy di Railway:**
   - Buka https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Pilih repository `botkita`
   - Add PostgreSQL database
   - Set environment variables di Railway dashboard
   - Deploy!

## 📝 Perintah Bot

```
/start - Mulai bot
/help - Bantuan
/login - Login akun
/search <keyword> - Cari produk
/cart - Lihat keranjang
/orders - Riwayat pesanan
/wishlist - Daftar favorit
/profile - Info profil
/logout - Keluar akun
```

## 🔧 Troubleshooting

### Bot tidak respond
- Pastikan TELEGRAM_BOT_TOKEN benar
- Check logs: `python main.py` (development mode)

### Database connection error
- Verify DATABASE_URL di .env
- Pastikan PostgreSQL running
- Check username/password

### Railway deployment failed
- Check Railway logs
- Verify environment variables
- Pastikan Procfile atau CMD di Dockerfile benar

## 📚 Tech Stack

- **Bot Framework**: python-telegram-bot
- **Database**: PostgreSQL + SQLAlchemy
- **Hosting**: Railway
- **Language**: Python 3.11

## 📄 License

MIT License - See LICENSE file

## 🤝 Support

- Email: support@botkita.dev
- Telegram: @support_botkita

---

Made with ❤️ by padlimiGunakan