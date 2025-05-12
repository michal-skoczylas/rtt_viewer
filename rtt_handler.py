# This Python file uses the following encoding: utf-8
import asyncio
import telnetlib3
import pyudev
import time
import subprocess
from PySide6.QtCore import QObject, Slot, Signal, Property, QStringListModel
from PySide6.QtWidgets import QFileDialog
import tree
import pylink
import os
from pylink.enums import JLinkInterfaces

class RTTHandler(QObject):
    dataReady = Signal(list)
    received_data_changed = Signal()
    connection_status_changed = Signal(bool)
    usb_devices_changed = Signal(list)
    CHIP_NAME="STM32F413ZH"
    RTT_CHANNEL=0
    jlink = pylink.JLink()


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
    @Slot()
    def board_setup(self,chip_name="STM32F413ZH",rtt_channel=0):
        self.CHIP_NAME =chip_name
        self.RTT_CHANNEL = rtt_channel
    #Powinno wysylac komende poczekac na odpowiedz i na jej podstawie utworzyc drzewo, trzeba to jakos przemylsec
    @Slot()
    def send_file_list_message(self):
        """Sends a super message to STM via rtt in order to receive file tree"""
        try:
            self.jlink.open()
            self.jlink.set_tif(JLinkInterfaces.SWD)
            self.jlink.connect(self.CHIP_NAME)
            self.jlink.rtt_start()
            bytes_written = self.jlink.rtt_write(0, b'super') 
            print(f"Successfully sent {bytes_written} bytes. Data: 'super'")
            if bytes_written==0:
                print("RTT buffer is full, retrying...")
                time.sleep(0.01)
                bytes_written = self.jlink.rtt_write(0, b'super') 
                
        except Exception as e:
           # Szczegółowe logowanie błędu
           print(f"Failed to send 'super' command. Error details:")
           print(f"Exception type: {type(e).__name__}")
           print(f"Error message: {str(e)}")

           # Dodatkowe informacje debugowe
           print("\nDebug info:")
           print(f"Is JLink connected: {hasattr(self.jlink, 'connected') and self.jlink.connected}")
           print(f"Chip name: {self.CHIP_NAME}")
           print(f"Interface type: {JLinkInterfaces.SWD}")

