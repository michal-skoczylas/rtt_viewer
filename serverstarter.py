#!/usr/bin/env python3
import subprocess
import time

def start_jlink_server():
    print("🔄 Uruchamianie serwera J-Link...")
    process = subprocess.Popen(
        ["JLinkExe", "-device", "STM32F407VG", "-if", "SWD", "-speed", "4000", "-autoconnect", "1", "-RTTTelnetPort", "19021"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"✅ Serwer J-Link działa (PID: {process.pid})")
    print("🔌 Telnet: 127.0.0.1:19021")
    print("🛑 CTRL+C aby zatrzymać")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate()
        print("\n🛑 Serwer J-Link zatrzymany")

if __name__ == "__main__":
    start_jlink_server()