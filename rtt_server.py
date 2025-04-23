import subprocess
import time

class RTTServer:
    def __init__(self, port="19021"):
        self.port = port
        self.process = None

    def start(self):
        try:
            print(f"🔄 Starting RTT server on port {self.port}...")
            self.process = subprocess.Popen(
                ["JLinkRTTClient", "-RTTTelnetPort", self.port],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Server started (PID: {self.process.pid})")
            return True
        except FileNotFoundError:
            print("❌ Error: JLinkRTTClient not found. Is SEGGER software installed?")
            return False
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False

    def stop(self):
        if self.process:
            print("🛑 Stopping server...")
            self.process.terminate()
            self.process.wait()
            print("✅ Server stopped")

if __name__ == "__main__":
    server = RTTServer()
    if server.start():
        try:
            print("Server running, press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()