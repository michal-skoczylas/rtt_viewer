# tree.py

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"Node({self.value})"

class Tree:
    def __init__(self, root_value):
        self.root = Node(root_value)

    def add_node(self, parent_value, value):
        parent_node = self._find_node(self.root, parent_value)
        if parent_node:
            new_node = Node(value)
            parent_node.add_child(new_node)

    def _find_node(self, node, value):
        if node.value == value:
            return node
        for child in node.children:
            found = self._find_node(child, value)
            if found:
                return found
        return None

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print(" " * level * 2 + str(node.value))
        for child in node.children:
            self.print_tree(child, level + 1)

    @staticmethod
    def from_string(path_string):
        tree = Tree("root")  # Korzeń drzewa to "root"
        lines = path_string.strip().split("\n")  # Rozdzielamy tekst na linie
        
        for line in lines:
            parts = line.split("/")  # Dzielimy ścieżki na części
            current_path = "root"
            
            for part in parts[1:]:  # Pomijamy "root", zaczynamy od ścieżki
                tree.add_node(current_path, part)  # Dodajemy węzeł dla każdej części
                current_path = part  # Aktualizujemy bieżący węzeł

        return tree
