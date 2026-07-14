# SmartCampusAI

> **An AI-powered academic portal built with Streamlit, bcrypt authentication, and JSON databases.**

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🔒 **Secure Auth** | Registration & Login with bcrypt password hashing |
| 📊 **Dashboard** | Attendance metrics, timetable, GPA, and live announcements |
| 🤖 **AI Assistant** | Integrated with Google Gemini, OpenAI, or offline demo mode |
| 🗄️ **JSON Database** | File-locked JSON storage for users, events, announcements |
| 🎨 **Premium UI** | Glassmorphism dark theme with gradient text and micro-animations |

---

## 📁 Project Structure

```
smartcampusai/
├── app.py                      # Home/landing page
├── .env                        # API keys & secrets (NOT committed)
├── .env.example                # Template for env vars
├── requirements.txt            # Python dependencies
├── .gitignore
│
├── pages/
│   ├── 1_Login.py              # Login page
│   ├── 2_Register.py           # Registration page
│   └── 3_Dashboard.py          # Main authenticated dashboard
│
├── auth/
│   └── auth_utils.py           # bcrypt auth, registration, session mgmt
│
├── database/
│   ├── db_utils.py             # Thread-safe JSON DB operations
│   ├── users.json              # User accounts (auto-created)
│   ├── events.json             # Campus events data
│   └── announcements.json      # Campus announcements data
│
└── utils/
    ├── api_client.py           # Multi-provider AI client (Gemini/OpenAI/Demo)
    └── styles.py               # Global CSS design system
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd smartcampusai
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 5. Run the application
```bash
streamlit run app.py
```

---

## 🔑 API Key Configuration (`.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `APP_SECRET_KEY` | App-level secret key | ✅ |
| `AI_PROVIDER` | `gemini` / `openai` / `demo` | ✅ |
| `GEMINI_API_KEY` | Google Gemini API key | If using Gemini |
| `GEMINI_API_URL` | Gemini endpoint URL | If using Gemini |
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI |
| `OPENAI_API_URL` | OpenAI endpoint URL | If using OpenAI |
| `OPENAI_MODEL` | Model name (e.g. `gpt-3.5-turbo`) | If using OpenAI |

---

## 🧪 AI Provider Setup

### Option A: Google Gemini (Recommended)
1. Get a free key at [Google AI Studio](https://aistudio.google.com/)
2. Set in `.env`:
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   ```

### Option B: OpenAI
1. Get an API key at [OpenAI](https://platform.openai.com/)
2. Set in `.env`:
   ```
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   ```

### Option C: Demo Mode (No API Key Needed)
```
AI_PROVIDER=demo
```

---

## 📦 Deployment

### Streamlit Cloud
1. Push to GitHub (ensure `.env` is in `.gitignore`)
2. Add secrets in **Streamlit Cloud → App Settings → Secrets** in TOML format:
   ```toml
   AI_PROVIDER = "gemini"
   GEMINI_API_KEY = "your_key_here"
   APP_SECRET_KEY = "your_secret_here"
   ```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## 🛡️ Security Notes

- Passwords are hashed with **bcrypt (12 rounds)** — never stored in plaintext
- `.env` is excluded from version control via `.gitignore`
- JSON database uses **file-level locking** to prevent concurrent write corruption
- Session state is cleared completely on logout

---

## 📄 License

MIT License — SmartCampusAI © 2026
