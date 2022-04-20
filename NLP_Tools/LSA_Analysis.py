import os.path
from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.coherencemodel import CoherenceModel


# Note, currently placeholder code for future reference when using LSA space to map text similarity based on
# the texts submitted over several concerts. Not currently in use.

def load_data(path: str, file_name: str):
    """
    This loads the text file
    :param path: str
    :param file_name: str
    :return: list of paragraphs/documents and title(initial 100 words considered as title of document
    """
    documents_list = []
    titles = []
    with open(os.path.join(path, file_name), "r") as fin:
        for line in fin.readlines():
            text = line.strip()
            documents_list.append(text)
    print("Total Number of Documents:", len(documents_list))
    titles.append(text[0:min(len(text), 100)])
    return documents_list, titles


def preprocess_data(documents_list: list):
    """
    This function runs all the documents through a regexp tokenizer,
    removes stop words, and stems the leftover words
    :documents_list: list
    :return: preprocessed texts from the document list
    """
    tokenizer = RegexpTokenizer(r'\w+')
    english_stop_words = set(stopwords.words('english'))
    porter_stemmer = PorterStemmer()
    texts = []
    for document in documents_list:
        raw = document.lower()
        tokens = tokenizer.tokenize(raw)
        stopped_tokens = [token for token in tokens if not token in english_stop_words]
        stemmed_tokens = [porter_stemmer.stem(i) for i in stopped_tokens]
        texts.append(stemmed_tokens)
    return texts


def prepare_corpus(cleaned_documents: list):
    """
    Create term dictionary of our corpus and
    Converting list of documents (corpus) into Document Term Matrix
    :param cleaned_documents: list
    :return: tuple of term dictionary and Document Term Matrix
    """
    dictionary = corpora.Dictionary(cleaned_documents)
    document_term_matrix = [dictionary.doc2bow(doc) for doc in cleaned_documents]
    return dictionary, document_term_matrix


def create_gensim_lsa_model(cleaned_documents: list, number_of_topics: int, words: int):
    """
    Create LSA model through gensim
    :param cleaned_documents: list of cleaned documents
    :param number_of_topics: int of number of topics
    :param words: int number of words associated with each topic
    :return: return LSA model
    """
    dictionary, doc_term_matrix = prepare_corpus(cleaned_documents)
    lsamodel = LdaModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)
    print(lsamodel.print_topics(num_topics=number_of_topics, num_words=words))
    return lsamodel


def compute_coherence_values(dictionary, doc_term_matrix, cleaned_documents,
                             stop, start=2, step=3):
    """
    Computes the coherence values for various number of topics
    :param dictionary: Gensim Dictionary
    :param doc_term_matrix: Gensim Corpus
    :param cleaned_documents: List of input texts
    :param stop: Maximum number of topics
    :return: List of LSA topic models and the coherence values corresponding
    to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, stop, step):
        lda_model = LdaModel(doc_term_matrix, num_topics=num_topics, id2word=dictionary)
        model_list.append(lda_model)
        coherence_model = CoherenceModel(model=lda_model, texts=cleaned_documents, dictionary=dictionary,
                                         coherence='c_v')
        coherence_values.append(coherence_model.get_coherence())
    return model_list, coherence_values


if __name__ == '__main__':
    path = "/Users/ericlemmon/Desktop/"
    filename = 'articles+4.txt'
    number_of_topics = 7
    words = 10
    document_list, titles = load_data(path, filename)
    clean_text = preprocess_data(document_list)
    model = create_gensim_lsa_model(clean_text, number_of_topics, words)
