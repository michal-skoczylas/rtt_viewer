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


class FileHandler(QObject):
    def __init__(self):
        file_path = ""

    @Slot()
    def select_save_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            None, "Save rtt data", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            print(f"Selected save path: {file_path}")
            self.save_rtt_data_to_file(file_path)

        def save_rtt_data_to_file(self, filepath):
            try:
                with open(filepath, "w") as file:
                    file.write("\n".join(self._last_command_data))
                print(f"data saved to: {filepath}")
            except Exception as e:
                print(f"Error saving file: {e}")
