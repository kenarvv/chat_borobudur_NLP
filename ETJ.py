import pandas as pd
import json
import os
from datetime import datetime

# Fungsi untuk mengelola jumlah file log
def manage_logs(folder, max_logs=10):
    """
    Membatasi jumlah file log dalam folder tertentu.
    Jika melebihi max_logs, file log tertua akan dihapus.
    """
    log_files = [f for f in os.listdir(folder) if f.startswith("intents_") and f.endswith(".json")]
    if len(log_files) > max_logs:
        # Urutkan file berdasarkan waktu modifikasi
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
        # Hapus file tertua
        os.remove(os.path.join(folder, log_files[0]))

# Fungsi untuk mengonversi Excel ke JSON dengan struktur tetap
def excel_to_json(input_file, output_file, log_folder):
    try:
        # Membaca file Excel
        df = pd.read_excel(input_file, sheet_name=None, dtype=str)  # Membaca semua sheet

        intents = []

        # Loop melalui setiap sheet
        for sheet_name, data in df.items():
            # Pastikan kolom yang dibutuhkan ada
            if 'tag' in data.columns and 'patterns' in data.columns and 'responses' in data.columns:
                for _, row in data.iterrows():
                    # Mengonversi pola dan respons menjadi list
                    patterns = row['patterns'].split('|') if pd.notna(row['patterns']) else []
                    responses = row['responses'].split('|') if pd.notna(row['responses']) else []

                    # Menambahkan intent ke dalam list
                    intents.append({
                        "tag": row['tag'],
                        "patterns": patterns,
                        "responses": responses
                    })

        # Menyimpan hasil ke file JSON (utama)
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump({"intents": intents}, json_file, indent=4, ensure_ascii=False)

        # Membuat nama file dengan timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_folder, f"intents_{timestamp}.json")

        # Menyimpan hasil ke file JSON dengan timestamp
        with open(log_file, 'w', encoding='utf-8') as json_file:
            json.dump({"intents": intents}, json_file, indent=4, ensure_ascii=False)

        # Kelola jumlah log agar tidak lebih dari 10
        manage_logs(log_folder)

        print(f"Data berhasil dikonversi dari Excel ke JSON: {output_file}")
        print(f"Log file berhasil disimpan: {log_file}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Jalankan fungsi
input_excel_file = "intents.xlsx"  # File Excel yang telah diedit
output_json_file = "intents.json"  # File JSON hasil konversi utama
log_update_folder = r"LOG_UPDATE\JSON"  # Folder log update

# Pastikan folder log ada
os.makedirs(log_update_folder, exist_ok=True)

excel_to_json(input_excel_file, output_json_file, log_update_folder)
