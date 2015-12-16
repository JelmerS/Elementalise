#!/usr/bin/env python3
# from time import sleep
import unicodedata

from nltk import tokenize

#
#
elementa_list = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg',
                 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V',
                 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se',
                 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh',
                 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba',
                 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho',
                 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt',
                 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
                 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
                 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg',
                 'Cn', 'Fl', 'Lv'
                 ]


def recur_text(sentence):
    # Expects lowercase sentence, with no spaces and no punctuation.
    loc = 0
    atomized_sentence = ''
    while loc < len(sentence):
        i = 1
        one = False
        two = False
        for element in elementa_list:
            if element.lower() == sentence[loc]:
                one = True
                element_one = element
            if loc + i + 1 < len(sentence) and element.lower() == sentence[loc] + sentence[loc + i]:
                two = True
                element_two = element
        if one and not two:
            atomized_sentence += element_one
            loc += i
        if two and not one:
            atomized_sentence += element_two
            # print(atomized_sentence + '-' + sentence[loc+i+1::])
            loc = loc + i + 1
        if one and two:
            # if there's more than one option for next element, try to solve with element of length 1 first,
            # by recurring with sub-sentence except when end of sentence:
            loc += i
            if loc + 1 == len(sentence):
                atomized_sentence += element_two
                return atomized_sentence
            # print('forking%s', sentence[loc::])
            fork1 = recur_text(sentence[loc::])
            if fork1 == '':
                loc += 1
                # print('forking%s', sentence[loc::])
                fork2 = recur_text(sentence[loc::])
                if fork2 == '':
                    return ''
                else:
                    atomized_sentence += element_two + fork2
                    return atomized_sentence
            else:
                atomized_sentence += element_one + fork1
                return atomized_sentence
        if not one and not two:
            # Failed
            return ''
    return atomized_sentence


# noinspection PyUnreachableCode
def atomize_sentences(sentence_list):
    # todo: Make a dict of correct sentences with atomised next to it.
    good_sentences = []
    for sentence in sentence_list:
        sentence = cleanup(sentence)
        sentence_result = recur_text(sentence)
        if sentence_result != '':
            good_sentences.append(sentence_result)
    return good_sentences


def atomize_words(word_list):
    good_words = []
    for word in word_list:
        word = cleanup(word)
        word_result = recur_text(word)
        if word_result != '':
            good_words.append(word_result)
    return good_words


def cleanup(characters):
    nfkd_form = unicodedata.normalize('NFKD', characters)
    characters = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return ''.join([c.lower() for c in characters if c.isalpha()])


def read_file(name):
    f = open(name, 'r')
    text = f.read()
    return text


def get_words(text):
    # input: text with punctuation
    # output: list of words
    return tokenize.word_tokenize(text)


def get_unique_words(text):
    # input: text with punctuation
    # output: list of unique words
    all_words = get_words(text)
    unique_words = []
    for i in all_words:
        if not i in unique_words:
            unique_words.append(i)
    return unique_words


def get_sentences(text):
    # input: text with punctuation
    # output: list of sentences
    sentence_list = tokenize.sent_tokenize(text)
    return sentence_list


# Main
if __name__ == "__main__":
    # filename = 'NBVtekst'
    filename = 'test'
    # filename = 'Het-Boek.txt'
    results = atomize_sentences(get_sentences(read_file(filename)))
    file_ = open('output', 'w')

    for result in results:
        file_.write(result)
        file_.write('\n')
        print(result)
    file_.close()
