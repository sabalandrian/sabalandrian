# In-Memory Database

The In-Memory Database is a Python class that simulates a basic in-memory database with support for transactions. It includes functionalities for setting values, retrieving values, deleting values, counting occurrences, and managing transactions.

## Features

- **SET:** Set the value associated with a given name in the database.
- **GET:** Retrieve the value for a specified name.
- **DELETE:** Delete the value associated with a specified name.
- **COUNT:** Return the count of distinct names that have a given value assigned to them.
- **BEGIN:** Start a new transaction.
- **ROLLBACK:** Rollback the most recent transaction.
- **COMMIT:** Commit all open transactions and make changes permanent.
- **END:** Exit the database.

## Usage
    # SET operation
    db.set_value("name", "foo")
    
    # GET operation
    value = db.get_value("name")
    print("GET name:", value)  # Output: GET name: foo

    # DELETE operation
    db.delete_value("name")

    # COUNT operation
    count = db.count_values("foo")
    print("COUNT foo:", count)  # Output: COUNT foo: 0
