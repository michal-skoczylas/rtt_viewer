import pylink
import time

class RTTClient:
    def __init__(self, device="Cortex-M4", speed=4000):
        """
        Inicjalizuje klienta RTT.
        :param device: Nazwa urządzenia (np. Cortex-M4).
        :param speed: Prędkość komunikacji w kHz.
        """
        self.device = device
        self.speed = speed
        self.jlink = pylink.JLink()
        self.rtt_started = False

    def connect(self):
        """Łączy się z urządzeniem za pomocą J-Link."""
        try:
            print(f"🔌 Connecting to device: {self.device} at {self.speed} kHz...")
            self.jlink.open()
            self.jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)  # Ustaw interfejs na SWD
            self.jlink.connect(self.device, speed=self.speed)
            print("✅ Connected to device")
        except pylink.errors.JLinkException as e:
            print(f"❌ Connection error: {e}")
            self.jlink.close()

    def start_rtt(self):
        """Uruchamia RTT na urządzeniu."""
        try:
            print("🔄 Starting RTT...")
            self.jlink.rtt_start()
            self.rtt_started = True
            print("✅ RTT started")
        except pylink.errors.JLinkException as e:
            print(f"❌ RTT start error: {e}")

    def send_message(self, message):
        """Wysyła wiadomość do RTT."""
        if not self.rtt_started:
            print("❌ RTT is not started")
            return

        try:
            print(f"📤 Sending message: {message}")
            self.jlink.rtt_write(0, message.encode('utf-8'))  # Kanał 0
            print("✅ Message sent")
        except pylink.errors.JLinkException as e:
            print(f"❌ Error sending message: {e}")

    def read_message(self):
        """Odczytuje wiadomość z RTT."""
        if not self.rtt_started:
            print("❌ RTT is not started")
            return

        try:
            print("📡 Reading message from RTT...")
            time.sleep(1)  # Czekaj chwilę, aby wiadomość mogła zostać odebrana
            data = self.jlink.rtt_read(0, 1024)  # Odczytaj do 1024 bajtów z kanału 0
            if data:
                print(f"📥 Received: {data.decode('utf-8').strip()}")
            else:
                print("⚠️ No data received")
        except pylink.errors.JLinkException as e:
            print(f"❌ Error reading message: {e}")

    def close(self):
        """Zamyka połączenie RTT i J-Link."""
        print("🔌 Closing connection...")
        if self.rtt_started:
            self.jlink.rtt_stop()
        self.jlink.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    client = RTTClient()
    try:
        client.connect()
        client.start_rtt()
        client.send_message("hejka")
        client.read_message()
    except KeyboardInterrupt:
        print("🛑 Stopping client...")
    finally:
        client.close()