# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import telnetlib3
import time
import asyncio
import qasync
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property, Signal
from PySide6.QtWidgets import QFileDialog
import pyudev
import tree
class RTTHandler(QObject):
    received_data_changed = Signal()  # Signal emitted when data changes

    def __init__(self):
        super().__init__()
        self._received_data = []
        self._max_lines = 20
        self._writer = None        
        self._last_command_data=[]

 
        
    @Property(str, notify=received_data_changed)
    def received_data(self):
        return "\n".join(self._last_command_data[-self._max_lines:])    
    def add_received_data(self, data):
        self._received_data.append(data)
        self._last_command_data.append(data)
        self.received_data_changed.emit()  # Emit signal when data changes

    @Slot()
    def read_rtt(self):
        asyncio.create_task(self._read_rtt())
        

    async def _read_rtt(self):
        host = "localhost"
        port = 19021
        
        print(f"Connecting with {host}:{port}")
        
        # Connect to telnet
        reader, writer = await telnetlib3.open_connection(host, port)
        self._writer = writer        
        print("Connected with RTT, Waiting for data...")
        
        try:
            # Continuous reading
            while True:
                data = await reader.read(1024)  # Read 1024 bytes
                if data:
                    print("Received: ", data.strip())
                    self.add_received_data(data.strip()) 
                await asyncio.sleep(0.1)
        except Exception as e:
            print("Error: ", e)
        finally:
            print("Closing connection")
            writer.close()
            await writer.wait_closed()
    #Send file_list command to rtt and read response
    @Slot()
    def send_file_list_command(self):
        if self._writer:
            command = 'file_list\n'
            self._writer.write(command)
            print(f"Sent command: {command.strip()}")
            asyncio.create_task(self._read_file_list_response())
    async def _read_file_list_response(self):
        if self._writer:
            try:
                data = await self._writer.read(1024)  # Read 1024 bytes
                if data:
                    print("Received file list: ", data.strip())
                    self.add_received_data(data.strip()) 
                    tree_obj = tree.Tree("root")
                    tree_obj = tree_obj.from_string(data)
                    tree_obj.print_tree()
                await asyncio.sleep(0.1)
            except Exception as e:
                print("Error: ", e)
        
    
    
   #Get device list 
    @Slot(result=list)
    def get_usb_devices(self):
        context = pyudev.Context()
        devices = []
        for device in context.list_devices(subsystem='usb',DEVTYPE='usb_device'):
            device_name = device.get('ID_MODEL', 'Unknown')
            device_node = device.device_node.rsplit('/', 1)[-1]
            devices.append(f"{device_name}")
        return devices
    #Select Save Path    
    @Slot()    
    def select_save_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            None,"Save rtt data","","Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            print(f"Selected save path: {file_path}")
            self.save_rtt_data_to_file(file_path)
        
        def save_rtt_data_to_file(self,filepath):
            try:
                with open(filepath,"w") as file:
                    file.write("\n".join(self._last_command_data))
                print(f"data saved to: {filepath}")
            except Exception as e:
                print(f"Error saving file: {e}")
    