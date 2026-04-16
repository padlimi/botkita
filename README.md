# 🤖 Telegram Bot + Gemini AI

Bot Telegram yang terintegrasi dengan Google Gemini AI, siap deploy ke Railway.

## ✨ Fitur

- Chat AI dengan Google Gemini (memori percakapan per user)
- Perintah: `/start`, `/new`, `/help`, `/about`
- Otomatis reset sesi dengan `/new`
- Mendukung pesan panjang (auto-split 4096 karakter)
- Deploy mudah ke Railway

---

## 🚀 Deploy ke Railway (Step by Step)

### 1. Siapkan Token & API Key

**Telegram Bot Token:**
1. Buka Telegram → cari `@BotFather`
2. Kirim `/newbot` → ikuti instruksi
3. Salin token yang diberikan

**Gemini API Key:**
1. Buka [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Klik **"Create API Key"**
3. Salin API key

---

### 2. Upload ke GitHub

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

---

### 3. Deploy ke Railway

1. Buka [https://railway.app](https://railway.app) → Login dengan GitHub
2. Klik **"New Project"** → **"Deploy from GitHub repo"**
3. Pilih repository kamu
4. Railway akan otomatis mendeteksi konfigurasi

---

### 4. Set Environment Variables di Railway

Di dashboard Railway → tab **"Variables"** → tambahkan:

| Variable | Value |
|---|---|
| `TELEGRAM_TOKEN` | Token dari BotFather |
| `GEMINI_API_KEY` | API Key dari AI Studio |
| `GEMINI_MODEL` | `gemini-1.5-flash` *(opsional)* |

---

### 5. Deploy!

Setelah variabel diset, Railway akan otomatis redeploy.
Cek log di tab **"Deployments"** → lihat:
```
Bot started with model: gemini-1.5-flash
```
Bot siap digunakan! 🎉

---

## 🛠️ Jalankan Lokal (Opsional)

```bash
# Install dependencies
pip install -r requirements.txt

# Buat file .env dari contoh
cp .env.example .env
# Edit .env → isi TELEGRAM_TOKEN dan GEMINI_API_KEY

# Jalankan
python bot.py
```

---

## 📁 Struktur File

```
telegram-gemini-bot/
├── bot.py              # Kode utama bot
├── requirements.txt    # Dependencies Python
├── Procfile            # Untuk Railway/Heroku
├── railway.toml        # Konfigurasi Railway
├── .env.example        # Contoh environment variables
├── .gitignore
└── README.md
```

---

## 🔧 Ganti Model Gemini

Set environment variable `GEMINI_MODEL` dengan salah satu:
- `gemini-1.5-flash` – Cepat & gratis (default)
- `gemini-1.5-pro` – Lebih pintar, lebih lambat
- `gemini-2.0-flash` – Terbaru & cepat
