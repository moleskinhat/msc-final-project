## Project

This repository contains the project for Poetry Analyser.
Poetry Analyser performs the analysis of poetic devices in English-language poems (e.g., rhyme scheme, alliteration, 
assonance, enjambment, caesura) with the aim of enhancing the practice of close reading. 
Primarily targeted at English Literature students, this application hopes to help users develop their close reading and 
analytical skills by encouraging them to get stuck into a text's literary devices, language, and patterns.

## Installation
Installation is self-contained using Python's setuptools. Dependencies are specified in the `setup.py` python file. 

This program requires `tkinter` to be installed (possibly separately if not installed by default on your system).

Simply clone this package, navigate to it and install it using:
```
$ pip install . # optionally use '-e' to install this package using the 'editable' feature
```

The `setup.py` file specifies an entrypoint `poetry_analyser` which is created when this package is installed. 
Furthermore, a post-install step is run to install the nltk data dependencies (`stopwords` and `punkt`). 
These dependencies are installed in the user's home directory.

Once the program is installed, fire up the command prompt and type the following to bring up the GUI:
```
$ poetry_analyser
```

Run tests by executing pytest:
```
$ pytest
```

The tests in the package `test/performance` are not run when calling `pytest` as they are scripts provided to allow 
developers to tune the performance of the underlying models.

## User Guide

1. Type your poem into the input box on the left.
2. Press `Enter` to load the poem into the system and generate line numbers. The box on the right confirms the entry.
3. Press any of the `analytical buttons` to bring up the results of the analyses
