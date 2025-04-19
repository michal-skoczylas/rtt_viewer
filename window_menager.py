import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QUrl, QObject, Signal, Property, Slot

class WindowManager(QObject):
    def __init__(self):
        super().__init__()
        self._current_window = "selection"

    # Sygnał zmiany okna
    windowChanged = Signal(str)
    
    @Property(str, notify=windowChanged)
    def currentWindow(self):
        return self._current_window
    
    @currentWindow.setter
    def currentWindow(self, value):
        if self._current_window != value:
            self._current_window = value
            self.windowChanged.emit(value)

    # Metoda wywoływana po wyborze płytki
    @Slot(str)
    def boardSelected(self, board_name):
        print(f"Wybrano płytkę: {board_name}")
        self.currentWindow = "main"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Menadżer okien
    manager = WindowManager()
    
    # Główne okno QML
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    
    # Rejestracja obiektu Python w QML
    view.rootContext().setContextProperty("windowManager", manager)
    view.setSource(QUrl.fromLocalFile("board_selector.qml"))
    
    view.setTitle("STM Board Selector")
    view.show()
    sys.exit(app.exec_())