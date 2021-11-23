import pytest
from poetry_analyser.Utils import *


# Line ending in punctuation
def test_get_last_word01():
    line = "Shall I compare thee to a summer’s day?"
    assert last_word(line) == "day"


# Line ending with no punctuation
def test_get_last_word02():
    line = "Thou art more lovely and more temperate"
    assert last_word(line) == "temperate"


# Line ending with word split by apostrophe and ending in punctuation
def test_get_last_word03():
    line = "When in eternal lines to Time thou grow'st."
    assert last_word(line) == "grow'st"


# Empty line test
def test_get_last_word04():
    line = ""
    assert last_word(line) == ""


# 1 word line with punctuation
def test_get_last_word05():
    line = "lastword."
    assert last_word(line) == "lastword"


# Line ending word containing punctuation
def test_get_last_word06():
    line = "This is my husband's"
    assert last_word(line) == "husband's"


# Gibberish line with lots of punctuation
def test_get_last_word07():
    line = ",,,..dkjsj kld.,d; ompdwn;,;."
    assert last_word(line) == "ompdwn"


# Test for performance and for multiple punctuation symbols
def test_get_last_word08():
    line1 = "This is a line."
    line2 = "This is another;"
    line3 = "And yet another--"
    line4 = "The last one..."
    assert last_word(line1) == "line"
    assert last_word(line2) == "another"
    assert last_word(line3) == "another"
    assert last_word(line4) == "one"


# Empty line test
def test_word_freq01():
    s = ""
    assert word_freq(s) == dict()


# Test with no punctuation, lowercase
def test_word_freq02():
    s = "one two two three three three"
    assert word_freq(s) == {"one": 1, "two": 2, "three": 3}


# Test with punctuation, lowercase
def test_word_freq03():
    s = "one, two two, three, three, three."
    assert word_freq(s) == {"one": 1, "two": 2, "three": 3}


# Test with upper- and lowercase
def test_word_freq04():
    s = "one, Two two, three, Three, THREE."
    assert word_freq(s) == {"one": 1, "two": 2, "three": 3}


# Test with multiple lines
def test_word_freq05():
    s = """Tomorrow, and tomorrow, and tomorrow,
Creeps in this petty pace from day to day,
To the last syllable of recorded time;
And all our yesterdays have lighted fools
The way to dusty death."""

    assert word_freq(s) == {"tomorrow": 3, "creeps": 1, "petty": 1, "pace": 1, "day": 2, "last": 1, "syllable": 1,
                            "recorded": 1, "time": 1, "yesterdays": 1, "lighted": 1, "fools": 1,
                            "way": 1, "dusty": 1, "death": 1}


# Only stopwords
def test_word_freq06():
    s = "this that this that"
    assert word_freq(s) == {}


# Simple phoneme in cmudict
def test_alliterative_part01():
    assert alliterative_part("two") == "T"


# Ambiguous phoneme in cmudict
def test_alliterative_part02():
    assert alliterative_part("cheese") == "CH"


# Simple phoneme in cmudict (uppercase)
def test_alliterative_part03():
    assert alliterative_part("ZOO") == "Z"


# Ambiguous phoneme in cmudict (uppercase)
def test_alliterative_part04():
    assert alliterative_part("SHOP") == "SH"


# Phoneme different to letters in cmudict
def test_alliterative_part05():
    assert alliterative_part("chasm") == "K"


# Fricative phoneme in cmudict
def test_alliterative_part06():
    assert alliterative_part("zhivago") == "ZH"


# Phoneme different to letters in cmudict
def test_alliterative_part07():
    assert alliterative_part("cease") == "S"


# Word not in cmudict
def test_alliterative_part08():
    assert alliterative_part("wabe") == "W"


# Ambiguous phoneme not in cmudict
# Assert result has been changed to suit shortcomings of compile_alliterative_part()
@pytest.mark.xfail(reason="cmudict is too inaccurate for this test to pass. 'chiasmus' is not in the cmudict.")
def test_alliterative_part09():
    # Should be: assert alliterative_part("chiasmus") == "K"
    assert alliterative_part("chiasmus") == "CH"


# Word not in cmudict starting with multiple consonants
def test_alliterative_part10():
    assert alliterative_part("trinary") == "T"


# Line with punctuation attached to words
def test_tokenize_line_nopunk01():
    assert tokenize_line_no_punk("This is a line, with punctuation, that I'm trying to parse.") == \
           ["This", "is", "a", "line", "with", "punctuation", "that", "I'm", "trying", "to", "parse"]


# Line with standalone punctuation
def test_tokenize_line_no_punk02():
    assert tokenize_line_no_punk("Test for a line with a - in the middle.") == ["Test", "for", "a", "line", "with", "a",
                                                                                "in", "the", "middle"]


# Line with lots of punctuation
def test_tokenize_line_no_punk03():
    assert tokenize_line_no_punk("][]@@parse ,.,.this.,.., line .., ---[];;") == ["parse", "this", "line"]


# Test for obvious sibilant sound ('ss')
def test_is_sibilant01():
    assert is_sibilant("hiss") == True


# Test for s that sounds like 'z'
def test_is_sibilant02():
    assert is_sibilant("Does") == False


# Test for s that sounds like 'z'
def test_is_sibilant03():
    assert is_sibilant("lousy") == False


# Test for obvious sibilant sound ('s')
def test_is_sibilant04():
    assert is_sibilant("snake") == True


# Test for sibilant 'c'
def test_is_sibilant05():
    assert is_sibilant("cedar") == True


# Test for more complex sibilant word
def test_is_sibilant06():
    assert is_sibilant("Franciscan") == True


# Test for word not in cmudict
def test_is_sibilant07():
    assert is_sibilant("assonant") == False
