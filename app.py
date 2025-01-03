from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
import signal

from chat import get_response

app = Flask(__name__)
CORS(app)

# Store the process ID in a file for reboot.py to use
with open('app.pid', 'w') as f:
    f.write(str(os.getpid()))

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Content-Security-Policy'] = "frame-ancestors *"
    return response

def run_update_model():
    try:
        subprocess.run([sys.executable, 'update_model.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menjalankan update_model.py: {e}")
        return False

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

@app.get("/update_model")
def update_model():
    if run_update_model():
        # Run reboot.py in a separate process
        subprocess.Popen([sys.executable, 'reboot.py'])
        return jsonify({"status": "success", "message": "Model berhasil diperbarui dan aplikasi akan di-restart"})
    else:
        return jsonify({"status": "error", "message": "Terjadi kesalahan saat memperbarui model"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)