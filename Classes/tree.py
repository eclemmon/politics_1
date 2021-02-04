from node import Node
from NLP_Tools.message_comparison_toolset import TF_IDF
from NLP_Tools.message_comparison_toolset import WordNetTweetSimilarityScore


class Tree:
    def __init__(self, message_comparison_obj):
        """
        A tree class that holds messages as nodes that can be traversed and catalogued
        for the purposes of showing the relationship between tweets.
        :param message_comparison_obj: A message comparison class that performs comparisons
        to find the closest related tweet so it can be attached to that node as a child.
        """
        self.nodes = {}
        self.root = Node(None, None, None)
        self.nodes[None] = self.root
        self.message_comparison_obj = message_comparison_obj

    def add_node(self, node):
        """
        Adds a node to the tree. The root's key is None, so if there are no extant nodes, the first
        incoming message is appended to the root.
        :param node: Node class
        """
        if len(self.nodes) == 1:
            self.root.add_child(node)
            self.nodes[node.message] = node
        else:
            key = self.find_closest_node(node)
            self.nodes[node.message] = node
            self.nodes[key].add_child(node)

    def remove_node(self, node):
        """
        Some functionality to remove a node.
        :param node: Node class.
        """
        del (self.nodes[node.message])
        for child_node in node.children:
            node.parent.add_child(child_node)
        node.parent.remove_child(node)

    def find_closest_node(self, node):
        """
        Finds the closest node via the text comparison object. Returns the most similar
        as a key for memoization.
        :param node: Node Class
        """
        most_similar = self.message_comparison_obj.most_similar_doc(node.message)
        if most_similar == 0.0:
            return None
        else:
            return most_similar

    def receive_message(self, message):
        """
        Receives messages as a string and generates nodes to add to the tree.
        :param message: String from a tweet.
        """
        new_node = Node(message)
        self.add_node(new_node)


if __name__ == '__main__':
    sentences = [
        "Some jazz musicians are excellent at the trombone.",
        "I played the viola for the wedding.",
        "Cats are jamming on a hurdy gurdy!",
        "Jesus ascended to heaven with blaring trumpets from angels' butts.",
        "Cats are beautiful animals.",
        "Kaija Saariaho writes spectral music",
        "Beep, boop, doowop.",
        "beep, bep, soowop.",
        "Music is sound in time",
        "Music is sound in ti",
        "cat, cats and jesus have a spectral music that sounds like jazz boob"
    ]

    tf_idf = TF_IDF()
    # word_net = WordNetTweetSimilarityScore([])
    tf_idf_tree = Tree(tf_idf)
    # wordnet_tree = Tree(word_net)
    for doc in sentences:
        # print(doc)
        tf_idf_tree.receive_message(doc)

        # wordnet_tree.receive_message(doc)
    print(tf_idf_tree.nodes["Music is sound in ti"].parent.parent.parent.message)
