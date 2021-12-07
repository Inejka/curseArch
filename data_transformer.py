import sqlite3
import spacy


class data_transformer:

    def __init__(self):
        self.nlp = spacy.load("ru_core_news_lg")
        conn = sqlite3.connect("data/db.sqlite")
        c = conn.cursor()
        c.execute("SELECT * FROM keywords")
        # print(c.fetchall())
        self.vocabulary = {}
        j = 0
        for i in c:
            self.vocabulary[i[0]] = j
            j += 1
        self.vocabulary_size = j
        self.zeros_list = []
        for i in range(j):
            self.zeros_list.append(0)
        conn.close()

    def get_train_data(self):
        conn = sqlite3.connect("data/db.sqlite")
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        data = []
        for i in c:
            vec = self.get_vec(i[0])
            data.append([vec, i[1] if i[1] > 0 else -1000])
        conn.close()
        return data

    def get_vec(self, str):
        to_return = self.zeros_list.copy()
        tmp = self.nlp(str)
        for token in tmp:
            try:
                index = self.vocabulary[token.lemma_]
            except:
                print(token.lemma_)
                pass
            else:
                to_return[index] += 1
        return to_return
