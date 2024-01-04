class InMemoryDatabase:
    def __init__(self):
        # Initialize an empty database as a dictionary
        self.database = {}
        # Track the count of values for COUNT command
        self.counts = {}
        # Track unique occurrences of each value
        self.unique_counts = {}
        # Track transactions and changes
        self.transactions = []
        self.current_transaction = []

    def set_value(self, name, value):
        # Sets the value associated with the given name in the database
        if not self.in_transaction():
            self.begin_transaction()
        self.current_transaction.append(("SET", name, value))
        # Update the count for the value
        self.counts[value] = self.counts.get(value, 0) + 1
        # Update unique counts for the value
        self.unique_counts[value] = 1

    def get_value(self, name):
        # Retrieves and returns the value for the specified name
        # Check if the name is in the current transaction
        for action, current_name, value in reversed(self.current_transaction):
            if action == "SET" and current_name == name:
                return value
            elif action == "DELETE" and current_name == name:
                return "NULL"  # The name is deleted in the current transaction
        # Check if the name is in the main database
        return self.database.get(name, "NULL")

    def delete_value(self, name):
        # Deletes the value associated with the specified name from the database
        if not self.in_transaction():
            self.begin_transaction()
        if name in self.database:
            value = self.database[name]
            self.current_transaction.append(("DELETE", name, value))
            # Update the count for the deleted value
            self.counts[value] -= 1
            if self.counts[value] == 0:
                del self.counts[value]
            # Update unique counts for the value
            del self.unique_counts[value]

    def count_values(self, value):
        # Returns the count of distinct names that have the given value assigned to them
        return self.unique_counts.get(value, 0)

    def begin_transaction(self):
        # Starts a new transaction
        self.transactions.append(self.current_transaction.copy())
        self.current_transaction = []

    def rollback_transaction(self):
        # Rolls back the most recent transaction
        if not self.transactions:
            print("TRANSACTION NOT FOUND.")
            return

        rolled_back_transaction = self.transactions.pop()
        for action, name, value in rolled_back_transaction:
            if action == "SET":
                # Rollback the value only if it exists in the database
                if name in self.database:
                    del self.database[name]
                    self.counts[value] -= 1
                    if self.counts[value] == 0:
                        del self.counts[value]
                    del self.unique_counts[value]
            elif action == "DELETE":
                self.database[name] = value
                self.counts[value] += 1
                self.unique_counts[value] = 1

    def commit_transaction(self):
        # Commits all open transactions and makes changes permanent
        for transaction in self.transactions:
            for action, name, value in transaction:
                if action == "SET":
                    self.database[name] = value
                    self.counts[value] += 1
                    self.unique_counts[value] = 1
                elif action == "DELETE":
                    del self.database[name]
                    self.counts[value] -= 1
                    if self.counts[value] == 0:
                        del self.counts[value]
                    del self.unique_counts[value]
        self.transactions = []
        self.current_transaction = []

    def end_database(self):
        # Exits the database without automatically committing transactions
        print("Exiting the database.")

    def in_transaction(self):
        # Checks if currently in a transaction
        return bool(self.current_transaction or self.transactions)

# Example 4: Nested Transactions with COMMIT
if __name__ == "__main__":
    # Create an instance of the InMemoryDatabase
    db = InMemoryDatabase()

    # 1 SET a foo
    db.set_value("a", "foo")
    # 2 SET b baz
    db.set_value("a", "baz")
    # 3 BEGIN
    db.begin_transaction()
    # 4 GET a
    print("GET a:", db.get_value("a"))
    # 5 SET a bar
    db.set_value("a", "bar")
    # 6 COUNT bar
    print("COUNT bar:", db.count_values("bar"))
    # 7 BEGIN
    db.begin_transaction()
    # 8 COUNT bar
    print("COUNT bar:", db.count_values("bar"))
    # 9 DELETE a
    db.delete_value("a")
    # 10 GET a
    print("GET a:", db.get_value("a"))
    # 11 COUNT bar
    print("COUNT bar:", db.count_values("bar"))
    # 12 ROLLBACK
    db.rollback_transaction()
    # 13 GET a
    print("GET a:", db.get_value("a"))
    # 14 COUNT bar
    print("COUNT bar:", db.count_values("bar"))
    # 15 COMMIT
    db.commit_transaction()
    # 16 GET a
    print("GET a:", db.get_value("a"))
    # 17 GET b
    print("GET a:", db.get_value("b"))
    # 18 END
    db.end_database()
    