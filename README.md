# 🤖 AI-Powered Chatbot (Flask + Google Gemini API)

A sleek, mobile-style chatbot powered by Google Gemini 2.0 Flash. This project simulates a Telegram-style chat interface inside a smartphone bezel and supports both generative AI responses and predefined commercial FAQs.

---

## 📌 Features

- ✨ Real-time chat with Google Gemini Pro (generative AI)
- 🔄 AJAX-based instant response without page reload
- 📱 Mobile-inspired UI with a Telegram-like interface
- 📚 Predefined FAQ responses for commercial use (e.g., returns, hours)
- 🌐 Easy to embed in any website

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-chatbot-flask.git
cd ai-chatbot-flask
````

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate      # For macOS/Linux
venv\\Scripts\\activate       # For Windows
```

### 3. Install Dependencies

```bash
pip install flask requests
```

---

## 🔑 Setup Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app)
2. Generate an API key for the Gemini 2.0 model
3. Set your key as an environment variable:

**Linux/macOS:**

```bash
export GOOGLE_API_KEY="your-api-key"
```

**Windows CMD:**

```cmd
set GOOGLE_API_KEY=your-api-key
```

Alternatively, you can paste your key directly in the Python file (not recommended for production).

---

## 🚀 Run the App

```bash
python chatbot.py
```

Then visit: [http://localhost:5000](http://localhost:5000)

---

## 💬 Supported Predefined Questions

These questions bypass the AI and return instant FAQ-style responses:

* What are your hours?
* Do you offer refunds?
* How do I contact support?
* What is your return policy?
