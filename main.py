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
    @Slot(str)
    def senddata(self,data):
        if self._writer and data:
            print(f"Sending data: {data}")
            self._writer.write(data + "\n")
            self.add_received_data(f"Sent: {data}")
            
    @Slot(result=list)
    def get_usb_devices(self):
        context = pyudev.Context()
        devices = []
        for device in context.list_devices(subsystem='usb',DEVTYPE='usb_device'):
            device_name = device.get('ID_MODEL', 'Unknown')
            device_node = device.device_node.rsplit('/', 1)[-1]
            devices.append(f"{device_name}")
        return devices
    @Slot()
    def send_hejka(self):
        print("Sending hejka")
        self._last_command_data.clear()
        self._writer.write("hejka")
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
    @Slot(str)
    def send_and_listen(self):
        pass

if __name__ == "__main__":


    app = QGuiApplication(sys.argv)

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    context_object = QObject()
    rtt_handler = RTTHandler()
    engine.rootContext().setContextProperty("rttHandler",rtt_handler)

    if not engine.rootObjects():
        sys.exit(-1)

    with loop:
        loop.run_forever()
    sys.exit(app.exec())
