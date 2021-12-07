import spacy
import sqlite3

# coding=utf8
nlp = spacy.load("ru_core_news_lg")
# pos = []
# rarity = {}
ok_types = ['VERB', 'NOUN', 'ADP']


def transoport_to_db(file_name):
    conn = sqlite3.connect("data/db.sqlite")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS keywords_db")
    c.execute("CREATE TABLE keywords_db (keyword TEXT,UNIQUE(keyword))")
    c.execute("DROP TABLE IF EXISTS tasks")
    c.execute("CREATE TABLE tasks (task TEXT,time INTEGER, UNIQUE(task))")
    file = open(file_name, 'r', encoding="utf8")
    while True:
        line = file.readline()
        if not line:
            break
        words, hour, minutes = line.split(':')
        c.execute("INSERT OR IGNORE INTO tasks(task,time) VALUES(?,?)", (words, (int(hour) * 60 + int(minutes))))
        tmp = nlp(words)
        for token in tmp:
            if (token.pos_ in ok_types and not token.is_stop):
                c.execute("INSERT OR IGNORE INTO keywords_db(keyword) VALUES(?)", (token.lemma_,))
            # print(token.lemma_, token.is_stop, token.pos_)
            # if not (token.pos_ in pos):
            #    pos.append(token.pos_)
            # try:
            #    rarity[token.pos_]
            # except:
            #    rarity[token.pos_] = 0
            # rarity[token.pos_] += 1
    # for i in pos:
    # print(i, rarity[i])
    file.close()
    conn.commit()
    conn.close()

# ['VERB', 'NOUN', 'ADP', 'PROPN', 'CCONJ', 'ADJ', 'NUM', 'ADV', 'PUNCT']
# ['VERB', 'NOUN', 'ADP', 'SPACE', 'PROPN', 'ADJ', 'PUNCT', 'CCONJ', 'PRON', 'ADV', 'NUM', 'PART', 'SCONJ', 'AUX', 'X', 'DET']
