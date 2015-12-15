#!/usr/bin/env python3
import wikipedia
from elementalize import process


p = wikipedia.page("Christmas")
content = p.content
sentences = process.get_sentences(content)
results = process.atomize_sentences(sentences)
print(results)
