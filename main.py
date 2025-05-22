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

        #Loading windows
        self.board_selector_window = None
        self.main_window = None
        #load board selector
        qml_file_selector = Path(__file__).resolve().parent /"board_selector.qml"
        self.engine.load(QUrl.fromLocalFile(str(qml_file_selector)))
        if not self.engine.rootObjects():
            sys.exit(-1)
        self.board_selector_window = self.engine.rootObjects()[0]
        #load main window without showing it
        qml_file_main = Path(__file__).resolve().parent /"main.qml"
        self.engine.load(QUrl.fromLocalFile(str(qml_file_main)))
        if len(self.engine.rootObjects())<2:
            print("Error loading main window") 
            sys.exit(-1)
        self.main_window = self.engine.rootObjects()[1]
        self.main_window.hide()

        #connect signals
        self.board_handler.boardSelected.connect(self.on_board_selected)

        
    
    def start(self):
        """Start app by showing board selector window"""
        self.show_board_selector()
        with self.loop:
            sys.exit(self.app.exec())
    
    def show_board_selector(self):
        self.board_selector_window.show()

    def show_main_window(self):
        self.main_window.show()

    def on_board_selected(self,board_name):
        """Handle board selection and switch to the main window"""
        print(f"Board selected: {board_name}")
        self.board_selector_window.hide()
        self.show_main_window()
async def main():
    manager = ApplicationManager()
    manager.start()
        

        
if __name__ == "__main__":
    asyncio.run(main())