from PySide6.QtCore import QObject, Signal

class BoardHandler(QObject):
    boardSelected = Signal(str)

    def __init__(self, ):
        super().__init__()
    
    def select_board(self,board_name):
        """Emit selected board name"""
        print(f"Selected board:{board_name}")
        self.boardSelected.emit(board_name)