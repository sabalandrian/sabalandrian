class InMemoryDatabase:
    def __init__(self):
        # Initialize an empty database as a dictionary
        self.database = {}
        # Track the count of values for COUNT command
        self.counts = {}

    def set_value(self, name, value):
        # Sets the value associated with the given name in the database
        self.database[name] = value
        # Update the count for the value
        self.counts[value] = self.counts.get(value, 0) + 1

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

    def count_values(self, value):
        # Returns the count of names that have the given value assigned to them
        return self.counts.get(value, 0)
    
    def end_database(self):
        # Exits the database without automatically committing transactions
        print("Exiting the database.")
    
#Example 1: Basic Commands
if __name__ == "__main__":
    # Create an instance of the InMemoryDatabase
    db = InMemoryDatabase()

#Example 1: Basic Commands
    #1 GET a
    print("GET a:", db.get_value("a"))
    #2 SET a foo
    db.set_value("a", "foo")
    #3 SET b foo
    db.set_value("b", "foo")
    #4 COUNT foo
    print("COUNT foo:", db.count_values("foo"))
    #5 COUNT bar
    print("COUNT bar:", db.count_values("bar"))
    #6 DELETE a
    db.delete_value("a")
    #7 COUNT foo
    print("COUNT foo:", db.count_values("foo"))
    #8 SET b baz
    db.set_value("b", "baz")
    #9 COUNT foo
    print("COUNT foo:", db.count_values("foo"))
    #10 GET b
    print("GET b:", db.get_value("b"))
    #11 GET B
    print("GET B:", db.get_value("B"))
    #12 END
    db.end_database()