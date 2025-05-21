# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import asyncio
import qasync
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

# Import with alias to avoid name conflict
from rtt_handler import RTTHandler
from file_handler import FileHandler
from board_handler import BoardHandler
# async def main():
#     # Use QApplication instead of QGuiApplication for better compatibility
#     app = QApplication(sys.argv)

#     # Set up async loop
#     loop = qasync.QEventLoop(app)
#     asyncio.set_event_loop(loop)

#     engine = QQmlApplicationEngine()

#     # Create and register handler
#     rtt_handler = RTTHandler()
#     file_handler = FileHandler()
#     board_handler = BoardHandler()


#     # Create instances in QML
#     engine.rootContext().setContextProperty("rttHandler", rtt_handler)
#     engine.rootContext().setContextProperty("fileHandler", file_handler)
#     engine.rootContext().setContextProperty("boardHandler",board_handler)

#     # Load QML
#     qml_file = Path(__file__).resolve().parent / "main.qml"
#     print(f"Loading QML from: {qml_file}")
#     engine.load(qml_file)

#     if not engine.rootObjects():
#         sys.exit(-1)


#     # Start application
#     with loop:
#         sys.exit(app.exec())

class ApplicationManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loop = qasync.QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        

        #Handlers
        self.rtt_handler = RTTHandler()
        self.file_handler = FileHandler()
        self.board_handler = BoardHandler()
        #QML Engine
        self.engine = QQmlApplicationEngine()
        #Register handlers in qml
        self.engine.rootContext().setContextProperty("rttHandler", self.rtt_handler)
        self.engine.rootContext().setContextProperty("fileHandler", self.file_handler)
        self.engine.rootContext().setContextProperty("boardHandler",self.board_handler)
        
        #handle board selection
        self.board_handler.boardSelected.connect(self.on_board_selected)
    
    def start(self):
        """Start app by showing board selector window"""
        self.show_board_selector()
        with self.loop:
            sys.exit(self.app.exec())
    
    def show_board_selector(self):
        """Show board selector window"""
        qml_file = Path(__file__).resolve().parent /"board_selector.qml"
        print(f"Loading board selector QML from: {qml_file}")
        self.engine.load(QUrl.fromLocalFile(str(qml_file)))

        if not self.engine.rootObjects():
            sys.exit(-1)
        self.board_selector_window = self.engine.rootObjects()[0]
        self.board_selector_window.show()

    def show_main_window(self):
        """Show main window"""
        qml_file = Path(__file__).resolve().parent /"main.qml"
        print(f"Loading board selector QML from: {qml_file}")
        self.engine.load(QUrl.fromLocalFile(str(qml_file)))
        if not self.engine.rootObjects():
            sys.exit(-1)
        
        self.main_window= self.engine.rootObjects()[0]
        self.main_window.show()
        self.main_window.raise_()
    def on_board_selected(self,board_name):
        """Handle board selection and switch to the main window"""
        print(f"Board selected: {board_name}")
        self.board_selector_window.close()
        self.show_main_window()
async def main():
    manager = ApplicationManager()
    manager.start()
        

        
if __name__ == "__main__":
    asyncio.run(main())