import nltk
import cmudict
from pronouncing import *
from string import punctuation
from functools import lru_cache
from nltk.corpus import stopwords
from itertools import product as iterprod


no_punct = lambda x: re.sub(r'[^\w\s]', '', x)

vowels = "aeiouyAEIOUY"
stop_words = set(stopwords.words('english'))
caesura_sym = ",.;:-!?"
cmudict_entries = None


def get_cmudict_entries():
    """
    Instantiates a global variable cmudict_entries using Singleton pattern. Advantage is that cmudict.dict() need
    only be called once, when first needed.
    :return: a list of tuples containing (word, transcriptions) from cmudict.dict()
    """
    global cmudict_entries
    if cmudict_entries is None:
        cmudict_entries = cmudict.dict()
    return cmudict_entries


def last_word(line):
    """
    Obtains the last word from a string.
    :param line: a line of string text
    :return: the last word in a line
    """
    line.strip()  # removes any whitespace
    if len(line) != 0:  # Ignores empty lines
        return [word for word in tokenize_line_no_punk(line)][-1]
    return ""


def word_freq(poem):
    """
    Creates a dictionary of word keys and their respective frequency values. Removes punctuation and ignores
    stopwords in order to only track obviously 'important' words. Intended for possible Repetition algorithm.
    :param poem: the full text submitted by the user
    :return: a dictionary object of word:freq pairs
    """
    word_dict = dict()
    clean_poem = [word.lower() for word in tokenize_line_no_punk(poem)]
    for word in clean_poem:
        if word in word_dict or word in stop_words:
            continue
        word_dict[word] = clean_poem.count(word)
    return word_dict


def tokenize_line_no_punk(line):
    """
    Splits a line into words, while removing any trailing punctuation marks.
    :param line: a string line from a poem
    :return: a list of words which comprise the input line
    """
    stripped_line = [word.strip(punctuation) for word in line.split()]  # strips punctuation from words
    return [x for x in stripped_line if x]  # removes empty strings left by standalone punctuation


def tokenize_stanzas(text):
    """
    Splits a poem into a list of stanzas by splitting on \n\n (new paragraph).
    :param text: a poem or text
    :return: a list of the text's stanzas
    """
    stanza_list = text.split("\n\n")
    return stanza_list


def compile_alliterative_part(word):
    """
    Manually compiles rudimentary 'alliterative part' of a parsed word when that word cannot be found in cmudict.
    This works by obtaining the first non-vowel characters of a word if it doesn't start with a vowel or simply
    returns the first letter.
    :param word: the word to be parsed
    :return: a string containing the 'alliterative part' of the word
    """
    chars = list(word)  # splits word in chars
    counter = 1  # tracks for first char
    first_phone = ""  # the phoneme to return
    while True:
        if chars[0] not in vowels:  # checks char is not a vowel
            first_phone += chars.pop(0)
        else:
            if counter == 1:  # only append the vowel if its the first char, otherwise alliterative part ends
                first_phone += chars.pop(0)
            break
        counter += 1
    return first_phone.upper()


def alliterative_part(word):
    """
    Obtains the 'alliterative part' of a word by using the cmudict. If the word is not in the cmudict then the
    alliterative part is compiled using compile_alliterative_part() method.
    :param word: the word to be parsed
    :return: a string containing the alliterative part of the word
    """
    s = word.lower()
    if s in get_cmudict_entries():
        first_phone = get_cmudict_entries()[s][0][0]  # Obtains first phone from first pronunciation
        return first_phone
    else:
        return s[0].upper()


def is_sibilant(word):
    """
    Checks if a word is sibilant (contains 'S' phoneme).
    :param word: the word to be checked
    :return: a boolean result
    """
    prons = phones_for_word(word)
    if len(prons) > 0:
        pron = prons[0].split()
        if "S" in pron:
            return True
        else:
            return False
    return False


@lru_cache()
def pronounce(word):
    """
    Manually generates a pronunciation for a given word, based on phonemes in cmudict.
    This is done by splitting words (generally down the middle and recursing outwards) into prefix and suffix and
    searching for any known pronunciations.
    :param word: a string word
    :return: a list of pronunciations compiled for the word parameter
    """
    s = word.lower()  # lowercases word for cmu_dict
    if s in get_cmudict_entries():
        return get_cmudict_entries()[s]  # obtains the pronunciation in the dictionary
    m = len(s) / 2  # gets the word midpoint
    partition = sorted(list(range(len(s))), key=lambda x: (x - m) ** 2 - x)  # orders char indices from middle outwards
    for i in partition:
        pre, suf = (s[:i], s[i:])  # creates a prefix/suffix pair
        if pre in get_cmudict_entries() and pronounce(suf) is not None:  # recurses through suffix part to get phones
            return [x + y for x, y in iterprod(get_cmudict_entries()[pre], pronounce(suf))]
    return None


def f_pronounce(word):
    """
    Obtains the conventional first pronunciation as a string from the list of pronunciations generated by pronounce()
    :param word: the word to parse
    :return: a string pronunciation
    """
    return ' '.join(pronounce(word)[0])
