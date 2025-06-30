import os
from flask import Flask, request, jsonify, render_template_string
import requests

API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyAjJEXNZUWG7EqpIdS2hBpbjqsrsiUWXZU")
MODEL_NAME = "gemini-2.0-flash"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

app = Flask(__name__)

# Define fallback intents
faq_responses = {
    "what are your hours": "We are open from 9 AM to 6 PM, Monday to Saturday.",
    "how do i contact support": "You can contact our support team at support@example.com or call 123-456-7890.",
    "do you offer refunds": "Yes, we offer refunds within 30 days of purchase with a valid receipt.",
    "what is your return policy": "Our return policy allows returns within 30 days in original packaging."
}

def match_intent(message):
    msg = message.lower()
    for pattern, reply in faq_responses.items():
        if pattern in msg:
            return reply
    return None

def get_html():
    return """
    <!doctype html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>Chatbot</title>
        <style>
          body {
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #d0e4fe;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          }
          .phone {
            width: 360px;
            height: 640px;
            background: #000;
            border-radius: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
          }
          .screen {
            position: absolute;
            top: 20px;
            left: 10px;
            right: 10px;
            bottom: 20px;
            background: #f8f9fa;
            border-radius: 30px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
          }
          .header {
            background: #0088cc;
            color: white;
            padding: 10px;
            font-weight: bold;
            text-align: center;
            font-size: 16px;
          }
          #chat-screen {
            flex: 1;
            padding: 10px;
            overflow-y: auto;
            background: #e5e5e5;
            display: flex;
            flex-direction: column;
          }
          .message {
            max-width: 70%;
            margin: 6px 0;
            padding: 8px 12px;
            border-radius: 18px;
            line-height: 1.4;
            word-wrap: break-word;
          }
          .user {
            background: #0088cc;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            border-bottom-left-radius: 18px;
            border-top-left-radius: 18px;
            border-top-right-radius: 18px;
          }
          .bot {
            background: white;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 18px;
            border-top-left-radius: 18px;
            border-top-right-radius: 18px;
          }
          .input-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: white;
            border-top: 1px solid #ccc;
          }
          .input-bar input {
            flex: 1;
            height: 36px;
            padding: 0 12px;
            border: 1px solid #ccc;
            border-radius: 18px;
            font-size: 14px;
            outline: none;
            margin-right: 10px;
          }
          .input-bar button {
            background: #0088cc;
            border: none;
            color: white;
            padding: 0 16px;
            font-size: 14px;
            border-radius: 18px;
            cursor: pointer;
          }
          .input-bar button:active {
            background: #006c9a;
          }
        </style>
      </head>
      <body>
        <div class=\"phone\">
          <div class=\"screen\">
            <div class=\"header\">AI Chat</div>
            <div id=\"chat-screen\"></div>
            <div class=\"input-bar\">
              <input id=\"user-input\" placeholder=\"Message...\" />
              <button id=\"send-btn\">Send</button>
            </div>
          </div>
        </div>
        <script>
          const screen = document.getElementById('chat-screen');
          const input = document.getElementById('user-input');
          const sendBtn = document.getElementById('send-btn');

          function addMessage(who, text) {
            const msg = document.createElement('div');
            msg.className = 'message ' + who;
            msg.textContent = text;
            screen.appendChild(msg);
            screen.scrollTop = screen.scrollHeight;
          }

          async function sendMessage() {
            const text = input.value.trim();
            if (!text) return;
            addMessage('user', text);
            input.value = '';
            try {
              const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: text })
              });
              const data = await res.json();
              addMessage('bot', data.reply);
            } catch (e) {
              addMessage('bot', '[Error] ' + e.message);
            }
          }

          sendBtn.addEventListener('click', sendMessage);
          input.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
        </script>
      </body>
    </html>
    """

@app.route('/')
def home():
    return render_template_string(get_html())

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')

    # Check for predefined responses first
    fallback = match_intent(user_msg)
    if fallback:
        return jsonify({"reply": fallback})

    payload = {"contents":[{"parts":[{"text":user_msg}]}]}
    params = {"key":API_KEY}

    try:
        resp = requests.post(BASE_URL, params=params, json=payload)
        resp.raise_for_status()
        body = resp.json()
        reply = body.get('candidates',[])[0].get('content',{}).get('parts',[{}])[0].get('text','').strip()
    except Exception as e:
        reply = f"[Error] {str(e)}"
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
