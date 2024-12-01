import polars as pl
from pymongo import MongoClient

from src.prepare_data import prepare_dataframe
from src.utils import download_and_extract

DATA_URL = "https://www.kaggle.com/api/v1/datasets/download/sohier/large-purchases-by-the-state-of-ca"

DATASET_PATH = "./data/PURCHASE ORDER DATA EXTRACT 2012-2015_0.csv"

MONGO_DB_NAME = "california_purchases"

COLLECTION_NAME = "purchase_orders"

download_and_extract(url=DATA_URL)

df = prepare_dataframe(dataset_path=DATASET_PATH)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client[MONGO_DB_NAME]

# Delete the collection if it already exists!
collist = db.list_collection_names()
if COLLECTION_NAME in collist:
    collection = db[COLLECTION_NAME]
    collection.drop()

# Crete collection
collection = db[COLLECTION_NAME]

# Convert the DataFrame to a list of dictionaries
df = df.with_columns(
    [
        pl.col("Creation Date").cast(pl.Datetime).alias("Creation Date"),
        pl.col("Purchase Date").cast(pl.Datetime).alias("Purchase Date"),
    ]
)
data = df.to_dicts()

# Insert the data into MongoDB
collection.insert_many(data)

print("Done!")
