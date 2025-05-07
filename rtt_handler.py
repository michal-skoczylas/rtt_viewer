# This Python file uses the following encoding: utf-8
import asyncio
import telnetlib3
import pyudev
import subprocess
from PySide6.QtCore import QObject, Slot, Signal, Property, QStringListModel
from PySide6.QtWidgets import QFileDialog
import tree

class RTTHandler(QObject):
    dataReady = Signal(list)
    received_data_changed = Signal()
    connection_status_changed = Signal(bool)
    usb_devices_changed = Signal(list)

    def __init__(self):
        super().__init__()
        self._received_data = []
        self._reader = None
        self._writer = None
        self._rtt_process = None
        self._tree = tree.Tree()
        self._directories_model = QStringListModel()
        self._last_command_data = []
        self._is_connecting = False
        self._telnet_port = "19021"
        self._usb_devices = []

        # Initialize components
        self.create_tree_from_sample_data()

    # Tree and file operations
    @Slot()
    def create_tree_from_sample_data(self):
        """Creates sample tree structure"""
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
            line = line.strip()
            self._tree.add_path(line)
        print("Sample tree created:")
        self._tree.print_tree()

    @Slot()
    def fill_combobox(self):
        """Fills combobox with top-level directories"""
        if self._tree:
            first_level = self._tree.get_top_level_folders()
            print("First-level directories:", first_level)
            self.dataReady.emit(first_level)
        else:
            print("Tree not initialized")

    @Slot(str, result=list)
    def get_folder_contents(self, folder_name):
        """Returns contents of specified folder"""
        if self._tree:
            contents = self._tree.get_folder_contents(folder_name)
            print(f"Contents of '{folder_name}':", contents)
            return contents
        else:
            print("Tree not initialized")
            return []

    @Slot(str, str)
    def process_selected_items(self, folder_name, file_name):
        """Processes selected folder and file"""
        if not folder_name or not file_name:
            print("Folder or file not selected")
            return
        
        full_path = f"{folder_name}/{file_name}"
        print(f"Processing selected item: {full_path}")
        self.send_message(f"cat {full_path}")

    @Slot(str, str)
    def construct_message(self, dir_name, file_name):
        """Constructs RTT command from UI selection"""
        message = f"cat {dir_name}/{file_name}"
        print(f"Constructed message: {message}")
        return message

    # USB device handling
    @Slot(result=list)
    def get_usb_devices(self):
        """Returns list of connected USB devices"""
        context = pyudev.Context()
        self._usb_devices = []
        try:
            for device in context.list_devices(subsystem="usb", DEVTYPE="usb_device"):
                device_name = device.get("ID_MODEL", "Unknown")
                self._usb_devices.append(device_name)
            self.usb_devices_changed.emit(self._usb_devices)
            return self._usb_devices
        except Exception as e:
            print(f"Error getting USB devices: {e}")
            return []

    # File operations
    @Slot()
    def select_save_path(self):
        """Opens file dialog to select save path"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            None, "Save RTT Data", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            print(f"Selected save path: {file_path}")
            self.save_rtt_data_to_file(file_path)

    def save_rtt_data_to_file(self, filepath):
        """Saves RTT data to file"""
        try:
            with open(filepath, "w") as file:
                file.write("\n".join(self._last_command_data))
            print(f"Data saved to: {filepath}")
        except Exception as e:
            print(f"Error saving file: {e}")

    @Slot(str, str, str)
    def read_file(self, dir_name, file_name, save_path):
        """Reads file from RTT and saves to disk"""
        asyncio.create_task(self._read_file(dir_name, file_name, save_path))

    async def _read_file(self, dir_name, file_name, save_path):
        """Async file reading operation"""
        if not self._writer:
            print("Not connected to RTT")
            return

        try:
            command = f"cat {dir_name}/{file_name}"
            self._writer.write(command + "\n")
            await self._writer.drain()

            with open(save_path, "wb") as file:
                while True:
                    data = await self._reader.read(1024)
                    if not data:
                        break
                    file.write(data.encode("utf-8"))
                    print(f"Received {len(data)} bytes")

            print(f"File saved to: {save_path}")
        except Exception as e:
            print(f"Error reading file: {e}")

    # Utility methods
    @Slot()
    def send_file_list_command(self):
        """Sends file_list command to RTT"""
        self.send_message("file_list")

    @Slot()
    def send_hello_message(self):
        """Sends test message to RTT"""
        self.send_message("hejka")

    @Slot()
    def clear_received_data(self):
        """Clears received data buffer"""
        self._last_command_data = []
        self.received_data_changed.emit()
        print("Received data cleared")