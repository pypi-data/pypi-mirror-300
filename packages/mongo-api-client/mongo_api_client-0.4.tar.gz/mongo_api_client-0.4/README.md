# MongoApiClient Python Client

## Description

MongoApiClient is a Python library for interacting with MongoDB databases. It provides an easy-to-use interface for performing various database operations.

## Installation

To install MongoApiClient, you can use pip:
```py -m pip install mongo-api-client```


## Building Queries
- Building Queries
- When building queries with MongoApiClient, you can use various operators and sorting options:
## Operators: 
- MongoApiClient supports the following operators:
    - "=": Equal to
    - "!=": Not equal to
    - "<": Less than
    - "<=": Less than or equal to
    - ">": Greater than
    - ">=": Greater than or equal to
    - "like": Similar to (using the MongoDB $regex operator)
- Sorting: You can specify the sorting order as "asc" (ascending) or  - "desc" (descending) using the sort_by() method.

## Usage
Here's an example of how to use MongoApiClient to interact with MongoDB:

```python
from mongo_api_client import MongoApiClient

# Initialize MongoApiClient with connection details
database = MongoApiClient(
    server_ip= "your-server-ip", 
    server_port=9875, 
    scheme= "http")
```
### Retriving data
```python
# Example: Perform a query
result = database\
    .from_db("isac-division2-bot")\
    .from_table("account-versioning")\
    .where("username", "like",  "paul")
    .where("age", ">", 10)
    .per_page(2)\
    .page(1)\
    .sort_by("created_at","desc")\
    .select() # or .find()

print(result)
```
### Retriving first result
```python
# Example: Perform a query
result = database\
    .from_db("isac-division2-bot")\
    .from_table("account-versioning")\
    .where("username", "like",  "paul")
    .where("age", ">", 10)\
    .sort_by("created_at","desc")\
    .get()\
    .first()
print(result)
```

### Counting results
```python
# Example: Perform a query
result = database\
    .from_db("isac-division2-bot")\
    .from_table("account-versioning")\
    .where("username", "like",  "paul")
    .where("age", ">", 10)\
    .sort_by("created_at","desc")\
    .count()
print(result)
```

### Retriving data by ID
```python
# Example: Perform a query
result = database\
    .from_db("isac-division2-bot")\
    .from_table("account-versioning")\
    .select_by_id("your-mongo-id") # or find_by_id("your-mongo-id")

print(result)
```

### Inserting Data
```python
# Example: Insert data into a table
testData = [
    {
    'username' : 'hoewea2342we',
    'age' : 21,
    'occupations' : ['software engineer', 'musician']
},
    {
    'username' : 'hoeweaasdeasdwe',
    'age' : 44,
    'occupations' : ['software engineer', 'musician']
},
    {
    'username' : 'hoewea111we',
    'age' : 23,
    'occupations' : ['software engineer', 'musician']
}
]

print(
    database
    .into_db('my-test-database')
    .into_table('my-test-table-2')
    .insert(testData)
    )

# Example: Insert data into a table if the condition 
# is NOT MET
print(
    database
    .into_db("my-test-database")
    .into_table("my-test-table")
    .where("username", "!=", "mathew")
    .insert_if_not_exists(testData))
```
### Updating Data
```python
# Example: Update data based on conditions
print(
    database
    .into_db("my-test-database")
    .into_table("my-test-table")
    .where("username", "=", "hoewea111we")
    .update({"username": "alexanderdth123", "age": 99})
    )

# Example: Update data by ID
print(
    database
    .from_db("my-test-database")
    .from_table("my-test-table")
    .update_by_id("665103498e80ecc6f646d6c5", {"username" : "popeye1212"})
    )
```

### Deleting Data
```python
# Example: Delete data from a table by ID
print(
    database
    .from_db("my-test-database")
    .from_table("my-test-table")
    .delete_by_id("665104538e80ecc6f646d6cd")
    )

# Example: Delete a database
print(database.delete_database("alexanderdth"))

# Example: Delete tables in a database
print(database.delete_tables_in_db("my-test-database", "my-test-table-2"))

# Example: Delete data from a table based on conditions
print(
    database
    .from_db("my-test-database")
    .from_table("my-test-table")
    .or_where("username", "=", "hoeweaasdeasdwe")
    .or_where("age", "=", 21)
    .delete()
    )
```

### Other Operations

```python
# List tables in a database
print(database.list_tables_in_db("my-db-name"))
# List databases
print(database.list_databases())
```