class Node:
    def __init__(self, message, parent=None, children=None, num_ancestors=0, instruments=[]):
        """
        Node class that holds messages and links itself to parents/children
        :type parent: Node
        :param message: String from a tweet.
        :param parent: A parent node.
        :param children: A child node.
        """
        self.message = message
        self.parent = parent
        self.num_ancestors = num_ancestors
        self.instruments = []
        if children is None:
            self.children = []
        else:
            self.children = [].append(children)

    def __str__(self):
        return "Message: {} || Number of Ancestors: {} || Instrument Chain: {}".format(
            self.message, self.num_ancestors, self.instruments
        )

    def __repr__(self):
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())

    def set_parent(self, node):
        """
        Sets a node to be the parent and adds self to parent's children.
        :param node: Parent node.
        """
        self.parent = node
        node.add_child(self)

    def add_child(self, node):
        """
        Adds a child to this node's children.
        :param node: Child node.
        """
        self.children.append(node)
        node.parent = self

    def remove_child(self, node):
        """
        Removes a child node from children and sets child node parent to None.
        :param node: Child node.
        """
        node.parent = None
        self.children.remove(node)
