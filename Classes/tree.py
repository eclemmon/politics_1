from node import Node
from NLP_Tools.message_comparison_toolset import TF_IDF
from NLP_Tools.message_comparison_toolset import WordNetTweetSimilarityScore

class Tree:
    def __init__(self, message_comparison_obj):
        self.nodes = {}
        self.root = Node(None, None, None)
        self.nodes[None] = self.root
        self.message_comparison_obj = message_comparison_obj

    def add_node(self, node):
        if len(self.nodes) == 1:
            self.root.add_child(node)
            self.nodes[node.message] = node

    def remove_node(self, node):
        for child_node in node.children:
            node.parent.add_child(child_node)
        node.parent.remove_child(node)

    def find_closest_node(self, node):
        pass