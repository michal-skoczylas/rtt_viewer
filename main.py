# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import asyncio
import qasync
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

# Import with alias to avoid name conflict
from rtt_handler import RTTHandler
from file_handler import FileHandler

async def main():
    # Use QApplication instead of QGuiApplication for better compatibility
    app = QApplication(sys.argv)

    # Set up async loop
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    engine = QQmlApplicationEngine()

    # Create and register handler
    rtt_handler = RTTHandler()
    file_handler = FileHandler()

    # Create instances in QML
    engine.rootContext().setContextProperty("rttHandler", rtt_handler)
    engine.rootContext().setContextProperty("fileHandler", file_handler)

    # Load QML
    qml_file = Path(__file__).resolve().parent / "main.qml"
    print(f"Loading QML from: {qml_file}")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)


    # Start application
    with loop:
        sys.exit(app.exec())

if __name__ == "__main__":
    asyncio.run(main())