import tree

if __name__ == "__main__":
    sample_data = """
    root/A
    root/A/A1
    root/A/A2
    root/B
    root/B/B1
    root/B/B2
    root/C
    """

    # Tworzenie drzewa
    file_tree = tree.Tree()
    for line in sample_data.strip().split("\n"):
        line = line.strip()  # Usuń dodatkowe białe znaki
        file_tree.add_path(line)

    # Wypisanie drzewa
    print("Drzewo plików:")
    file_tree.print_tree()

    # Pobranie folderów nadrzędnych
    top_level_folders = file_tree.get_top_level_folders()
    print("\nFoldery nadrzędne:", top_level_folders)
