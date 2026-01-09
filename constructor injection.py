"""Definition: Dependencies are provided through a class’s constructor.When to Use:
Most common and recommended approach.Ensures class is fully initialised with required dependencies."""
from abc import ABC, abstractmethod
from typing import Protocol
#Defines a Protocol (interface) for a Database object.
class Database(Protocol):
    def execute_query(self, query: str) -> list[dict]:#execute a SQL query and return results
        ... #The ... means nobody is provided for the method since it's just a protocol.

"""This is an *alternative* to `Protocol` that uses abstract base classes (ABC). - The key difference:
Child classes **must inherit** from `DatabaseABC`.The `@abstractmethod` decorator enforces that subclasses
implement the `execute` method.This is not used in the rest of the code, but it shows a common alternative."""
class DatabaseABC(ABC):
    @abstractmethod
    def execute_query(self, query: str) -> list[dict]:
        pass

#Concrete implementation of the Database protocol for a SQL database.
class PostgreSqlDatabase:
    def execute_query(self, query: str) -> list[dict]:
        # Simulate executing a SQL query and returning results.
        print(f"Executing query on PostgreSqlDatabase: {query}")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}] #mocked data

class MySqlDatabase:
    def execute_query(self, query: str) -> list[dict]:
        # Simulate executing a SQL query and returning results.
        print(f"Executing query on MySqlDatabase: {query}")
        return [{"id": 3, "name": "Charlie"}, {"id": 4, "name": "Diana"}] #mocked data

#Service class that depends on the Database protocol/dependency injection.
class UserService:
    def __init__(self, db: Database): #Constructor injection of the Database dependency.
        self._db = db

    def get_users(self) -> list[dict]:
        return self._db.execute_query("SELECT * FROM users;") #Fetch users from the database.

    def get_user_by_id(self, user_id: int) -> dict | None:
        results = self._db.execute_query(f"SELECT * FROM users WHERE id = {user_id};")
        #If the result contains at least one user, it returns the first user (result[0]); otherwise, it returns None.
        return results[0] if results else None

# Example usage:usage with different database implementations.
if __name__ == "__main__":
    #Production-PostgreSQL
    postgres_db = PostgreSqlDatabase() # Creates an instance of the `PostgreSQLDatabase` class.
    #Injects the `PostgreSQLDatabase` dependency into the `UserService` class via its constructor (`__init__`).
    user_service_postgres = UserService(postgres_db)
    #calls the `get_users` method of the `UserService` instance, which in turn calls
    # the `execute_query` method of the injected `PostgreSQLDatabase` instance to fetch user data.
    print(user_service_postgres.get_users())

    #Development-MySQL
    mysql_db = MySqlDatabase()
    user_service_mysql = UserService(mysql_db)
    print(user_service_mysql.get_users())
