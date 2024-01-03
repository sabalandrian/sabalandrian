class InMemoryDatabase:
    def __init__(self):
        # Initialize an empty database as a dictionary
        self.database = {}
        # Track the count of values for COUNT command
        self.counts = {}
        # Track unique occurrences of each value
        self.unique_counts = {}

    def set_value(self, name, value):
        # Sets the value associated with the given name in the database
        self.database[name] = value
        # Update the count for the value
        self.counts[value] = self.counts.get(value, 0) + 1
        # Update unique counts for the value
        self.unique_counts[value] = 1

    def get_value(self, name):
        # Retrieves and returns the value for the specified name
        return self.database.get(name, "NULL")

    def delete_value(self, name):
        # Deletes the value associated with the specified name from the database
        if name in self.database:
            value = self.database[name]
            del self.database[name]
            # Update the count for the deleted value
            self.counts[value] -= 1
            if self.counts[value] == 0:
                del self.counts[value]
            # Update unique counts for the value
            del self.unique_counts[value]

    def count_values(self, value):
        # Returns the count of distinct names that have the given value assigned to them
        return self.unique_counts.get(value, 0)

    def end_database(self):
        # Exits the database without automatically committing transactions
        print("Exiting the database.")

# Example usage:
if __name__ == "__main__":
    # Create an instance of the InMemoryDatabase
    db = InMemoryDatabase()

    #1 SET a foo
    db.set_value("a", "foo")
    #2 SET a foo
    db.set_value("a", "foo")
    #3 COUNT foo
    print("COUNT foo:", db.count_values("foo")) 
    #4 GET a
    print("GET a:", db.get_value("a"))
    #5 DELETE a
    db.delete_value("a")
    #6 GET a
    print("GET a:", db.get_value("a"))
    #7 COUNT foo
    print("COUNT foo:", db.count_values("foo"))
    #8 END
    db.end_database()