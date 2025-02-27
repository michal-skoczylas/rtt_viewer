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


class RTTHandler(QObject):
    received_data_changed = Signal()  # Signal emitted when data changes

    def __init__(self):
        super().__init__()
        self._received_data = ""

    @Property(str, notify=received_data_changed)
    def received_data(self):
        return self._received_data

    @received_data.setter
    def received_data(self, value):
        if self._received_data != value:
            self._received_data = value
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
        
        print("Connected with RTT, Waiting for data...")
        
        try:
            # Continuous reading
            while True:
                data = await reader.read(1024)  # Read 1024 bytes
                if data:
                    print("Received: ", data.strip())
                    self.received_data = data.strip()  # Set the received data
                
                await asyncio.sleep(0.1)
        except Exception as e:
            print("Error: ", e)
        finally:
            print("Closing connection")
            writer.close()
            await writer.wait_closed()


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
