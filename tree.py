class Tree:
    def __init__(self):
        self.tree = {}

    def add_path(self, path):
        """
        Dodaje ścieżkę do drzewa.
        :param path: Ścieżka w formacie "folder1/folder2/file"
        """
        print(f"Przetwarzana ścieżka: '{path}'")  # Debugowanie
        parts = path.split("/")
        if parts[0] != "root":
            raise ValueError("Ścieżka musi zaczynać się od 'root'")
        
        current_level = self.tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}  # Tworzy nowy podfolder, jeśli nie istnieje
            current_level = current_level[part]

    def get_top_level_folders(self):
        """
        Zwraca listę folderów na najwyższym poziomie drzewa.
        :return: Lista folderów (kluczy) na najwyższym poziomie.
        """
        root = self.tree.get("root",{})
        return list(root.keys())

    def get_folder_contents(self, folder_name):
        """
        Zwraca zawartość (podfoldery i pliki) danego folderu.
        :param folder_name: Nazwa folderu, którego zawartość chcemy uzyskać.
        :return: Lista podfolderów i plików w danym folderze.
        """
        root = self.tree.get("root",{})
        folder = root.get(folder_name, {})
        return list(folder.keys())

    def print_tree(self, current_level=None, indent=0):
        """
        Wypisuje całe drzewo w formie hierarchicznej.
        :param current_level: Aktualny poziom drzewa (domyślnie korzeń).
        :param indent: Liczba wcięć dla hierarchii.
        """
        if current_level is None:
            current_level = self.tree

        for key, value in current_level.items():
            print(" " * indent + key)
            if isinstance(value, dict):
                self.print_tree(value, indent + 2)