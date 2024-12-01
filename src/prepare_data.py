import polars as pl

def prepare_dataframe(dataset_path):
# Define the column names and their data types
    column_names = [
        'Creation Date', 'Purchase Date', 'Fiscal Year', 'LPA Number', 'Purchase Order Number',
        'Requisition Number', 'Acquisition Type', 'Sub-Acquisition Type', 'Acquisition Method',
        'Sub-Acquisition Method', 'Department Name', 'Supplier Code', 'Supplier Name',
        'Supplier Qualifications', 'Supplier Zip Code', 'CalCard', 'Item Name', 'Item Description',
        'Quantity', 'Unit Price', 'Total Price', 'Classification Codes', 'Normalized UNSPSC',
        'Commodity Title', 'Class', 'Class Title', 'Family', 'Family Title', 'Segment',
        'Segment Title', 'Location'
    ]

    # Read the CSV file with the specified column names
    df = pl.read_csv(dataset_path, has_header=True, new_columns=column_names, infer_schema_length=10000)

    # Convert the 'Creation Date' and 'Purchase Date' columns to datetime
    df = df.with_columns([
        pl.col('Creation Date').str.strptime(pl.Date, format="%m/%d/%Y", strict=False).alias('Creation Date'),
        pl.col('Purchase Date').str.strptime(pl.Date, format="%m/%d/%Y", strict=False).alias('Purchase Date')
    ])

    # Convert the 'Unit Price' and 'Total Price' columns to float, removing the dollar sign and commas
    pruchase_orders = df.with_columns([
        pl.col('Unit Price').str.replace_all(r'[\$,]', '').cast(pl.Float64).alias('Unit Price'),
        pl.col('Total Price').str.replace_all(r'[\$,]', '').cast(pl.Float64).alias('Total Price')
    ])


    pruchase_orders.write_parquet("data/california_purchase_orders.parquet")

    return pruchase_orders