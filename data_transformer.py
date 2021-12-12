import sqlite3
import spacy
# https://pythonrepo.com/repo/ahmados-rusynonyms-python-natural-language-processing
from ru_synonyms import SynonymsGraph


class data_transformer:

    def __init__(self, path):
        self.path = path
        self.nlp = spacy.load("ru_core_news_lg")
        self.reload()
        self.sg = SynonymsGraph()

    def get_voc_size(self):
        return self.vocabulary_size

    def get_train_data(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        X = []
        Y = []
        for i in c:
            vec = self.get_vec(i[0])
            X.append(vec)
            Y.append(i[1] if i[1] > 0 else -100)
            # data.append([vec, i[1] if i[1] > 0 else -1000])
        conn.close()
        return X, Y

    def get_vec(self, str, show_res=False):
        to_return = self.zeros_list.copy()
        tmp = self.nlp(str)
        for token in tmp:
            try:
                index = self.vocabulary[token.lemma_]
            except:
                if show_res and not token.is_stop:
                    # print(token.lemma_, "---", self.most_similar(self.nlp.vocab[token.lemma_]))
                    # print(self.sg.is_in_dictionary(token.lemma_))
                    if self.sg.is_in_dictionary(token.lemma_):
                        listt = self.sg.get_list(token.lemma_)
                        for i in listt:
                            found = False
                            try:
                                index = self.vocabulary[token.lemma_]
                            except:
                                pass
                            else:
                                to_return[index] += 1
                                found = True
                            if found:
                                break
            else:
                to_return[index] += 1
        return to_return

    def get_vecs(self, strs, show_res=False):
        test = []
        for i in strs:
            temp = self.get_vec(i, show_res)
            test.append(temp)
        return test

    def reload(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT * FROM keywords")
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

    def most_similar(self, word):
        by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
        return [w.orth_ for w in by_similarity[:10]]
