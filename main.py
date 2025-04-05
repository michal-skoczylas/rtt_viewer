# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import telnetlib3
import time
import asyncio
import qasync
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property, Signal, QAbstractItemModel, QModelIndex
from PySide6.QtWidgets import QFileDialog
import pyudev
import rtt_handler
import tree


if __name__ == "__main__":


    app = QGuiApplication(sys.argv)

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    context_object = QObject()
    rtt_handler = rtt_handler.RTTHandler()
    engine.rootContext().setContextProperty("rttHandler",rtt_handler)

    if not engine.rootObjects():
        sys.exit(-1)

    with loop:
        loop.run_forever()
    sys.exit(app.exec())
