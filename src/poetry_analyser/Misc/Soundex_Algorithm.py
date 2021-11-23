def soundex(word):
    """
    Uses the Soundex phonetic algorithm to obtain a 4-digit code for a word's pronunciation.
    :param word: the word to be codified
    :return: 4 digit code
    """
    encoding = [' ', ' ', ' ', ' ']  # prepares 4-digit list for encryption
    encoding_index = 1

    char_maps = "01230120022455012623010202"  # alphabetical char->digit encryption map

    encoding[0] = word[0].upper()  # Obtains first char of the word

    for i in range(1, len(word)):
        c = ord(word[i].upper()) - 65
        if 0 <= c <= 25:
            if char_maps[c] != '0':
                if char_maps[c] != encoding[encoding_index - 1]:  # ignores if char is same as previous char
                    encoding[encoding_index] = char_maps[c]
                    encoding_index += 1
                if encoding_index > 3:  # breaks after 3
                    break

    if encoding_index <= 3:
        while (encoding_index <= 3):
            encoding[encoding_index] = '0'
            encoding_index += 1

    return ''.join(encoding)


print(soundex("brown"))  # returns B650
print(soundex("town"))  # returns T500
print(soundex("gown"))  # returns G500

# All 3 rhyme but only 2 share a code ending
