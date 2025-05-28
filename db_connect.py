from pymongo import MongoClient
import os

print(f">>> db_connect.py загружен из: {os.path.abspath(__file__)}")
print(">>> Используется db_connect.py с прямым подключением к порту 30002 (mongo2)")

# Подключаемся напрямую к узлу, который сейчас является primary (mongo2:30002)
client = MongoClient("mongodb://localhost:30002/?replicaSet=my-replica-set&directConnection=true")
db = client["cement_factory"]
