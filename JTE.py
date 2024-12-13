import json
import pandas as pd
import os
from datetime import datetime

# Membaca file intents.json
with open('intents.json', 'r') as file:
    data = json.load(file)

# Daftar tag yang akan digabungkan ke satu kategori "Gabungan"
combined_tags = [
    "Overall_Hotel","Overall_Layanan","Overall_Transport","Overall_Wisata","Overall_Kuliner","Pengurus_TP_PKK_Anggota","Perangkat_Desa","Lembaga_Kemasyarakatan_BPD","Layanan_Masyarakat_Borobudur"
]

# Daftar awalan untuk kategori lainnya
categories = {
    "basic":[],
    "introduce":[],
    "desbo":[],
    "canbo":[],
    "Hotel": [],
    "Layanan": [],
    "Transport": [],
    "Wisata": [],
    "Kuliner": [],
    "Pengurus_TP": [],
    "Perangkat_Desa": [],
    "Lembaga_Kemasyarakatan": [],
}

# Tambahkan kategori "Gabungan"
categories["Gabungan"] = []

# Mengelompokkan intents berdasarkan kategori
for intent in data["intents"]:
    tag = intent["tag"]
    if tag in combined_tags:
        categories["Gabungan"].append(intent)
    elif tag.startswith("Agama"):
        categories["Agama"].append(intent)
    else:
        categorized = False
        for prefix in categories.keys():
            if tag.startswith(prefix) and prefix != "Gabungan":
                categories[prefix].append(intent)
                categorized = True
                break
        if not categorized:
            # Jika tidak cocok dengan kategori apa pun, masukkan ke kategori "Lainnya"
            if "Lainnya" not in categories:
                categories["Lainnya"] = []
            categories["Lainnya"].append(intent)

# Lokasi output
output_file_main = "intents.xlsx"  # File utama
output_folder_log = r"LOG_UPDATE\SHEET"  # Folder log
os.makedirs(output_folder_log, exist_ok=True)  # Membuat folder jika belum ada

# Nama file dengan timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_timestamp = os.path.join(output_folder_log, f"intents_{timestamp}.xlsx")

# Fungsi untuk membatasi jumlah file log
def manage_logs(folder, max_logs=10):
    log_files = [f for f in os.listdir(folder) if f.startswith("intents_") and f.endswith(".xlsx")]
    if len(log_files) > max_logs:
        # Urutkan file berdasarkan waktu modifikasi
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
        # Hapus file tertua
        os.remove(os.path.join(folder, log_files[0]))

# Membuat kedua file Excel
for output_file in [output_file_main, output_file_timestamp]:
    with pd.ExcelWriter(output_file) as writer:
        for category, intents in categories.items():
            df = pd.DataFrame(intents)

            # Mengonversi `patterns` dan `responses` ke format yang sesuai
            df['patterns'] = df['patterns'].apply(lambda x: "|".join(x) if isinstance(x, list) else x)
            df['responses'] = df['responses'].apply(lambda x: "|".join(x) if isinstance(x, list) else x)

            # Menulis data ke sheet
            df.to_excel(writer, sheet_name=category[:30], index=False)  # Sheet name max 31 chars

    if output_file == output_file_main:
        print(f"File utama berhasil dibuat: {output_file}")
    else:
        print(f"File dengan timestamp berhasil dibuat: {output_file}")
        # Kelola log untuk memastikan hanya ada maksimal 10 file
        manage_logs(output_folder_log)

