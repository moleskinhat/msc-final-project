import nltk
import cmudict
from pronouncing import *
from string import punctuation
from nltk.corpus import stopwords
from poetry_analyser.Utils import *
from nltk import word_tokenize, sent_tokenize, line_tokenize


vowels = "aeiouyAEIOUY"
stop_words = set(stopwords.words('english'))
caesura_sym = ",.;:-!?"
cmudict_entries = None

# Lambda function for removing punctuation from words
no_punct = lambda x: re.sub(r'[^\w\s]', '', x)


class Model:
    poem = ""  # Stores the input poem

    def __init__(self):
        pass

    def poem_injection(self, poem):
        self.poem = poem
        self.create_line_num_dict()
        self.get_line_count()
        self.lines = line_tokenize(self.poem)
        self.create_stanzas_num_dict()
        self.get_stanza_count()

    def get_metre(self):
        pass

    def get_rhyme_scheme(self):
        """
        Obtains the rhyme scheme pattern for the poem. Checks whether the last word of each line rhymes with any
        subsequent lines and labels rhyming lines with the appropriate numeric signature (to be converted into
        alphabetical letters by Controller).
        :return a list of numbers indicating the rhyme scheme (E.g. [1, 2, 1, 2] for ABAB rhyme scheme).
        """
        rhyme_scheme = [0 for _ in range(self.line_count)]  # pre-populated list for labelling the rhyme scheme
        line_num_list = list(self.line_dict.keys())  # list of line indices
        assigned = set()  # set of lines that have had a rhyme signature assigned
        rhyme_signature = 1  # 1 = A; 2 = B etc...

        for i in line_num_list:
            if i in assigned:  # ignore lines that have already been assigned
                continue
            rhyme_word = no_punct(last_word(self.line_dict[i]).lower())  # obtains the last word in the line
            for j in line_num_list:
                if j in assigned:
                    continue
                # the last word in the line to compare rhymes to
                compare_word = no_punct(last_word(self.line_dict[j]).lower())
                if compare_word in rhymes(rhyme_word) or (compare_word == rhyme_word):
                    rhyme_scheme[j - 1] = rhyme_signature
                    assigned.add(j)
            rhyme_signature += 1
        return rhyme_scheme

    def stanzafy_rhyme_scheme(self):
        """
        Normalises the rhyme scheme for each stanza so that rhymes are contained within their stanzas and don't stretch
        across the whole poem. This is useful for ensuring that rhyme schemes don't get too distorted in the case of
        misidentification of rhymes.
        :return: a list of numbers indicating the rhyme scheme but normalised by stanza
        """
        rhyme_scheme = self.get_rhyme_scheme()
        stanzas = tokenize_stanzas(self.poem)
        line_break = 0
        stanza_list = []

        # Split rhyme scheme up by stanza and store in list of lists
        for s in stanzas:
            s_len = len(s.split("\n"))
            stanza_rhyme = rhyme_scheme[line_break:line_break+s_len]
            stanza_list.append(stanza_rhyme)
            line_break += s_len

        # Iterate through each stanza's rhyme scheme in the poem
        for s in range(len(stanza_list)):
            new_s = [0 for _ in range(len(stanza_list[s]))]  # prepare a new list to replace the previous one
            assigned = set()  # a set of assigned lines (see get_rhyme_scheme)
            rhyme_signature = 1  # the rhyme signature to replace the previous one

            for i in range(len(stanza_list[s])):
                if i in assigned:
                    continue
                for j in range(len(stanza_list[s])):
                    if j in assigned:
                        continue
                    if stanza_list[s][i] == stanza_list[s][j]:  # checks whether 2 lines in the stanza rhyme
                        new_s[j] = rhyme_signature  # assigns those lines the new rhyme signature
                        assigned.add(j)
                rhyme_signature += 1

            stanza_list[s] = new_s  # replaces the stanza's rhyme scheme from the main list

        # returns a flattened list for the new rhyme scheme so that output mirrors that of get_rhyme_scheme()
        return [item for sublist in stanza_list for item in sublist]

    def get_form(self):
        pass

    def get_alliteration(self):
        """
        Creates groups of alliterative word sequences per line, which are then stored as tuples within a list per line.
        Iterates through a line comparing pairs of words and groups them if they alliterate.
        :return: a list of lists corresponding to each line, containing tuples of alliterative groups
        """
        word_cache_dict = dict()  # A dictionary of word:alliterative_part pairs to improve performance
        offset = 1  # an integer measuring the distance from the first alliterative word in the sequence
        master = []  # A list of lists containing tuples of alliterative groups

        for l_no in self.line_dict.keys():  # line number
            line = self.line_dict[l_no]  # the line string
            words = tokenize_line_no_punk(line)
            line_lst = []  # the list for the line
            allit_group = []  # the group of words that alliterate
            word_cache_dict[words[0]] = alliterative_part(words[0])  # add first word's alliterative part to cache

            for i in range(1, len(words)):
                if words[i] not in word_cache_dict:
                    word_cache_dict[words[i]] = alliterative_part(words[i])
                new_word = word_cache_dict[words[i]]
                if new_word == word_cache_dict[words[i - offset]]:  # compares alliterative parts
                    if offset == 1:  # adds both the first and second word of the alliterative sequence to the group
                        allit_group.append(words[i - offset])
                        allit_group.append(words[i])
                        offset += 1
                    else:
                        allit_group.append(words[i])  # if offset is > 1 then only need to add the newest word
                else:
                    if len(allit_group) > 0:
                        line_lst.append(tuple(allit_group))  # converts group to tuple and adds to line list
                        allit_group.clear()
                    offset = 1
            if len(allit_group) > 0:  # does same as above but for alliterative words at end of line
                line_lst.append(tuple(allit_group))
            offset = 1
            master.append(line_lst)

        return master

    def get_assonance(self):
        """
        Iterates through words in a line and stores all of the vowel sounds in a list, `phone_lst`.
        Iterates through each word again and groups words that share the same vowel sounds.
        These are stored in lists [shared_vowel_sound, word1, word2,...] for each shared vowel sound.
        Appends this list to the assonance_lst and moves onto the next line.
        :return: a list of lists for each line, containing each shared vowel sound, and the words that share them.
        """
        word_dict = dict()

        l_no = 0
        assonance_lst = []
        for ln in self.lines:
            line = tokenize_line_no_punk(ln)  # split line and remove punctuation
            if len(line) == 0:  # skip empty lines
                continue
            l_no += 1
            line_lst = [l_no]
            phone_lst = []

            for word in line:
                if word not in word_dict:  # if word not already in word_dict, adds word entry & phones to dict
                    prons = phones_for_word(word)
                    if len(prons) > 0:
                        pron = prons[0]  # Obtains first pronunciation by default
                        word_dict[word] = [phone for phone in pron.split() if any(char.isdigit() for char in phone)]
                    else:
                        word_dict[word] = []  # not a proper solution - only for when words missing from cmudict!
                p = [phone for phone in word_dict[word] if phone not in phone_lst]  # temp list to add to phone_lst
                phone_lst.extend(p)

            for phone in phone_lst:  # for each of the phones in the line
                lst = [phone]
                for word in line:  # for each word in the line
                    if phone in word_dict[word]:  # check whether that word contains that phone
                        lst.append(word)  # if so, adds it to the list of words that are assonant with that phone
                if len(lst) > 2:  # checks that more than 1 word in the line shares that phone
                    # otherwise not assonant
                    line_lst.append(lst)  # adds list of words assonant on that phone to list for the line

            if len(line_lst) > 1:  # only adds to assonance list if line contains assonance
                assonance_lst.append(line_lst)

        return assonance_lst

    def get_consonance(self):
        pass

    def get_sibilance(self):
        """
        Searches each line for sibilant phoneme 'S' from cmudict's phoneme list. Stores these words in a list for each
        line.
        :return: a list of lists of sibilant words for each line.
        """
        sibilant_words = []  # tracks sibilant words
        line_count = 0  # tracks line number

        for ln in self.lines:  # iterate through non-blank lines
            line = tokenize_line_no_punk(ln)
            line_length = len(line)
            if line_length == 0:
                continue
            line_count += 1
            line_list = [line_count]
            for i in range(0, line_length):  # iterate through words in line
                if is_sibilant(line[i]):
                    line_list.append(line[i])
            if len(line_list) > 1:
                sibilant_words.append(line_list)

        return sibilant_words

    def get_internal_rhyme(self):
        pass

    def get_repetition(self):
        pass

    def get_anaphora(self):
        pass

    def get_simile(self):
        pass

    def get_enjambment(self):
        """
        Identifies lines that contain enjambment, i.e. the sentence runs over onto the next line.
        :return: a list of line numbers for lines in the poem that contain enjambment
        """
        l_no = 0
        enjambing_lines = []
        for line in self.lines:
            l_no += 1
            if len(line) == 0:  # skip empty or new lines
                continue
            tokens = word_tokenize(line)  # tokenize the line into words & punctuation
            if tokens[-1] in caesura_sym:
                continue  # if the final token is a 'caesura symbol' then it is not an enjambing line
            enjambing_lines.append(l_no)  # add the enjambing line number to the list of lines
        return enjambing_lines

    def get_caesura(self):
        """
        Identifies possible caesuras in a poem line by line. Tokenizes each line and checks each element against a group
        of caesura symbols. If the line contains caesura then it is reconstructed with the appropriate symbols
        indicating where the caesura occurs. These lines are then added to a list along with a line number, in turn
        added to a list of lists.
        :return: a list of lists for each line containing line number and the line with the caesura clearly marked
        """
        l_no = 1  # track line numbers
        caesura_lst = []
        for line in self.lines:
            if len(line) == 0:  # ignore empty lines or line breaks
                continue
            line_list = [l_no]
            words = word_tokenize(line)
            last_token = ""
            # remove punctuation at end of line as it's not a caesura
            if any(char in punctuation for char in words[-1]):
                last_token = words.pop(-1)  # save last punctuation to add back to line later
            if any(word in caesura_sym for word in words):  # checks if line contains caesura symbol
                # reconstruct line with caesura symbols delineated
                new_line = ["|" + str(word) + "|" if word in caesura_sym else word for word in words]
                new_str = " ".join(new_line) + last_token
                line_list.append(new_str)
            if len(line_list) > 1:
                caesura_lst.append(line_list)
            l_no += 1

        return caesura_lst

    def create_line_num_dict(self):
        """
        Matches each line in the poem with its corresponding line number and stores this inside a dictionary object.
        Allows this dictionary object to be queried by other methods, e.g. get_rhyme_scheme()
        """
        self.line_dict = dict()
        line_list = line_tokenize(self.poem, blanklines='discard')
        line_count = 1
        for line in line_list:
            self.line_dict[line_count] = line.strip()
            line_count += 1

    def get_line_count(self):
        """
        Gets the number of lines in the poem.
        """
        self.line_count = len(self.line_dict)

    def create_stanzas_num_dict(self):
        """
        Matches each stanza in the poem with its corresponding stanza number and stores this inside a dictionary object.
        Allows this dictionary object to be queried by other methods.
        """
        self.stanzas = dict()
        stanza_list = tokenize_stanzas(self.poem)
        stanza_count = 1
        for stanza in stanza_list:
            self.stanzas[stanza_count] = stanza.strip()
            stanza_count += 1

    def get_stanza_count(self):
        """
        Gets the number of stanzas in the poem.
        """
        self.stanza_count = len(self.stanzas)
