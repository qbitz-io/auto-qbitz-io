import subprocess
import time
import sys

API_COMMAND = [sys.executable, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]


def run_api_server():
    while True:
        print("Starting API server...")
        process = subprocess.Popen(API_COMMAND)
        process.wait()
        print(f"API server exited with code {process.returncode}")
        print("Restarting API server in 3 seconds...")
        time.sleep(3)


if __name__ == "__main__":
    run_api_server()
