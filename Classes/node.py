class Node:
    def __init__(self, message, parent=None, children=None):
        self.message = message
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = [].append(children)

    def set_parent(self, node):
        self.parent = node
        node.add_child(self)

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def remove_child(self, node):
        self.children.remove(node)
