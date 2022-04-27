import random
from node import Node
from NLP_Tools.message_comparison_toolset import TF_IDF
from NLP_Tools.message_comparison_toolset import WordNetTweetSimilarityScore


class Tree:
    """
    Tree class for storing nodes. Useful for future development with more concrete object comparison when conducting
    sound synthesis on related incoming texts.
    """
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

    def add_node(self, node: Node):
        """
        Adds a node to the tree. The root's key is None, so if there are no extant nodes, the first
        incoming message is appended to the root.
        :param node: Node class
        """
        if len(self.nodes) == 1:
            self.root.add_child(node)
            self.set_node_instrument_chain(node, 0)
            self.nodes[node.message] = node
        else:
            if self.nodes.get(node.message):
                # Some memoization to speed up algorithm
                key, similarity = node.message, 1.0
                node = self.nodes.get(node.message)
            else:
                # get closest message by similarity
                key, similarity = self.find_closest_node(node)
                self.nodes[node.message] = node
                node.num_ancestors = self.nodes[key].num_ancestors + 1
                self.nodes[key].add_child(node)
                self.set_node_instrument_chain(node, similarity)
            print(node, similarity)

    def remove_node(self, node: Node):
        """
        Some functionality to remove a node.
        :param node: Node class.
        """
        del(self.nodes[node.message])
        for child_node in node.children:
            node.parent.add_child(child_node)
        node.parent.remove_child(node)

    def remove_node_by_message(self, message: str):
        """
        Removes a node by the input message.
        :param message: str
        :return: None
        """
        node = self.nodes[message]
        self.remove_node(node)

    def find_closest_node(self, node: Node):
        """
        Finds the closest node via the text comparison object. Returns the most similar Node
        as a key for memoization.
        :param node: Node Class
        """
        most_similar = self.message_comparison_obj.new_incoming_document(node.message)
        if most_similar[1] == 0.0:
            return None, 0.0
        else:
            return most_similar

    def receive_message(self, message: str):
        """
        Receives messages as a string and generates nodes to add to the tree.
        :param message: String from a tweet.
        """
        new_node = Node(message)
        self.add_node(new_node)
        return new_node

    def set_node_instrument_chain(self, node: Node, similarity_score: float):
        if similarity_score >= 0.9:
            node.instruments = node.parent.instruments
        else:
            if node.parent is None:
                node.instruments = [random.randint(0, 16)]
            else:
                node.instruments = node.parent.instruments[-4:] + [random.randint(0, 15)]

    def get_node_instrument_chain(self, node, num_instruments=None):
        if num_instruments is None:
            num_instruments = len(node.instruments)
        return node.instruments[:num_instruments]

if __name__ == '__main__':
    sentences = [
        "politics I",
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
        "cat, cats and jesus have a spectral music that sounds like jazz boob",
        "politics is power",
        "I love dogs",
        "Ruth is my baby",
        "I am sitting in a room",
        "I hate dog",
        "i hate dogs",
        "I have a dog",
        'no to dog',
        "I had a dog",
        "I was a doggo",
        "I had a dogg",
        "nary another had any old damn hound",
        "I had a dog"
    ]

    tf_idf = TF_IDF()
    # word_net = WordNetTweetSimilarityScore([])
    tf_idf_tree = Tree(tf_idf)
    # wordnet_tree = Tree(word_net)
    for doc in sentences:
        # print(doc)
        tf_idf_tree.receive_message(doc)

        # wordnet_tree.receive_message(doc)
    # print(tf_idf_tree.nodes["Music is sound in ti"].parent.parent.message)
    # print(tf_idf_tree.nodes)
