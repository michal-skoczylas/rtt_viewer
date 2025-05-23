class Tree:
    def __init__(self):
        self.tree = {}

    def add_path(self, path):
            """
            Dodaje ścieżkę do drzewa.
            :param path: Ścieżka w formacie "/folder1/folder2/nazwa_pliku/rozmiar"
            """
            print(f"Przetwarzana ścieżka: '{path}'")
            parts = path.strip("/").split("/")
            if len(parts) < 2:
                raise ValueError("Ścieżka musi zawierać co najmniej plik i rozmiar")

            *folders, file_name, size_str = parts
            try:
                size = int(size_str)
            except ValueError:
                raise ValueError(f"Nieprawidłowy rozmiar pliku: {size_str}")

            current_level = self.tree
            for folder in folders:
                if folder not in current_level or not isinstance(current_level[folder], dict):
                    current_level[folder] = {}
                current_level = current_level[folder]
            current_level[file_name] = size  # Plik jako klucz, rozmiar jako wartość

    def get_top_level_folders(self):
        """
        Zwraca listę folderów na najwyższym poziomie drzewa.
        :return: Lista folderów (kluczy) na najwyższym poziomie.
        """
        return list(self.tree.keys())

    def get_folder_contents(self, folder_name):
        """
        Zwraca zawartość (podfoldery i pliki) danego folderu.
        :param folder_name: Nazwa folderu, którego zawartość chcemy uzyskać.
        :return: Lista podfolderów i plików w danym folderze.
        """
        folder = self.tree.get(folder_name, {})
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
