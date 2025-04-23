import pylink
import time


def connect_to_device(speed=4000):
    """Łączy się z urządzeniem za pomocą J-Link."""
    jlink = pylink.JLink()
    try:
        print(f"🔌 Connecting to device: STM32F413ZH at {speed} kHz...")
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)  # Ustaw interfejs na SWD
        jlink.connect(chip_name="STM32F413ZH", speed=speed)  # Użyj poprawnej nazwy urządzenia
        print("✅ Connected to device")
        return jlink
    except pylink.errors.JLinkException as e:
        print(f"❌ Connection error: {e}")
        jlink.close()
        return None


def start_rtt(jlink):
    """Uruchamia RTT na urządzeniu."""
    try:
        print("🔄 Starting RTT...")
        jlink.rtt_start()
        print("✅ RTT started")
        return True
    except pylink.errors.JLinkException as e:
        print(f"❌ RTT start error: {e}")
        return False


def listen_to_rtt(jlink):
    """Nasłuchuje wiadomości z RTT."""
    print("📡 Listening for messages from RTT...")
    try:
        while True:
            data = jlink.rtt_read(0, 1024)  # Odczytaj do 1024 bajtów z kanału 0
            if data:
                # Konwertuj listę liczb całkowitych na ciąg bajtów
                message = bytes(data).decode('utf-8').strip()
                print(f"📥 Received: {message}")
            else:
                print("⚠️ No data received")
            time.sleep(0.5)  # Oczekuj 0.5 sekundy przed kolejnym odczytem
    except KeyboardInterrupt:
        print("🛑 Stopping RTT listener...")
    except pylink.errors.JLinkException as e:
        print(f"❌ Error reading message: {e}")


def main():
    """Główna funkcja skryptu."""
    speed = 4000

    # Połącz się z urządzeniem
    jlink = connect_to_device(speed)
    if not jlink:
        return

    # Uruchom RTT
    if not start_rtt(jlink):
        jlink.close()
        return

    # Nasłuchuj wiadomości
    try:
        listen_to_rtt(jlink)
    finally:
        print("🔌 Closing connection...")
        jlink.rtt_stop()
        jlink.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    main()