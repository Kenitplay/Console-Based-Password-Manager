# 🔐 Console-Based Password Manager (Flask + SQLite + hashlib)

A lightweight, self-hosted password manager designed to run on an old Android phone using **Pydroid3**. It works over local Wi-Fi, requires no internet, and includes a simple client-server setup built with **Flask**, **SQLAlchemy**, and **hashlib**.

---

## 📦 Features

- 🧠 Stores plaintext + hashed passwords (for integrity)
- 🧮 Uses `hashlib.sha256()` (no external crypto libs)
- 🖥 Console-based UI for client devices
- ⚙️ Full CRUD (Create, Read, Update, Delete)
- 🔁 Automatically reorders IDs after deletion
- 📴 Offline-only – no internet required
- 📱 Hostable on any old phone with Pydroid3

---

## 🛠 Setup

### 1. 📱 Server (On Old Phone or PC)

Install dependencies:

```bash
pip install flask flask_sqlalchemy
python server.py
```

### 2. 💻 Client (Any Device)

Install dependencies:

```bash
pip install requests
```
## Run The Client:

```bash
python client.py
```

It will ask you for the server’s IP (e.g., 192.168.1.11), then present an interactive menu to:
- View saved credentials
- Add new ones
- Edit or delete existing entries


## 📂 File Structure
```bash
password-manager/
├── server.py       # Flask API server (runs on host device)
├── client.py       # Console-based client app
├── passwords.db    # SQLite database (auto-generated)
└── README.md       # This file
```

## 🔐 Security Notes
- Local network use only
- Do not expose this app to the internet
- Passwords are stored in plaintext for usability
- Meant for personal offline use, not enterprise-grade security


## 📱 Pydroid3 Note
If you're using Pydroid3 on Android:
- The database (passwords.db) is typically located at:
```bash
/data/data/ru.iiec.pydroid3/files
```
- Use Pydroid's built-in file browser or os.getcwd() in Python to confirm.

## 👤 Author
- Built with care by Kenitplay.



