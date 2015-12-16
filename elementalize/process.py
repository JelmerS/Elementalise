#!/usr/bin/env python3
#from time import sleep
from nltk import tokenize
import string
import unicodedata

#
#
elementa_list=[ 'H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg',
				'Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V',
				'Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se',
				'Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh',
				'Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba',
				'La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho',
				'Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt',
				'Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac',
				'Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm',
				'Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg',
				'Cn','Fl','Lv'
			]

def recurr_text(sentence):
	#Expects lowercase sentence, with no spaces and no punctuation.
	loc = 0
	atomized_sentence = ''
	while loc < len(sentence):
		i = 1
		one = False
		two = False
		#if loc+i+1 < len(sentence) and sentence[loc+i] == ' ':
		#	i = 2
		for element in elementa_list:
			if element.lower() == sentence[loc]:
				one = True
				element_one = element
			if loc+i+1 < len(sentence) and element.lower() == sentence[loc] + sentence[loc+i]:
				two = True
				element_two = element
		if one and not two:
			atomized_sentence += element_one
			#print(atomized_sentence + '-' + sentence[loc+i::])
			loc = loc + i
		if two and not one:
			atomized_sentence += element_two
			#print(atomized_sentence + '-' + sentence[loc+i+1::])
			loc = loc + i + 1
		if one and two:
			#if there's more than one option for next element, try to solve with element of length 1 first, by recurring with subsentence ecxept when end of sentence:
			loc = loc + i
			if loc + 1 == len(sentence):
				atomized_sentence += element_two
				return atomized_sentence
			#print('forking%s', sentence[loc::])
			fork1 = recurr_text(sentence[loc::])
			if fork1 == '':
				loc = loc + 1
				#print('forking%s', sentence[loc::])
				fork2 = recurr_text(sentence[loc::])
				if fork2 == '':
					return''
				else:
					atomized_sentence += element_two + fork2
					return atomized_sentence
			else:
				atomized_sentence += element_one + fork1
				return atomized_sentence
		if not one and not two:
			#print('Got to ' + atomized_sentence)
			return ''
	return atomized_sentence


def atomize_sentences(sentence_list):
	#todo: Make a dict of correct sentences with atomised next to it.
	Good_Sentences = []
	for sentence in sentence_list:
		sentence = cleanup(sentence)
		sentence_result	= recurr_text(sentence)
		if sentence_result != '':
			Good_Sentences.append(sentence_result)
	return Good_Sentences

def atomize_words(word_list):
	Good_Words = []
	for word in word_list:
		word = cleanup(word)
		word_result = recurr_text(word)
		if word_result != '':
			Good_Words.append(word_result)
	return Good_Words

def cleanup(input):
	#input = input.replacediacritics
	nfkd_form = unicodedata.normalize('NFKD', input)
	input = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
	return ''.join([c.lower() for c in input if c.isalpha()])

def read_file(filename):
	f = open(filename,'r')
	text = f.read()
	return text


def get_words(text):
	#input: text with punctuation
	#output: list of words
	return tokenize.word_tokenize(text)

def get_unique_words(text):
	#input: text with punctuation
	#output: list of unique words
	allWords = get_words(text)
	uniqueWords = [] 
	for i in allWords:
		if not i in uniqueWords:
			uniqueWords.append(i)
	return uniqueWords

def get_sentences(text):
	#input: text with punctuation
	#output: list of sentences
	sentence_list = tokenize.sent_tokenize(text)
	return sentence_list

#Main
if __name__ == "__main__":
	#filename = 'NBVtekst'
	filename = 'test'
	#filename = 'Het-Boek.txt'
	results = atomize_sentences(get_sentences(read_file(filename)))
	file_ = open('output', 'w')

	for result in results:
		file_.write(result)
		file_.write('\n')
		print(result)
	file_.close()
