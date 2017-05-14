# phrase-corrector

## Synopsis

A python web server which provides

* phrase corrections with the probablility of it being correct.
* topic modeling for the provided phrases

### Prerequisites
* list of keywords to train the program
* list of synonyms

## Motivation

Didn't came accross any free and opensource solution which solves the problem phrase coreection. Peter norvig's [solution](http://norvig.com/spell-correct.html) explains how to correct spellings of individual keywords. But in real world we get much or information about a word when it is used in a sentance or phrase. Thats why I am useing bigrams to find the best possible correction.

## Acknowledgments

* [peter norvig](http://norvig.com/spell-correct.html)