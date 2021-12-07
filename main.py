import file_worker
import data_transformer

#file_worker.transport_to_db("data/k_tasks")
dt = data_transformer.data_transformer()
print(dt.get_train_data())

