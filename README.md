<div align="center">
  <h1>🛡️ CyberLearn Pi</h1>
  <p><strong>A lightweight, interactive cybersecurity education platform optimized for Raspberry Pi and low-resource hardware.</strong></p>
  
  [![Python version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![Flask](https://img.shields.io/badge/Flask-3.0.3-black)](https://flask.palletsprojects.com/)
  [![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI%20Tutor-blueviolet)](https://ai.google.dev/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
</div>

<br />

## 📖 About The Project

**CyberLearn Pi** is a project built using the most fundamental and fast technologies to ensure smooth and fluid operation even on low-end, ARM-based systems (e.g., *Raspberry Pi 1 Type B - 512 MB RAM*). It safely teaches students network security, encryption, and command-line basics in a sandboxed environment. Built with Vanilla JS, compiled TailwindCSS, and a lightweight SQLite-Flask architecture, it runs without the bloat of modern SPA frameworks.

## ✨ Key Features

- 📚 **Modular Lesson Content:** Offline-capable Markdown-based educational documents.
- 💻 **Integrated Terminal Simulator:** A client-side JavaScript simulator where students can safely practice Linux commands without the risk of damaging a real server.
- 🤔 **Interactive Quiz Engine:** An AJAX-powered question bank that provides instant feedback at the end of modules without reloading the page.
- 🤖 **Cyber-Tutor (AI Assistant):** An educational assistant powered by Google Gemini 1.5 Pro AI (Optimized for tokens to keep hardware API costs low).
- ⚡ **High Performance:** Optimized with Vanilla JS, SQLite, and Flask-Gunicorn (max 2 async workers), eliminating the need for Node.js or massive databases.
- 🔒 **Secure Access:** A user authentication panel controlled by Flask-Login.

---

## 🚀 Quick Start & Installation

You can use the automated setup script to quickly install it on Linux or macOS distributions:

```bash
# Clone the repository to your computer/server
git clone [GITHUB-REPO-LINK]
cd cyberlearn-pi

# Grant permissions and run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 🛠️ Manual Developer Setup

If you prefer not to use the automated script, follow these standard steps:

**1. Prepare the virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Initialize the database and seed initial data:**
```bash
python3 scripts/seed_db.py
```

**3. Set API Keys:**
- Rename the `.env.example` file in the directory to `.env` and fill in the appropriate fields (Gemini API Secret, etc.).

**4. Start the live development server:**
```bash
bash scripts/dev_server.sh
```
The application will be accessible at `http://localhost:5000`.

---

## 🏗️ Project Architecture & Directory Structure

- `app.py`: The main Flask application entry point.
- `blueprints/`: Controller structures divided by application domains (Auth, Quiz, Lesson, etc.).
- `models/`: Lightweight SQLite3 database tables holding user data (without SQLAlchemy overhead).
- `content/lessons/`: A repository of Markdown (.md) files where lesson content is stored.
- `static/js/`: Vanilla Javascript files responsible for the education panel, terminal simulator, and quiz interactions.

## 🤝 Contributing

Pull requests are always welcome for anyone wishing to contribute to the development. However, since we account for hardware RAM limits (max 512 MB) when adding libraries to the project, please avoid including unnecessary npm / pip packages.

## 📄 License

This project is distributed under the **MIT** license. See the `LICENSE` file for more information.
