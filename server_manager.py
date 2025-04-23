import subprocess
import asyncio
import telnetlib3

class ServerManager:
    def __init__(self, telnet_port="19021"):
        """
        Inicjalizuje menedżera serwera RTT.
        :param telnet_port: Port Telnet dla RTT.
        """
        self.telnet_port = telnet_port
        self.process = None
        self._reader = None
        self._writer = None

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

    async def connect_to_rtt(self, host="localhost", port=None):
        """
        Podłącza się do serwera RTT.
        """
        if port is None:
            port = self.telnet_port

        try:
            print(f"🔌 Łączenie z serwerem RTT na {host}:{port}...")
            self._reader, self._writer = await telnetlib3.open_connection(host, port)
            print("✅ Połączono z RTT")
            asyncio.create_task(self._read_rtt_messages())
        except Exception as e:
            print(f"❌ Błąd podczas łączenia z RTT: {e}")
            self._reader = None
            self._writer = None

    async def _read_rtt_messages(self):
        """
        Nasłuchuje wiadomości przychodzących z serwera RTT.
        """
        try:
            while True:
                data = await self._reader.read(1024)
                if data:
                    print(f"📥 Odebrano wiadomość RTT: {data.strip()}")
        except Exception as e:
            print(f"❌ Błąd podczas odczytu wiadomości RTT: {e}")