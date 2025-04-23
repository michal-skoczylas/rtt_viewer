import telnetlib3
import asyncio

async def listen_to_rtt(host="localhost", port=19021):
    """Łączy się z serwerem RTT przez Telnet i nasłuchuje wiadomości."""
    print(f"🔌 Connecting to RTT server at {host}:{port}...")
    try:
        # Połącz się z serwerem RTT
        reader, writer = await telnetlib3.open_connection(host, port)
        print("✅ Connected to RTT server")

        print("📡 Listening for messages from RTT...")
        while True:
            # Odczytaj wiadomość z serwera RTT
            message = await reader.read(1024)  # Odczytaj do 1024 znaków
            if message:
                print(f"📥 Received: {message.strip()}")
            else:
                print("⚠️ No data received")
            await asyncio.sleep(0.5)  # Oczekuj 0.5 sekundy przed kolejnym odczytem
    except asyncio.CancelledError:
        print("🛑 Stopping RTT listener...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🔌 Closing connection...")
        writer.close()
        await writer.wait_closed()
        print("✅ Connection closed")

def main():
    """Główna funkcja skryptu."""
    host = "localhost"
    port = 19021

    # Uruchom pętlę nasłuchiwania RTT
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(listen_to_rtt(host, port))
    except KeyboardInterrupt:
        print("🛑 Stopping application...")
    finally:
        loop.close()

if __name__ == "__main__":
    main()