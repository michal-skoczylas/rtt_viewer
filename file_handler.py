from PySide6.QtCore import QObject, Slot,Signal
from PySide6.QtWidgets import QFileDialog

class FileHandler(QObject):
    savePathSelected = Signal(str)
    def __init__(self):
        super().__init__()
        self._save_path = ""

    @Slot(result=str)
    def select_save_path(self):
        """
        Otwiera okno dialogowe do wyboru miejsca zapisu pliku.
        :return: Ścieżka wybranego pliku.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            None, "Select Save Path", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self._save_path = file_path
            print(f"Selected save path: {file_path}")
            self.savePathSelected.emit(file_path)
        else:
            print("No path selected")
        return self._save_path

    @Slot(str, str)
    def save_to_file(self, file_path, data):
        """
        Zapisuje dane do pliku.
        :param file_path: Ścieżka do pliku.
        :param data: Dane do zapisania.
        """
        try:
            with open(file_path, "w") as file:
                file.write(data)
            print(f"Data saved to: {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")