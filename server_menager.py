import subprocess
import time

class ServerManager:
    def __init__(self, device="STM32F407VG", interface="SWD", speed="4000", telnet_port="19021"):
        """
        Inicjalizuje menedżera serwera RTT.
        :param device: Nazwa urządzenia (np. STM32F407VG).
        :param interface: Interfejs (np. SWD lub JTAG).
        :param speed: Prędkość komunikacji (np. 4000 kHz).
        :param telnet_port: Port Telnet dla RTT.
        """
        self.device = device
        self.interface = interface
        self.speed = speed
        self.telnet_port = telnet_port
        self.process = None

    def start_server(self):
        """Uruchamia serwer RTT jako proces w tle."""
        if self.process is not None:
            print("⚠️ Serwer RTT już działa!")
            return

        print("🔄 Uruchamianie serwera RTT...")
        try:
            self.process = subprocess.Popen(
                [
                    "JLinkExe",
                    "-device", self.device,
                    "-if", self.interface,
                    "-speed", self.speed,
                    "-autoconnect", "1",
                    "-RTTTelnetPort", self.telnet_port
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Serwer RTT uruchomiony (PID: {self.process.pid})")
        except FileNotFoundError:
            print("❌ Nie znaleziono JLinkExe. Upewnij się, że jest w PATH.")
        except Exception as e:
            print(f"❌ Błąd podczas uruchamiania serwera RTT: {e}")

    def stop_server(self):
        """Zatrzymuje działający serwer RTT."""
        if self.process is None:
            print("⚠️ Serwer RTT nie działa!")
            return

        print("🛑 Zatrzymywanie serwera RTT...")
        try:
            self.process.terminate()
            self.process.wait()
            print("✅ Serwer RTT zatrzymany")
        except Exception as e:
            print(f"❌ Błąd podczas zatrzymywania serwera RTT: {e}")
        finally:
            self.process = None

    def is_running(self):
        """Sprawdza, czy serwer RTT działa."""
        if self.process is not None and self.process.poll() is None:
            print(f"✅ Serwer RTT działa (PID: {self.process.pid})")
            return True
        print("❌ Serwer RTT nie działa")
        return False