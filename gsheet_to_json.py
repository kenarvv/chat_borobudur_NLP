import pandas as pd
import json
import requests
import io
import time

# Fungsi untuk membaca data dari Google Sheets dalam format CSV
def fetch_public_gsheet_csv(spreadsheet_url):
    """
    Mengambil data dari Google Sheets publik dalam format CSV.
    :param spreadsheet_url: URL Google Sheets
    :return: DataFrame berisi data dari sheet
    """
    # print("Program selesai berjalan sekitar 60 detik")
    # time.sleep(30)  # Diberikan delay selama 30 detik untuk memastikan data pada google sheets sudah tersimpan terlebih dahulu
    try:
        # Mengunduh data dalam format CSV
        response = requests.get(spreadsheet_url)
        response.raise_for_status()  # Memastikan permintaan berhasil

        # Membaca data CSV menjadi DataFrame
        df = pd.read_csv(io.StringIO(response.text), on_bad_lines='skip')  # Menangani baris yang salah
        print("Kolom yang ditemukan:", df.columns)  # Menampilkan kolom yang ada di CSV

        return df
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca Google Sheets: {e}")
        return None

# Fungsi untuk mengonversi DataFrame ke file JSON
def dataframe_to_json(df, output_file):
    """
    Konversi DataFrame ke file JSON dengan struktur intents chatbot.
    :param df: DataFrame berisi data chatbot
    :param output_file: Nama file JSON hasil konversi
    """
    try:
        intents = []

        # Pastikan kolom 'patterns' dan 'responses' ada
        if 'patterns' not in df.columns or 'responses' not in df.columns:
            print("Kolom 'patterns' atau 'responses' tidak ditemukan dalam DataFrame.")
            return
        
        # Proses setiap baris data
        for _, row in df.iterrows():
            patterns = row['patterns'].split('|') if pd.notna(row['patterns']) else []
            responses = row['responses'].split('|') if pd.notna(row['responses']) else []
            intents.append({
                "tag": row['tag'],
                "patterns": patterns,
                "responses": responses
            })

        # Simpan ke file JSON utama
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump({"intents": intents}, json_file, indent=4, ensure_ascii=False)

        print(f"Data berhasil dikonversi ke JSON: {output_file}")

    except Exception as e:
        print(f"Terjadi kesalahan saat mengonversi data ke JSON: {e}")

# URL Google Sheets dan ID sheet (gid)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-vU-qVPt77la8GaWSIp-HDxxZawbknDTat_tXHCJpbgHP1kHO-W4Mx69cNqgVnM5wk-nbegpkH-Me/pub?output=csv"  # Ganti dengan URL Anda
output_json_file = "intents.json"  # Nama file output JSON

# Ambil data dari Google Sheets dan simpan ke JSON
df = fetch_public_gsheet_csv(spreadsheet_url)
if df is not None:
    dataframe_to_json(df, output_json_file)
else:
    print("Gagal membaca data dari Google Sheets.")
