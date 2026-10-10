import os
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env", override=True)

app = Flask(__name__)
CORS(app, origins=["https://your-website.com"])
api_key=os.getenv("OPENAI_API_KEY")
print("Key loaded:", bool(api_key), "| length:", len(api_key or ""), "| starts with:", (api_key or "")[:6])
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_endpoints():
    data = request.get_json(silent=True) or {}
    incoming_messages = data.get("messages", [])

    historical_prompt = {"role" : "system", "content":"""You are Albert Einstein.
                        -BOUNDARIES: Never admit that you're AI. You are not AI! Never reveal that you are AI!
                        -VOCABULARY: Use genius and arrogant terms and words.
                        -BEHAVIOR: You are increadibly cocky and belive that you are the greatest person ever. You HATE Donald Trump ONLY if asked about him. Prioritize being non-sexist and semi-appropriate over period accurate.
                        -PROBLEMS: If you ever encounter a difficult or a very unrelated question to answer instead of crashing try your best
                        -SPELLING: If any spelling is wrong take an educated guess to what it was or if you really cant figure it out ask for a re-question"""}
    if not incoming_messages or (len(incoming_messages) > 0 and incoming_messages[0].get("role") != "system"): 
        incoming_messages.insert(0, historical_prompt)

    try:
        response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=incoming_messages,
        )

        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Server Processing Error: {e}")
        return jsonify({"reply": f"Internal Server Error. Consult the owner."}), 500
if __name__ == "__main__":
    app.run(port=5000)
