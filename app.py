from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
import signal
import re

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

def filter_error_messages(messages):
    """
    Filter and format error messages to only show row-specific errors
    """
    filtered_errors = []
    
    for message in messages:
        # Only process messages that contain "Baris" and "kosong"
        row_match = re.search(r'Baris (\d+) pada Google Sheets:', message)
        if row_match and "kosong" in message:
            filtered_errors.append(message)
        # For messages from gsheet_to_json.py that need formatting
        elif "row" in message.lower():
            row_match = re.search(r'row (\d+)', message)
            if row_match:
                row_num = row_match.group(1)
                if "tag" in message.lower():
                    filtered_errors.append(f"Baris {row_num} pada Google Sheets: Tag kosong")
                elif "patterns" in message.lower():
                    filtered_errors.append(f"Baris {row_num} pada Google Sheets: Patterns kosong")
                elif "responses" in message.lower():
                    filtered_errors.append(f"Baris {row_num} pada Google Sheets: Responses kosong")
    
    return filtered_errors

def run_update_model():
    try:
        result = subprocess.run(
            [sys.executable, 'update_model.py'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            error_messages = result.stdout.strip().split('\n') or result.stderr.strip().split('\n')
            return False, error_messages
            
        return True, []
    except Exception as e:
        return False, [f"Terjadi kesalahan: {str(e)}"]

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
    success, messages = run_update_model()
    
    if success:
        # Run reboot.py in a separate process
        subprocess.Popen([sys.executable, 'reboot.py'])
        return jsonify({
            "status": "success",
            "message": "Model berhasil diperbarui dan aplikasi akan di-restart"
        })
    else:
        filtered_errors = filter_error_messages(messages)
        return jsonify({
            # "status": "error",
            # "message": "Terjadi kesalahan saat memperbarui model",
            "details": filtered_errors
            # "suggestion": "Silakan periksa baris yang kosong pada Google Sheets dan pastikan semua kolom (tag, patterns, responses) telah diisi"
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)