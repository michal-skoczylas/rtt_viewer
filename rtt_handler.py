# This Python file uses the following encoding: utf-8
import asyncio
import telnetlib3
import pyudev
from PySide6.QtCore import QObject, Slot, Signal, Property, QStringListModel
from PySide6.QtWidgets import QFileDialog
import tree


class RTTHandler(QObject):
    # Sygnały
    dataReady = Signal(list)  # Emitowany, gdy dane są gotowe do uzupełnienia modelu
    received_data_changed = Signal()  # Emitowany, gdy odebrane dane się zmienią
    

    def __init__(self):
        super().__init__()
        self._received_data = []
        self._writer = None
        self._tree = tree.Tree()  # Inicjalizacja drzewa
        self._directories_model = QStringListModel()  # Model dla QML
        self._last_command_data = []  # Przechowywanie ostatnich danych
        self.create_tree_from_sample_data()

    # Właściwość do wyświetlania odebranych danych
    @Property(str, notify=received_data_changed)
    def received_data(self):
        return "\n".join(self._last_command_data)

    # Dodawanie odebranych danych
    def add_received_data(self, data):
        self._received_data.append(data)
        self._last_command_data.append(data)
        self.received_data_changed.emit()

    # Tworzenie drzewa na podstawie przykładowych danych
    @Slot()
    def create_tree_from_sample_data(self):
        sample_data = """
        root/A
        root/A/A1
        root/A/A2
        root/B
        root/B/B1
        root/B/B2
        root/C
        """
        self._tree = tree.Tree()
        for line in sample_data.strip().split("\n"):
            line = line.strip()  # Usuń dodatkowe białe znaki
            self._tree.add_path(line)
        print("Tree created from sample data:")
        self._tree.print_tree()

    # Uzupełnianie ComboBoxa folderami z pierwszego poziomu drzewa
    @Slot()
    def fill_combobox(self):
        if self._tree:
            first_level = self._tree.get_top_level_folders()
            print("First-level directories:", first_level)  # Debugowanie
            self.dataReady.emit(first_level)  # Emituj sygnał z listą folderów
        else:
            print("Tree not initialized")

    # Uzupełnaianie comboboxa plikami z wybranego folderu
    @Slot(str,result=list)
    def get_folder_contents(self,folder_name):
        """
    Zwraca zawartość (podfoldery i pliki) danego folderu.
    :param folder_name: Nazwa folderu, którego zawartość chcemy uzyskać.
    :return: Lista podfolderów i plików w danym folderze.
    """ 
        if self._tree:
            contents = self._tree.get_folder_contents(folder_name)
            print(f"Contens of selected folder: '{folder_name}:'",contents)
            return contents
        else:
            print("tree not initialized")
            return []
    # Pobieranie listy urządzeń USB
    @Slot(result=list)
    def get_usb_devices(self):
        context = pyudev.Context()
        devices = []
        for device in context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
            device_name = device.get('ID_MODEL', 'Unknown')
            devices.append(device_name)
        return devices

    # Wybór ścieżki zapisu pliku
    @Slot()
    def select_save_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            None, "Save RTT Data", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            print(f"Selected save path: {file_path}")
            self.save_rtt_data_to_file(file_path)

    # Zapis danych RTT do pliku
    def save_rtt_data_to_file(self, filepath):
        try:
            with open(filepath, "w") as file:
                file.write("\n".join(self._last_command_data))
            print(f"Data saved to: {filepath}")
        except Exception as e:
            print(f"Error saving file: {e}")

    # Odczyt danych RTT
    @Slot()
    def read_rtt(self):
        asyncio.create_task(self._read_rtt())

    async def _read_rtt(self):
        host = "localhost"
        port = 19021
        print(f"Connecting to {host}:{port}")

        try:
            reader, writer = await telnetlib3.open_connection(host, port)
            self._writer = writer
            print("Connected to RTT, waiting for data...")

            while True:
                data = await reader.read(1024)
                if data:
                    print("Received:", data.strip())
                    self.add_received_data(data.strip())
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self._writer:
                self._writer.close()

    # Wysłanie polecenia `file_list` do RTT
    @Slot()
    def send_file_list_command(self):
        if self._writer:
            command = "file_list\n"
            self._writer.write(command)
            print(f"Sent command: {command.strip()}")
            asyncio.create_task(self._read_file_list_response())

    async def _read_file_list_response(self):
        if self._writer:
            try:
                data = await self._writer.read(1024)
                if data:
                    print("Received file list:", data.strip())
                    self.add_received_data(data.strip())
                    self._tree = tree.Tree()
                    for line in data.strip().split("\n"):
                        self._tree.add_path(line)
                    self._tree.print_tree()
            except Exception as e:
                print(f"Error: {e}")
