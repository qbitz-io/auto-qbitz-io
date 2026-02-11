import unittest
import subprocess
import sys
import time

class SupervisorSimulationTest(unittest.TestCase):
    def test_supervisor_loop(self):
        # This test simulates the supervisor loop logic by running the supervisor script
        # and checking that it restarts the API server process on exit.

        supervisor_process = subprocess.Popen([sys.executable, "backend/supervisor.py"])
        time.sleep(5)  # Wait for API server to start

        # Terminate the API server process to simulate crash
        import psutil
        api_process = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'uvicorn' in proc.info['name'] or (proc.info['cmdline'] and 'uvicorn' in proc.info['cmdline'][0]):
                api_process = proc
                break

        self.assertIsNotNone(api_process, "API server process not found")

        api_process.terminate()
        api_process.wait(timeout=10)

        # Wait for supervisor to restart the API server
        time.sleep(10)

        # Check if a new API server process is running
        new_api_process = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'uvicorn' in proc.info['name'] or (proc.info['cmdline'] and 'uvicorn' in proc.info['cmdline'][0]):
                if proc.pid != api_process.pid:
                    new_api_process = proc
                    break

        self.assertIsNotNone(new_api_process, "API server was not restarted by supervisor")

        # Cleanup
        supervisor_process.terminate()
        supervisor_process.wait(timeout=10)

if __name__ == '__main__':
    unittest.main()
