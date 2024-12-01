import polars as pl
from src.utils import download_and_extract
from src.prepare_data import prepare_dataframe

DATA_URL = "https://www.kaggle.com/api/v1/datasets/download/sohier/large-purchases-by-the-state-of-ca"

DATASET_PATH = "./data/PURCHASE ORDER DATA EXTRACT 2012-2015_0.csv"

download_and_extract(url=DATA_URL)

df = prepare_dataframe(dataset_path=DATASET_PATH)

df.write_database(
    table_name="purchase_orders",
    connection="sqlite:///data/california_purchases.db",
)
