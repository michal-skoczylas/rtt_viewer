#!/usr/bin/env python3
import telnetlib

def connect_to_jlink_server(host="127.0.0.1", port=19021):
    print(f"🔌 Łączenie z serwerem J-Link na {host}:{port}...")
    try:
        with telnetlib.Telnet(host, port) as tn:
            print("✅ Połączono z serwerem J-Link")
            print("💬 Wpisz komendy (CTRL+C aby zakończyć):")
            
            while True:
                command = input("> ")
                if command.strip().lower() in ["exit", "quit"]:
                    print("🛑 Rozłączono z serwerem J-Link")
                    break
                tn.write(command.encode('ascii') + b"\n")
                response = tn.read_until(b"\n", timeout=1).decode('ascii')
                print(response.strip())
    except ConnectionRefusedError:
        print("❌ Nie udało się połączyć z serwerem J-Link. Upewnij się, że serwer działa.")
    except KeyboardInterrupt:
        print("\n🛑 Rozłączono z serwerem J-Link")

if __name__ == "__main__":
    connect_to_jlink_server()