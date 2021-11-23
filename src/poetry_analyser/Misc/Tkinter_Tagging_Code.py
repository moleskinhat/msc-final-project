import tkinter as tk
from string import punctuation
from nltk import word_tokenize, line_tokenize


# Taken from Utils
def last_word(line):
    line.strip()  # removes any whitespace
    if len(line) != 0:  # Ignores empty lines
        return [word for word in word_tokenize(line) if word not in punctuation][-1]
    return ""


root = tk.Tk()
txt = tk.Text(root)
txt.pack()

text = """Shall I compare thee to a summer’s day?
Thou art more lovely and more temperate.
Rough winds do shake the darling buds of May,
And summer’s lease hath all too short a date.
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimmed;
And every fair from fair sometime declines,
By chance, or nature’s changing course, untrimmed;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow’st,
Nor shall death brag thou wand'rest in his shade,
When in eternal lines to Time thou grow'st.
So long as men can breathe, or eyes can see,
So long lives this, and this gives life to thee."""

txt.insert("1.0", text)
l_no = 1
lines = line_tokenize(txt.get("1.0", "end-1c"))
# print(lines)
l_word = ""
for line in lines:
    l_length = len(line)-1
    # print(l_length)
    l_word = last_word(line)
    w_length = len(l_word)
    # print(l_word, w_length)
    txt.tag_add("highlight", str(l_no) + "." + str(l_length - w_length), str(l_no) + "." + str(l_length))
    txt.tag_configure("highlight", foreground="red", background="yellow")
    l_no += 1

root.mainloop()