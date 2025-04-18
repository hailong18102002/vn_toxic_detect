from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# App setup
app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URL_CONNECT")

# Load model
tokenizer = AutoTokenizer.from_pretrained("tarudesu/ViHateT5-base-HSD")
model = AutoModelForSeq2SeqLM.from_pretrained("tarudesu/ViHateT5-base-HSD")
PREFIX = "toxic-speech-detection"

# MongoDB setup
client = MongoClient(mongo_uri)
db = client["vn_toxic"]
users_collection = db["users"]
history_collection = db["toxic_detection"]

# Utility: Generate model output
def generate_output(input_text, prefix):
    prefixed_input = prefix + ': ' + input_text
    input_ids = tokenizer.encode(prefixed_input, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=256)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# ===== Routes =====
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/sign', endpoint='signin')
def sign():
    return render_template('signin.html')

@app.route('/detect', endpoint='detect')
def detect():
    return render_template('detect.html')

@app.route('/history', endpoint='history')
def history():
    histories = list(history_collection.find())
    for h in histories:
        h["status_color"] = 'red' if h['status'] == 'toxic' else 'green'
        h["short_content"] = (h["content"][:50] + "...") if len(h["content"]) > 50 else h["content"]
        h["show_more"] = len(h["content"]) > 50
    return render_template('history.html', histories=histories)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Thiếu tên đăng nhập hoặc mật khẩu"}), 400

        if users_collection.find_one({"user": username}):
            return jsonify({"error": "Người dùng đã tồn tại"}), 409

        users_collection.insert_one({"user": username, "password": password})
        return jsonify({"success": "Đăng ký thành công"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Đã xảy ra lỗi trong quá trình đăng ký"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({"user": username})
    if user and user.get("password") == password:
        return jsonify({"success": "Đăng nhập thành công"}), 201
    else:
        return jsonify({"error": "Không có người dùng hoặc tài khoản hoặc mật khẩu"}), 409

@app.route('/api/check', methods=['POST'])
def check_content():
    data = request.json
    input_type = data.get('type')
    content = data.get('content')
    url = data.get("url", "")
    text_to_check = content

    # If URL provided, scrape content
    if url:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'li', 'span'])
                text_to_check = '\n'.join(tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True))
            else:
                return jsonify({"error": f"Không thể lấy nội dung từ URL (status code {response.status_code})"}), 400
        except Exception as e:
            return jsonify({"error": f"Lỗi khi lấy nội dung từ URL: {str(e)}"}), 500

    # Use model for detection
    result = generate_output(text_to_check, PREFIX)
    is_toxic = result.lower() == "toxic"

    # Prepare history
    history_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": content,
        "type": input_type,
        "status": result,
        "score": 85 if is_toxic else 5,
        "url": url
    }
    history_collection.insert_one(history_data)

    return jsonify({
        'status': 'toxic' if is_toxic else 'non-toxic',
        'score': history_data['score'],
        'message': content
    })

# Run app
if __name__ == '__main__':
    app.run(debug=True)
