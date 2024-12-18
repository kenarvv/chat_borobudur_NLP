from flask import Flask, render_template, request, jsonify
import subprocess
import sys

from chat import get_response

app = Flask(__name__)

# Fungsi untuk menjalankan update_model.py
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
    # Jalankan update_model.py untuk memperbarui model
    if run_update_model():
        return jsonify({"status": "success", "message": "Model berhasil diperbarui"})
    else:
        return jsonify({"status": "error", "message": "Terjadi kesalahan saat memperbarui model"})

if __name__ == "__main__":
    app.run(debug=True)