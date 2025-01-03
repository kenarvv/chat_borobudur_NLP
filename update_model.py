import subprocess
import sys

def run_gsheet_to_json_and_train():
    try:
        # Run gsheet_to_json.py and capture its output
        result = subprocess.run(
            [sys.executable, 'gsheet_to_json.py'],
            capture_output=True,
            text=True,
            check=False
        )
        
        # If gsheet_to_json.py failed or reported errors
        if result.returncode != 0:
            error_messages = result.stdout.strip() or result.stderr.strip()
            return False, [error_messages]
            
        print("gsheet_to_json.py berhasil dijalankan.")
        
        # Run train.py
        train_result = subprocess.run(
            [sys.executable, 'train.py'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if train_result.returncode != 0:
            error_messages = train_result.stdout.strip() or train_result.stderr.strip()
            return False, [error_messages]
            
        print("train.py berhasil dijalankan.")
        return True, ["Model berhasil diperbarui."]
    
    except subprocess.CalledProcessError as e:
        return False, [f"Terjadi kesalahan saat menjalankan skrip: {e}"]
    except Exception as e:
        return False, [f"Terjadi kesalahan tidak terduga: {e}"]

if __name__ == "__main__":
    success, messages = run_gsheet_to_json_and_train()
    print("\n".join(messages))
    if not success:
        sys.exit(1)