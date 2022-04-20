"""
Compares messages between one another according to different NLP algorithms.
Wordnet_Sentence_Similarity uses Wordnet
"""
import numpy as np
from nltk import word_tokenize, pos_tag, PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


porterstemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))


def preprocess(string):
    """
    This preprocessor function converts all strings to lower case and stems them with
    nltk's porter stemmer.
    :param string: string passed to function by sklearn TF-IDF Vectorizer
    :return: None if a stop word, processed string if not
    """
    string = string.lower()
    string = porterstemmer.stem(string)
    if string in stop_words:
        return None
    else:
        return string


class TF_IDF:
    """
    Term frequency-Inverse Document Frequency class for comparing two texts based on a corpus of documents.
    Currently not in use in favor of Levenshtein distance.
    """
    def __init__(self):
        """
        Initialization for TF_IDF class.
        """
        self.docs_tfidf = None
        self.all_documents = []
        self.vectorizer = TfidfVectorizer(preprocessor=preprocess)

    def new_incoming_tweet(self, new_tweet_text: str):
        """
        Update the tfidf vectorizor to include all the documents and the new one.
        :param new_tweet_text: str
        :return: tuple (str, float) of the closest related text and the cosine similarity score
        """
        if len(self.all_documents) == 0:
            self.all_documents.append(new_tweet_text)
            self.docs_tfidf = self.vectorizer.fit_transform(self.all_documents)
            return 0.0
        else:
            query_tfidf = self.vectorizer.transform([new_tweet_text])
            cosine_simiilarities = cosine_similarity(query_tfidf, self.docs_tfidf).flatten()
            self.all_documents.append(new_tweet_text)
            self.docs_tfidf = self.vectorizer.fit_transform(self.all_documents)
            result = dict(list(zip(self.all_documents[:-1], list(cosine_simiilarities))))
            return max(result, key=result.get), max(result.values())

    def most_similar_doc(self, new_tweet_text: str):
        """
        Gets the most similar document to the input text
        :param new_tweet_text: str
        :return: str
        """
        if len(self.all_documents) == 0:
            self.all_documents.append(new_tweet_text)
            self.docs_tfidf = self.vectorizer.fit_transform(self.all_documents)
            return None
        else:
            self.all_documents.append(new_tweet_text)
            tfidf = self.vectorizer.fit_transform(self.all_documents)
            pairwise_similarity = tfidf * tfidf.T
            arr = pairwise_similarity.toarray()
            np.fill_diagonal(arr, np.nan)
            input_idx = self.all_documents.index(new_tweet_text)
            result_idx = np.nanargmax(arr[input_idx])
            return self.all_documents[result_idx]


class WordnetSentenceSimilarity:
    """
    This class constructs a value for one sentence's similarity to another's.
    First construct the class and then call [object].symmetric_sentence_similarity()
    """

    def __init__(self, sent1: str, sent2: str):
        self.sentence1 = sent1
        self.sentence2 = sent2

    @staticmethod
    def penn_to_wn(tag: str):
        """
        Converts a Penn Treebank Part of Speech tag, which is used as the default in NLTK's POS tagger
        :param tag: str
        :return: Returns a simplified POS tag.
        """
        if tag.startswith('N'):
            return 'n'
        if tag.startswith('V'):
            return 'v'
        if tag.startswith('J'):
            return 'a'
        if tag.startswith('R'):
            return 'r'
        return None

    def tagged_to_synset(self, word: str, tag: str):
        """
        Takes a word and its tagged part of speech and returns it
        as a Wordnet synset object.
        :param word: str. The tokenized word in the sentence.
        :param tag: str. The tagged part of speech.
        :return: None || str. returns either None if there is no part of speech tag, or
        the most common part of speech for the synset.
        """
        wn_tag = self.penn_to_wn(tag)
        if wn_tag is None:
            return None
        try:
            return wn.synsets(word, wn_tag)[0]
        except:
            return None

    def sentence_similarity(self, sentence1: str, sentence2: str):
        """
        This function will compute the similarity of a sentence according to Wordnet's
        path similarity (distance from sense). It computes an average of the sentence's
        word's distance from the other sentence's words.
        :param sentence1: str
        :param sentence2: str
        :return: float
        """
        # Tokenizes and tags the sentence.
        sentence1 = pos_tag(word_tokenize(sentence1))
        sentence2 = pos_tag(word_tokenize(sentence2))

        # Builds a list of of synsets by simplifying the part of speech tag and selecting the most
        # common sense of the synset, incorporates all synsets into a list.
        synsets1 = [self.tagged_to_synset(*tagged_word) for tagged_word in sentence1]
        synsets2 = [self.tagged_to_synset(*tagged_word) for tagged_word in sentence2]

        # Filter out the Nones
        synsets1 = [ss for ss in synsets1 if ss is not None]
        synsets2 = [ss for ss in synsets2 if ss is not None]

        # Initializes the score
        score, count = 0.0, 0

        # For each word in the first sentence
        for synset in synsets1:
            # Get the similarity value of the most similar word in the other sentence
            simlist = [synset.path_similarity(ss) for ss in synsets2 if synset.path_similarity(ss)]
            if not simlist:
                continue
            best_score = max(simlist)

            # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
                count += 1

        # Average the values
        score /= count
        return score

    # @clock
    def symmetric_sentence_similarity(self):
        """
        This function will compute the average of sentence_similarity since,
        since sentence_similarity(s1, s2) doesn't always equal sentence_similarity(s2, s1).
        This is a little bit hacky
        :return: float
        """
        return (self.sentence_similarity(self.sentence1, self.sentence2) +
                self.sentence_similarity(self.sentence2, self.sentence1)) / 2


class WordNetTweetSimilarityScore:
    """
    WordNetTweetSimilarityScore class for getting the text with the highest similarity score and the corresponding
    Princeton word net similarity score.
    """
    def __init__(self, logged_tweets: list):
        """
        Initialization for WordNetTweetSimilarityScore
        :param logged_tweets: list
        """
        self.all_documents = logged_tweets

    def new_incoming_tweet(self, new_tweet: str):
        """
        Takes an incoming tweet and gets the  text with the highest similarity score and the corresponding Princeton
        word net similarity score.
        :param new_tweet: str
        :return: tuple of (str, float)
        """
        tweet_similarity_score_dict = {}
        for tweet in self.all_documents:
            fs_to_s = WordnetSentenceSimilarity(new_tweet, tweet)
            result = fs_to_s.symmetric_sentence_similarity()
            tweet_similarity_score_dict[tweet] = result
        return max(tweet_similarity_score_dict, key=tweet_similarity_score_dict.get), \
               max(tweet_similarity_score_dict.values())


if __name__ == '__main__':
    print("Testing similarity scores for sentences:")
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

    focus_sentence = "Hello every one I love music so much."

    tweets = WordNetTweetSimilarityScore(sentences)
    print(tweets.new_incoming_tweet(focus_sentence))

    tf_idf = TF_IDF()
    for sentence in sentences:
        print(tf_idf.new_incoming_tweet(new_tweet_text=sentence))

    for sentence in sentences:
        print(tf_idf.most_similar_doc(new_tweet_text=sentence))
