import os
import csv
import json
import random
import spacy
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
from spacy.cli import download
from rapidfuzz import fuzz, process
from flask import Flask, request, jsonify

# Inisialisasi Flask app
app = Flask(__name__)

# Load .env dan API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("❌ API key tidak ditemukan! Pastikan sudah diset di Hugging Face 'Repository secrets' dengan nama 'GEMINI_API_KEY'.")

# Konfigurasi Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Load NLP spaCy model
try:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
except (OSError, IOError):
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Load intents
with open("data/intents.json", "r", encoding="utf-8") as f:
    default_intents = json.load(f)["intents"]

# Load materi belajar
with open("data/materi_ai.json", "r", encoding="utf-8") as f:
    materi_data = json.load(f)["materi"]

def prediksi_intent(pesan, intents_data):
    pesan = pesan.lower()
    best_score = 0
    best_intent = None
    for intent in intents_data:
        for pattern in intent["patterns"]:
            score = fuzz.token_sort_ratio(pesan, pattern.lower())
            if score > best_score:
                best_score = score
                best_intent = intent
    return best_intent if best_score >= 60 else None

def deteksi_entitas(pesan):
    doc = nlp(pesan)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Load materi AI dari file JSON
def load_materi_ai():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "materi_ai.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["materi"]
    except Exception as e:
        print(f"❌ Gagal memuat materi_ai.json: {e}")
        return []

def respond(message, history, system_message, max_tokens, temperature, top_p, nama, email, toko):
    # 1. Cek materi(pertanyaan materi)
    materi_data = load_materi_ai()
    materi_dict = {str(item["id"]): item for item in materi_data}

    # 2. Cek intent (pertanyaan bebas)
    intent = prediksi_intent(message, default_intents)
    if intent:
        yield random.choice(intent["responses"])
        return

    # 3. Cek apakah pesan adalah permintaan menu
    message = message.strip()
    if message.lower() in ["halo", "hi", "mulai", "start", "saya mau belajar", "belajar ai", "menu", "pilihan belajar"]:
        menu_msg = "👋 Hai! Mau belajar apa?\n"
        for item in materi_data:
            nomor = item["id"]
            menu_msg += f"{nomor}. {item['judul']}\n"
        menu_msg += "\nKetik nomor pilihan kamu (misalnya: 1)"
        yield menu_msg
        return
    elif message in materi_dict:
        materi = materi_dict[message]
        yield f"📘 *{materi['judul']}*\n\n{materi['isi']}"
        return


    # 4. Fallback
    yield "Maaf, saya belum paham maksud Anda. Bisa ulangi dengan kata yang lebih jelas?"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        pesan = data.get("message", "")
        pengirim = data.get("from", "anon")
        print(f"📩 Pesan dari {pengirim}: {pesan}")

        response_gen = respond(
            message=pesan,
            history=[],
            system_message="Kamu adalah asisten edukasi AI",
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
            nama=pengirim,
            email="anon@example.com",
            toko="reynald_fashion"
        )

        jawaban = next(response_gen)
        return jsonify({"reply": jawaban})

    except Exception as e:
        print("❌ ERROR di webhook:", e)
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))  # Railway bakal ngisi PORT
    app.run(host='0.0.0.0', port=port)
