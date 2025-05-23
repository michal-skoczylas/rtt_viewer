# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import asyncio
import qasync
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

from rtt_handler import RTTHandler
from file_handler import FileHandler
from board_handler import BoardHandler
from app_manager import ApplicationManager

async def main():
    manager = ApplicationManager()
    manager.start()
        

        
if __name__ == "__main__":
    asyncio.run(main())