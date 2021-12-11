import spacy
import sqlite3

# coding=utf8
# pos = []
# rarity = {}
ok_types = ['VERB', 'NOUN', 'ADP']


class file_worker:
    def __init__(self, path):
        self.path = path
        self.nlp = spacy.load("ru_core_news_lg")

    def reset_db(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS keywords")
        c.execute("CREATE TABLE keywords (keyword TEXT,UNIQUE(keyword))")
        c.execute("DROP TABLE IF EXISTS tasks")
        # c.execute("CREATE TABLE tasks (task TEXT,time INTEGER, UNIQUE(task))")
        c.execute("CREATE TABLE tasks (task TEXT,time INTEGER)")
        conn.commit()
        conn.close()

    def transport_to_db(self, file_name):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        file = open(file_name, 'r', encoding="utf8")
        while True:
            line = file.readline()
            if not line:
                break
            words, hour, minutes = line.split(':')
            c.execute("INSERT INTO tasks(task,time) VALUES(?,?)", (words, (int(hour) * 60 + int(minutes))))
            tmp = self.nlp(words)
            for token in tmp:
                if (token.pos_ in ok_types and not token.is_stop):
                    c.execute("INSERT OR IGNORE INTO keywords(keyword) VALUES(?)", (token.lemma_,))
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

    def add_task(self, task):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        words, hour, minutes = task.split(':')
        c.execute("INSERT INTO tasks(task,time) VALUES(?,?)", (words, (int(hour) * 60 + int(minutes))))
        tmp = self.nlp(words)
        for token in tmp:
            if (not token.is_stop):
                c.execute("INSERT OR IGNORE INTO keywords(keyword) VALUES(?)", (token.lemma_,))
        conn.commit()
        conn.close()

# ['VERB', 'NOUN', 'ADP', 'PROPN', 'CCONJ', 'ADJ', 'NUM', 'ADV', 'PUNCT']
# ['VERB', 'NOUN', 'ADP', 'SPACE', 'PROPN', 'ADJ', 'PUNCT', 'CCONJ', 'PRON', 'ADV', 'NUM', 'PART', 'SCONJ', 'AUX', 'X', 'DET']
