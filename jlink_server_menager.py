import subprocess

class JLinkServerMenager():
    def __init__(self):
        self.process = None
    
    def start_server(self):
        """Funkcja uruchamiająca serwer JLink jako proces w tle
        """
        if self.process is None:
            print("Uruchamianie serwera JLink...")
            self.process = subprocess.Popen(
                ["JLinkExe", "-autoconnect","1"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text = True
            )
            print(f" Serwer JLink działa (PID: {self.process.pid})")
    
    def stop_server(self):
        """Funkcja zatrzymująca serwer JLink
        """
        if self.process:
            print("Zatrzymywanie serwera JLink...")
            self.process.terminate()
            self.process.wait()
            self.process=None
            print("Serwer JLink zatrzymany")