from textwrap import dedent

DATA_INFORMATION = {
    "document_title": "DGS Purchasing Data Dictionary",
    "fields": [
        {
            "name": "Creation Date",
            "description": "System Date",
            "additional_notes": "Date of purchase order entered by user, can be backdated",
        },
        {
            "name": "Purchase Date",
            "description": "Date of purchase order entered by user",
            "key_details": [
                "Can be backdated",
                "Creation date is primarily used for tracking",
            ],
        },
        {
            "name": "Fiscal Year",
            "description": "Derived based on creation date",
            "details": {
                "start_date": "July 1",
                "end_date": "June 30",
                "jurisdiction": "State of California",
            },
            "unique_values": ["2014-2015", "2013-2014", "2012-2013"],
        },
        {
            "name": "LPA Number",
            "description": "Leveraged Procurement Agreement Number",
            "aliases": ["Contract Number"],
            "special_condition": "If contract number exists, amount is considered contract spend",
        },
        {
            "name": "Purchase Order Number",
            "description": "Identifier for purchase order",
            "constraints": [
                "Numbers are not unique",
                "Different departments can have same purchase order number",
            ],
        },
        {
            "name": "Requisition Number",
            "description": "Identifier for requisition",
            "constraints": [
                "Numbers are not unique",
                "Different departments can have same requisition number",
            ],
        },
        {
            "name": "Acquisition Type",
            "description": "Type of acquisition",
            "categories": [
                "Non-IT Goods",
                "Non-IT Services",
                "IT Goods",
                "IT Services",
            ],
        },
        {
            "name": "Sub-Acquisition Type",
            "description": "Depends on primary acquisition type",
            "recommendation": "Refer to full data dictionary for details",
        },
        {
            "name": "Acquisition Method",
            "description": "Method used to make purchase",
            "recommendation": "Consult data dictionary and supplemental acquisition method document",
        },
        {
            "name": "Sub-Acquisition Method",
            "description": "Depends on primary acquisition method",
            "recommendation": "Refer to data dictionary for details",
        },
        {
            "name": "Department Name",
            "description": "Name of purchasing department",
            "type": "Normalized field",
        },
        {
            "name": "Supplier Code",
            "description": "Unique supplier identifier",
            "type": "Normalized field",
        },
        {
            "name": "Supplier Name",
            "description": "Name entered by supplier during state registration",
        },
        {
            "name": "Supplier Qualifications",
            "description": "Certification categories",
            "categories": [
                "Small Business (SB)",
                "Small Business Enterprise (SBE)",
                "Disabled Veteran Business Enterprise (DVBE)",
                "Non-Profits (NP)",
                "Micro-Business (MB)",
            ],
            "key_note": "Qualifications are not mutually exclusive; a supplier can have multiple certifications",
        },
        {
            "name": "Supplier Zip Code",
            "description": "Geographic identifier for supplier",
        },
        {
            "name": "CalCard",
            "description": "State credit card usage",
            "values": ["Yes", "No"],
        },
        {"name": "Item Name", "description": "Name of items being purchased"},
        {
            "name": "Item Description",
            "description": "Detailed description of items being purchased",
        },
        {"name": "Quantity", "description": "Number of items being purchased"},
        {"name": "Unit Price", "description": "Price per individual item"},
        {
            "name": "Total Price",
            "description": "Aggregate price of items",
            "exclusions": ["Does not include taxes", "Does not include shipping"],
        },
        {
            "name": "Classification Codes",
            "description": "United Nations Standard Products and Services Code (UNSPSC) v. 14",
            "details": [
                "May have multiple UNSPSC numbers based on line items",
                "Entered in eSCPRS system",
            ],
        },
        {
            "name": "Normalized UNSPSC",
            "description": "Standardized UNSPSC number",
            "details": "First 8 digits identify entire purchase order",
        },
        {
            "name": "Commodity Title",
            "description": "Correlated title based on 8-digit Normalized UNSPSC",
        },
        {
            "name": "Class",
            "description": "Correlated class number based on 8-digit Normalized UNSPSC",
        },
        {
            "name": "Class Title",
            "description": "Correlated class title based on 8-digit Normalized UNSPSC",
        },
        {
            "name": "Family",
            "description": "Correlated family number based on 8-digit Normalized UNSPSC",
        },
        {
            "name": "Family Title",
            "description": "Correlated family title based on 8-digit Normalized UNSPSC",
        },
        {
            "name": "Segment",
            "description": "Correlated segment number based on 8-digit Normalized UNSPSC",
        },
    ],
    "reference": {
        "unspsc_website": "http://www.unspsc.org/",
        "version": "UNSPSC v. 14",
    },
}

DATABASE_SCHEMA = """CREATE TABLE purchase_orders (
        "Creation Date" DATE, 
        "Purchase Date" DATE, 
        "Fiscal Year" TEXT, 
        "LPA Number" TEXT, 
        "Purchase Order Number" TEXT, 
        "Requisition Number" TEXT, 
        "Acquisition Type" TEXT, 
        "Sub-Acquisition Type" TEXT, 
        "Acquisition Method" TEXT, 
        "Sub-Acquisition Method" TEXT, 
        "Department Name" TEXT, 
        "Supplier Code" BIGINT, 
        "Supplier Name" TEXT, 
        "Supplier Qualifications" TEXT, 
        "Supplier Zip Code" TEXT, 
        "CalCard" TEXT, 
        "Item Name" TEXT, 
        "Item Description" TEXT, 
        "Quantity" FLOAT, 
        "Unit Price" FLOAT, 
        "Total Price" FLOAT, 
        "Classification Codes" TEXT, 
        "Normalized UNSPSC" BIGINT, 
        "Commodity Title" TEXT, 
        "Class" BIGINT, 
        "Class Title" TEXT, 
        "Family" BIGINT, 
        "Family Title" TEXT, 
        "Segment" BIGINT, 
        "Segment Title" TEXT, 
        "Location" TEXT
)"""

TEXT2SQL_SYSTEM_MESSAGE = """You're an excellent data analyst that writes sql queries based on questions and quries in natural langauge.
    Return valid sql directly without any introductions"""
TEXT2SQL_USER_MESSAGE = dedent('''\
    You have access to data about purchase orders for the state of California.
    The SQL code that was used to create the database is given under `## DATABASE_SCHEMA:`.
    Some information about the fields and what they represent is given under `## DATA_INFORMATION`
    Use these to write a sql query to fetch data that is needed to answer a user's question.
    
    ## DATABASE_SCHEMA:
    """
    {database_schema}
    """

    ## DATA_INFORMATION:
    """
    {data_information}
    """
    
    ## USER_QUESTION:
    """
    {user_question}
    """
''')


def format_sql_prompt(user_question: str):
    return TEXT2SQL_USER_MESSAGE.format(
        database_schema=DATABASE_SCHEMA,
        data_information=DATA_INFORMATION,
        user_question=user_question,
    )


ANALYST_SYSTEM_MESSAGE = (
    """You're an excellent data analyst that answers user's questions."""
)
ANALYST_USER_MESSAGE = dedent('''\
    Given the following sql query `SQL_QUERY` and its result `SQL_QUERY_RESULT`, answer the user's question `USER_QUESTION`.
    Give contextual information for the answer so that the user gets a better understanding.
    Use markdown to format your response.
    Your rseponse should be in the following format:
    """
    ## Answer
    <your final answer goes here>

    ## SQL QUERY
    ```sql
    <the sql query used to answer the question goes here>
    ```

    ## ## SQL RESULT
    ```sql
    <the result of running the sql query goes here>
    ```

    ## REASONING
    <the steps and reasoning used to analyze the question and write the sql query go here>
    """
    
    ## USER_QUESTION:
    """
    {user_question}
    """

    ## SQL_QUERY:
    """
    {sql_query}
    """

    ## SQL_QUERY_RESULT:
    {sql_result}

''')


def format_analyst_prompt(user_question: str, sql_query: str, sql_result: str):
    return ANALYST_USER_MESSAGE.format(
        user_question=user_question,
        sql_query=sql_query,
        sql_result=sql_result,
    )
