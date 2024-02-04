import os
from pymongo import MongoClient
from googleapiclient.discovery import build
import googleapiclient.errors

client = MongoClient("mongodb://localhost:27017")
print(client.test)

print(client.list_database_names())
