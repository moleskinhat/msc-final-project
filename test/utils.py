import random


def generate_model(cfdist, word, num=10):
    """
    A random 10-word line generator for use in testing of algorithms on long texts. Takes a random word from
    the Brown Corpus and uses bigrams and Conditional Frequency Distribution to continously generate random words.
    :param cfdist: The Conditional Frequency Distribution list - a list of most likely words to follow the input word,
    here based on Brown Corpus
    :param word: the starting word of the line - here taken at random from Brown Corpus
    :param num: the number of words per line (includes punctuation)
    :return: a 10-word line string of randomly generated words
    """
    s = ""
    for i in range(num):
        s += word + ' '
        word = random.choice(list(cfdist[word]))
    return s + "\n"
