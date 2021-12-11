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
        self.local_dt = data_transformer.data_transformer(self.path + "db.sqlite")
        self.local_fw = file_worker.file_worker(self.path + "db.sqlite")
        self.epochs = epochs
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            self.local_fw.reset_db()
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
        self.load_global()

    def start(self):
        print("Started, enter commands")
        while True:
            command = input()
            if command == "exit" or command == '0':
                break
            if command == "train global" or command == '1':
                self.train_global()
            if command == "predict examples" or command == '2':
                self.predict_examples()
            if command == "update global database" or command == '3':
                self.update_global_database()
            if command == "save global" or command == '4':
                self.save_global()
            if command == "load global" or command == '5':
                self.load_global()
            if command == "predict" or command == "6":
                self.predict()
            if command == "add local task" or command == "7":
                self.add_local_task()
            if command == "reset local db" or command == "8":
                self.reset_local_db()
            if command == "train local" or command == "9":
                self.train_local()

    def train_global(self):
        self.global_net = network.model(self.global_dt.get_voc_size(), self.epochs)
        start = timer()
        X, Y = self.global_dt.get_train_data()
        self.global_net.fit(X, Y)
        print("Train global end in ", timer() - start)

    def predict_examples(self):
        ans = self.global_net.predict(self.global_dt.get_vecs(self.examples))
        for i, j in zip(self.examples, ans):
            print(i, j)

    def update_global_database(self):
        self.global_fw.reset_db()
        self.global_fw.transport_to_db("data/k_tasks")
        self.global_fw.transport_to_db("data/i_tasks")
        print("Database updated")

    def save_global(self):
        # self.global_net.save("data/" + "global")
        print("Global NOT saved")

    def load_global(self):
        self.global_net = network.model(self.global_dt.get_voc_size(), self.epochs)
        self.global_net.load("data/" + "global")
        print("Global loaded")

    def predict(self):
        str = input("Input string to predict: ")
        global_predict = self.global_net.predict([self.global_dt.get_vec(str)])
        local_predict = self.local_net.predict([self.local_dt.get_vec(str)])
        print(global_predict)
        print(local_predict)
        print(self.global_net.get_null_vector())
        print(self.local_net.get_null_vector())
        if local_predict == self.local_net.get_null_vector():
            print(global_predict)
        else:
            if (global_predict == -1000):
                print(local_predict)
            else:
                print(global_predict * 0.1 + local_predict * 0.9)

    def add_local_task(self):
        task = input("Enter task in format (Task:hours:minutes)(if task takes unpredicted time input T:-1:-1) -> ")
        self.local_fw.add_task(task)
        print("Task added")

    def reset_local_db(self):
        self.local_fw.reset_db()

    def train_local(self):
        self.local_dt.reload()
        self.local_net = network.model(self.local_dt.get_voc_size(), self.epochs, local=True)
        start = timer()
        X, Y = self.local_dt.get_train_data()
        self.local_net.fit(X, Y)
        print("Train local end in ", timer() - start)
