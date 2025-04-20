from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot

class WindowManager(QObject):
    def __init__(self):
        super().__init__()
        self.engines = []  # Przechowujemy silniki aby okna nie były zamykane
    
    @Slot()
    def load_main_screen(self):
        engine = QQmlApplicationEngine()
        engine.load("main.qml")
        self.engines.append(engine)  # Przechowujemy referencję

# app = QApplication([])

# manager = WindowManager()

# # Pierwsze okno
# first_engine = QQmlApplicationEngine()
# first_engine.rootContext().setContextProperty("windowManager", manager)
# first_engine.load("board_selector.qml")

# app.exec()