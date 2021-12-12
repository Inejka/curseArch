import data_transformer
import network
import os
import file_worker
from timeit import default_timer as timer
from tensorflow import keras


class app:
    def __init__(self, user_name, epochs=1500):
        self.global_fw = file_worker.file_worker("data/db.sqlite")
        self.global_dt = data_transformer.data_transformer("data/db.sqlite")
        self.path = "users/" + user_name + "/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.local_fw = file_worker.file_worker(self.path + "db.sqlite")
        try:
            self.local_dt = data_transformer.data_transformer(self.path + "db.sqlite")
        except:
            self.reset_local_db()
            self.local_dt = data_transformer.data_transformer(self.path + "db.sqlite")
        self.epochs = epochs
        self.examples = ["проснуться", "покушоц", "погладить кота 1", "зайти в телегу", "скипнуть мемы",
                         "погладить кота 2",
                         "сделать лабу по ос", "написать отчёт к лабе по ос", "залить лабу по ос на гитхаб",
                         "оформить лабу по ос красиво", "сделать лабу по пивасу", "написать отчёт к лабе по пивасу",
                         "сделать проектик на спринге и оформить в гитхаб", "написать документацию для JMantic",
                         "опубликовать пакет JMantic на гитхаб", "погладить кота 3", "сделать чай",
                         "осудить себя за то, что между погладить кота 3 и 4 на самом деле смотрел ютаб", "пойти спать",
                         "покушоц и выпить чай", "покушоц и сделать чай", "убраться в квартире", "убраться из дома",
                         "сходить в магазин", "купить одежду", "купить технику", "Пусть будет подстричь кошке когти",
                         "NULL ETALON",
                         "Придумать подарки родителям на новый год", "Пересчитать шкалу скидок в курсовой",
                         "Выбрать место для прогулки", "Составить список дел на выходные", "Составить список покупок",
                         "Сделать последний укол"]
        try:
            self.load_global()
        except:
            print("You need to train global")
        try:
            self.load_local()
        except:
            print("You need to train local")

    def start(self):
        print("Started, enter commands")
        while True:
            command = input()
            if command == "exit" or command == '0':
                break
            if command == "train global" or command == '1':
                print(self.train_global())
            if command == "predict examples" or command == '2':
                arhc = self.predict_examples()
                for i, j in arhc:
                    print(i, j)
            if command == "update global database" or command == '3':
                print(self.update_global_database())
            if command == "save global" or command == '4':
                print(self.save_global())
            if command == "load global" or command == '5':
                print(self.load_global())
            if command == "predict" or command == "6":
                print(self.predict())
            if command == "add local task" or command == "7":
                print(self.add_local_task())
            if command == "reset local db" or command == "8":
                print(self.reset_local_db())
            if command == "train local" or command == "9":
                print(self.train_local())
            if command == "save local" or command == '10':
                print(self.save_local())
            if command == "load local" or command == '11':
                print(self.load_local())

    def train_global(self):
        self.global_net = network.model(self.global_dt.get_voc_size(), self.epochs)
        start = timer()
        X, Y = self.global_dt.get_train_data()
        self.global_net.fit(X, Y)
        return "Train global end in ", timer() - start

    def predict_examples(self):
        to_return = []
        for i in self.examples:
            to_return.append([i, self.get_time(i)[0]])
        return to_return

    def update_global_database(self):
        self.global_fw.reset_db()
        self.global_fw.transport_to_db("data/k_tasks")
        self.global_fw.transport_to_db("data/i_tasks")
        return "Database updated"

    def save_global(self):
        # self.global_net.save("data/" + "global")
        return "Global NOT saved"

    def load_global(self):
        self.global_net = network.model(self.global_dt.get_voc_size(), self.epochs)
        self.global_net.load("data/" + "global")
        return "Global loaded"

    def predict(self, args=None):
        if not args:
            args = input("Input string to predict: ")
        return self.get_time(args)

    def get_time(self, string):
        global_predict = self.global_net.predict([self.global_dt.get_vec(string)])
        local_predict = self.local_net.predict([self.local_dt.get_vec(string)])
        if local_predict == self.local_net.get_null_vector() and global_predict == self.global_net.get_null_vector():
            return "net doesn't know words"
        if local_predict == self.local_net.get_null_vector():
            return str(global_predict[0][0])
        if global_predict == self.global_net.get_null_vector():
            return str(local_predict[0][0])
        if global_predict == -1000 or local_predict == -1000:
            return str(local_predict[0][0])
        return str((0.9 * local_predict + 0.1 * global_predict)[0][0])

    def add_local_task(self, args=None):
        if not args:
            args = input("Enter task in format (Task:hours:minutes)(if task takes unpredicted time input T:-1:-1) -> ")
        self.local_fw.add_task(args)
        return "Task added"

    def reset_local_db(self):
        self.local_fw.reset_db()
        return "local database reset"

    def train_local(self):
        self.local_dt.reload()
        self.local_net = network.model(self.local_dt.get_voc_size(), self.epochs, local=True)
        start = timer()
        X, Y = self.local_dt.get_train_data()
        self.local_net.fit(X, Y)
        return "Train local end in ", timer() - start

    def save_local(self):
        self.local_net.save(self.path + "local")
        return "Local saved"

    def load_local(self):
        self.local_net = network.model(self.local_dt.get_voc_size(), self.epochs)
        self.local_net.load(self.path + "local")
        return "Local loaded"

    def execute(self, string, args):
        if string == "train global" or string == '1':
            return (self.train_global())
        if string == "predict examples" or string == '2':
            return self.predict_examples()
        if string == "update global database" or string == '3':
            return (self.update_global_database())
        if string == "save global" or string == '4':
            return (self.save_global())
        if string == "load global" or string == '5':
            return (self.load_global())
        if string == "predict" or string == "6":
            return (self.predict(args))
        if string == "add local task" or string == "7":
            return (self.add_local_task(args))
        if string == "reset local db" or string == "8":
            return (self.reset_local_db())
        if string == "train local" or string == "9":
            return (self.train_local())
        if string == "save local" or string == '10':
            return (self.save_local())
        if string == "load local" or string == '11':
            return (self.load_local())
