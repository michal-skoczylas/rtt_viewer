import pylink
import os
from pylink.enums import JLinkInterfaces

def save_rtt_with_progress(total_size_kb=3):
    """Zapis danych RTT z wyświetlaniem postępu"""
    CHIP_NAME = "STM32F413ZH"
    RTT_CHANNEL = 0
    FILE_NAME = "hihi.txt"
    TOTAL_SIZE = total_size_kb * 1024  # Konwersja KB → bajty
    
    jlink = pylink.JLink()
    try:
        # Inicjalizacja
        jlink.open()
        jlink.set_tif(JLinkInterfaces.SWD)
        jlink.connect(CHIP_NAME)
        jlink.rtt_start()
        
        with open(FILE_NAME, 'w', encoding='utf-8') as file:
            print(f"Przesyłanie {total_size_kb} KB...")
            
            bytes_received = 0
            while bytes_received < TOTAL_SIZE:
                data = jlink.rtt_read(RTT_CHANNEL, 1024)
                if data:
                    text = bytes(data).decode('utf-8', errors='replace')
                    file.write(text)
                    bytes_received += len(data)
                    
                    # Oblicz i wyświetl postęp
                    progress = min(100, (bytes_received / TOTAL_SIZE) * 100)
                    print(f"\rPostęp: {progress:.1f}%", end='', flush=True)
            
            print("\nPrzesyłanie zakończone!")
            
    except KeyboardInterrupt:
        print("\nPrzerwano")
    finally:
        actual_size = os.path.getsize(FILE_NAME) / 1024
        print(f"Faktyczny rozmiar pliku: {actual_size:.2f} KB")
        jlink.rtt_stop()
        jlink.close()

if __name__ == "__main__":
    save_rtt_with_progress(total_size_kb=3)  # Dla 3 KB