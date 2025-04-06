import tree



tree = tree.Tree("root")
message = "/dir1/file1\n/dir1/file2\n/dir2/file1\n/dir2/file2\n"
tree = tree.from_string(message) 
tree.print_tree()
