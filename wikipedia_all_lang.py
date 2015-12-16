#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import wikipedia
from elementalize import process

wiki_url = 'https://en.wikipedia.org/wiki/Periodic_table'

print("Source page :" + wiki_url)

# get languages
soup = BeautifulSoup(urllib.request.urlopen(wiki_url), "html.parser")
links = [(el.get('lang'), el.get('title')) for el in soup.select('li.interlanguage-link > a')]

for language, title in links:
    page_title = title.split(u' – ')[0]
    wikipedia.set_lang(language)
    page = wikipedia.page(page_title)
    print("Results for language " + language + ":\n")
    sentences = process.get_unique_words(page.content)
    results = process.atomize_words(sentences)
    print(results)
    print("-----\n")
