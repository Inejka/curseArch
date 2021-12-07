import spacy
from collections import Counter
from string import punctuation

# coding=utf8

nlp = spacy.load("ru_core_news_lg")
text = """Когда я только начинал работать удаленно, то целые месяцы приводил в порядок свое рабочее место, стараясь 
довести всё до совершенства. Стол, кронштейны для монитора, веб-камера – просто остановиться не мог. Моя работа 
напрямую связана с тем, чтобы повышать людям производительность, так что о подобных вещах я думаю много."""
doc = nlp(text)
for token in doc:
    print('{}--->{}'.format(token, token.lemma_))
print(doc.ents)
