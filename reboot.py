import os
import sys
import time
import signal
import subprocess

def kill_app():
    try:
        # Read the PID from the file
        with open('app.pid', 'r') as f:
            pid = int(f.read().strip())
        
        # Kill the process
        os.kill(pid, signal.SIGTERM)
        
        # Wait a bit to ensure the process is terminated
        time.sleep(2)
        
        return True
    except FileNotFoundError:
        print("PID file not found")
        return False
    except ProcessLookupError:
        print("Process not found")
        return False
    except Exception as e:
        print(f"Error killing process: {e}")
        return False

def start_app():
    try:
        # Start app.py in a new process
        subprocess.Popen([sys.executable, 'app.py'])
        return True
    except Exception as e:
        print(f"Error starting app: {e}")
        return False

if __name__ == "__main__":
    # Kill the existing app
    if kill_app():
        print("Successfully killed existing app")
        # Start the app again
        if start_app():
            print("Successfully started new app instance")
        else:
            print("Failed to start new app instance")
    else:
        print("Failed to kill existing app")