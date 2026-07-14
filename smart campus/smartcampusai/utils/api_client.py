"""
SmartCampusAI — AI API Client
==============================
Supports Google Gemini, OpenAI, and a built-in demo/simulation mode.
API provider is selected via the AI_PROVIDER environment variable.
"""

import os
import requests
from dotenv import load_dotenv

# Load .env variables at module import
load_dotenv()


def _get_config() -> dict:
    """Returns the active AI configuration from environment variables."""
    return {
        "provider":      os.getenv("AI_PROVIDER", "demo").strip().lower(),
        # Custom API (original project key)
        "custom_key":    (os.getenv("AI_API_KEY") or "").strip(),
        "custom_url":    (os.getenv("AI_API_URL") or "").strip(),
        # Google Gemini
        "gemini_key":    (os.getenv("GEMINI_API_KEY") or "").strip(),
        "gemini_url":    (os.getenv("GEMINI_API_URL") or "").strip(),
        # OpenAI
        "openai_key":    (os.getenv("OPENAI_API_KEY") or "").strip(),
        "openai_url":    (os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")).strip(),
        "openai_model":  os.getenv("OPENAI_MODEL", "gpt-3.5-turbo").strip(),
    }


def ask_ai(prompt: str, system_context: str = "") -> str:
    """
    Sends a prompt to the configured AI provider and returns the response.

    Routing logic:
        - AI_PROVIDER=gemini  → Google Gemini API
        - AI_PROVIDER=openai  → OpenAI Chat Completions API
        - AI_PROVIDER=demo    → Built-in simulation (no API calls)

    Args:
        prompt (str): The user query to send.
        system_context (str): Optional system-level context to prepend.
    Returns:
        str: The assistant's text response.
    Raises:
        RuntimeError: On network failures or unexpected API response formats.
    """
    cfg = _get_config()
    provider = cfg["provider"]

    # ── Demo / Simulation Mode ──────────────────────────────────
    if provider == "demo" or not prompt.strip():
        return _simulate_campus_response(prompt)

    # ── Custom API (AI_API_KEY / AI_API_URL) ─────────────────────
    if provider == "custom":
        return _call_custom(prompt, cfg)

    # ── Google Gemini ───────────────────────────────────────
    if provider == "gemini":
        return _call_gemini(prompt, cfg)

    # ── OpenAI ──────────────────────────────────────────────
    if provider == "openai":
        return _call_openai(prompt, system_context, cfg)

    # ── Unknown / Fallback ────────────────────────────────────
    return _simulate_campus_response(prompt)


def _call_custom(prompt: str, cfg: dict) -> str:
    """
    Calls a custom AI REST API using AI_API_KEY and AI_API_URL.
    Supports Bearer token auth with a standard OpenAI-compatible request body.
    Falls back to demo mode if key is missing or placeholder.
    """
    api_key = cfg["custom_key"]
    api_url = cfg["custom_url"]

    if not api_key or api_key in ("your_api_key_here", ""):
        return _simulate_campus_response(prompt)
    if not api_url:
        return _simulate_campus_response(prompt)

    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are SmartCampusAI, an intelligent academic assistant "
                    "for university students and faculty. Help with schedules, "
                    "attendance, exam tips, campus events, and academic advice."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=25)
        response.raise_for_status()
        data = response.json()

        # Try standard OpenAI response shape first
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        # Fallback response fields
        if "response" in data:
            return data["response"]
        if "text" in data:
            return data["text"]
        if "content" in data:
            return data["content"]

        raise ValueError(f"Unexpected API response format: {list(data.keys())}")

    except requests.exceptions.ConnectionError:
        return (
            "⚠️ **Could not reach the AI server.**\n\n"
            "The custom API endpoint may be unavailable or the URL may be incorrect.\n"
            "Falling back to demo mode responses:\n\n"
            + _simulate_campus_response(prompt)
        )
    except requests.exceptions.HTTPError as e:
        return (
            f"⚠️ **API Error {e.response.status_code}:**\n\n"
            f"Message: {e.response.text[:200]}\n\n"
            "Check that your `AI_API_KEY` is valid and the endpoint is correct."
        )
    except Exception as e:
        raise RuntimeError(f"⚠️ Custom AI API error: {e}")


def _call_gemini(prompt: str, cfg: dict) -> str:
    """Calls Google Gemini API and returns the text response."""
    api_key = cfg["gemini_key"]
    api_url = cfg["gemini_url"]

    if not api_key or api_key == "your_gemini_api_key_here":
        return _simulate_campus_response(prompt)

    # Append API key to URL
    separator = "&" if "?" in api_url else "?"
    url = f"{api_url}{separator}key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [{"text": f"You are SmartCampusAI, an AI assistant for university students and faculty. {prompt}"}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=25,
                                 headers={"Content-Type": "application/json"})
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "No content returned.")

        raise ValueError("Unexpected Gemini API response format.")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"🌐 Network error reaching Gemini API: {e}")
    except Exception as e:
        raise RuntimeError(f"⚠️ Gemini API error: {e}")


def _call_openai(prompt: str, system_context: str, cfg: dict) -> str:
    """Calls OpenAI Chat Completions API and returns the text response."""
    api_key = cfg["openai_key"]
    api_url = cfg["openai_url"]
    model   = cfg["openai_model"]

    if not api_key or api_key == "your_openai_api_key_here":
        return _simulate_campus_response(prompt)

    sys_msg = system_context or (
        "You are SmartCampusAI, an intelligent academic assistant for university students and faculty. "
        "You help with schedules, attendance, exam tips, campus events, and academic advice."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user",   "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(
            api_url,
            json=payload,
            timeout=25,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        response.raise_for_status()
        data = response.json()

        choices = data.get("choices", [])
        if choices:
            return choices[0]["message"]["content"]

        raise ValueError("Unexpected OpenAI API response format.")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"🌐 Network error reaching OpenAI API: {e}")
    except Exception as e:
        raise RuntimeError(f"⚠️ OpenAI API error: {e}")


def _simulate_campus_response(prompt: str) -> str:
    """
    Returns an intelligent simulated campus response for demo/offline mode.
    Covers attendance, schedule, announcements, and general queries.
    """
    q = prompt.lower()

    if any(w in q for w in ["attendance", "absent", "present", "missed"]):
        return (
            "🤖 **SmartCampusAI · Demo Mode**\n\n"
            "Here is your attendance summary:\n\n"
            "| Subject | Attended | Total | Percentage |\n"
            "|---------|----------|-------|------------|\n"
            "| CS101 — Intro to Programming | 38 | 40 | **95%** 🟢 |\n"
            "| MATH202 — Linear Algebra | 32 | 40 | **80%** 🟡 |\n"
            "| ENG105 — Technical Writing | 36 | 40 | **90%** 🟢 |\n"
            "| PHY301 — Engineering Physics | 30 | 40 | **75%** 🔴 |\n\n"
            "⚠️ PHY301 is at the minimum threshold. Attend all remaining classes.\n\n"
            "*Set `AI_PROVIDER=gemini` or `openai` in `.env` to use live AI.*"
        )

    if any(w in q for w in ["schedule", "class", "timetable", "today", "lecture"]):
        return (
            "🤖 **SmartCampusAI · Demo Mode**\n\n"
            "📅 **Your Timetable for Today:**\n\n"
            "| Time | Subject | Venue |\n"
            "|------|---------|-------|\n"
            "| 09:00 – 10:30 AM | CS101: Intro to Programming | Room 402, Eng Block |\n"
            "| 11:00 – 12:30 PM | MATH202: Linear Algebra | Seminar Hall B |\n"
            "| 02:00 – 04:00 PM | CS101: Programming Lab | Lab Building A |\n\n"
            "*Set `AI_PROVIDER=gemini` or `openai` in `.env` to use live AI.*"
        )

    if any(w in q for w in ["notice", "announcement", "event", "news"]):
        return (
            "🤖 **SmartCampusAI · Demo Mode**\n\n"
            "🔔 **Recent Campus Announcements:**\n\n"
            "1. 🔴 **Final Exam Schedule Published** — Exams begin July 22nd. Check student portal.\n"
            "2. 🟡 **Hackathon Registration Closes Tonight** — Prize pool $5,000. Teams of 2–4.\n"
            "3. 🟢 **Digital Library Access** — IEEE Xplore & SpringerLink now free for all students.\n\n"
            "*Set `AI_PROVIDER=gemini` or `openai` in `.env` to use live AI.*"
        )

    if any(w in q for w in ["gpa", "grade", "mark", "score", "cgpa"]):
        return (
            "🤖 **SmartCampusAI · Demo Mode**\n\n"
            "📊 **Academic Performance Summary:**\n\n"
            "| Semester | GPA | Status |\n"
            "|----------|-----|--------|\n"
            "| Sem 1 | 3.6 | ✅ Excellent |\n"
            "| Sem 2 | 3.4 | ✅ Good |\n"
            "| Sem 3 | 3.7 | ✅ Excellent |\n"
            "| Sem 4 (Current) | 3.5 | 📈 On Track |\n\n"
            "**Cumulative GPA: 3.55** — Dean's List candidate!\n\n"
            "*Set `AI_PROVIDER=gemini` or `openai` in `.env` to use live AI.*"
        )

    return (
        f"🤖 **SmartCampusAI · Demo Mode**\n\n"
        f"You asked: *\"{prompt}\"*\n\n"
        "I'm your intelligent campus assistant. I can help you with:\n"
        "- 📅 **Schedules & Timetables**\n"
        "- 📈 **Attendance & GPA tracking**\n"
        "- 🔔 **Campus announcements & events**\n"
        "- 📚 **Study tips and exam preparation**\n\n"
        "💡 *To use a live AI model, update `AI_PROVIDER` in your `.env` file to `gemini` or `openai`.*"
    )
