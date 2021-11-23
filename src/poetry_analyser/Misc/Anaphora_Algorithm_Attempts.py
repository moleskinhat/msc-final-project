from collections import Counter
import numpy as np


def most_frequent(lst):
    occurrence_count = Counter(lst)
    return occurrence_count.most_common(1)[0][0]


def line_matrix(line_list):
    matrix = []
    word_counter = 0
    last_word = max([len(line.split()) for line in line_list]) - 1

    while word_counter <= last_word:
        i_wordlist = []
        for line in line_list:
            if word_counter >= len(line.split()):
                i_wordlist.append("*")
            else:
                words = line.split()
                i_wordlist.append(words[word_counter])
        matrix.append(i_wordlist)
        word_counter += 1

    return np.array(matrix)


lines = ["Every breath you take",
         "Every move you make",
         "Every bond you break",
         "Every step you take",
         "I'll be watching you"]

matrix = line_matrix(lines)

anaphoric_line = []

freq = most_frequent(matrix[0])

poss_lines = []

for i in range(0, len(matrix[0])):
    if matrix[0][i] == freq:
        poss_lines.append(i)

extracted_matrix = matrix[:, poss_lines]

print(extracted_matrix)