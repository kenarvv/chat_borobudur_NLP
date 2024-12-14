import subprocess
import sys

def run_gsheet_to_json_and_train():
    try:
        # Menjalankan gsheet_to_json.py
        subprocess.run([sys.executable, 'gsheet_to_json.py'], check=True)
        print("gsheet_to_json.py berhasil dijalankan.")
        
        # Menjalankan train.py
        subprocess.run([sys.executable, 'train.py'], check=True)
        print("train.py berhasil dijalankan.")
    
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menjalankan skrip: {e}")
        return False
    return True

if __name__ == "__main__":
    # Jalankan pembaruan model
    if run_gsheet_to_json_and_train():
        print("Model berhasil diperbarui.")
    else:
        print("Terjadi kesalahan saat memperbarui model.")
