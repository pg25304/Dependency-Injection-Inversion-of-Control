"""
Example: Interface Injection (Dependency Injection)
The dependency provides an injector method that will inject the dependency
into any client passed to it
"""

from abc import ABC, abstractmethod


class DatabaseConnectionInjector(ABC):
    """Interface that defines how to inject database connection"""
    
    @abstractmethod
    def inject_database(self, db_connection):
        pass


class DatabaseConnection:
    """Database connection that can be injected"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = True
    
    def query(self, sql):
        return f"Executing '{sql}' on database '{self.db_name}'"
    
    def close(self):
        self.connected = False
        print(f"Database connection to '{self.db_name}' closed")


class Repository(DatabaseConnectionInjector):
    """
    Repository implements the injector interface
    The interface defines HOW the dependency should be injected
    """
    
    def __init__(self):
        self.db = None
    
    def inject_database(self, db_connection: DatabaseConnection):
        """Implementation of the injection interface"""
        self.db = db_connection
        print(f"✅ Database '{db_connection.db_name}' injected into Repository")
    
    def find_all(self, table):
        if not self.db:
            raise RuntimeError("Database not injected!")
        
        result = self.db.query(f"SELECT * FROM {table}")
        print(f"📊 {result}")
        return result


class ServiceContainer:
    """
    Container that performs the injection based on the interface
    This is often part of a DI framework
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
    
    def inject_dependencies(self, client: DatabaseConnectionInjector):
        """
        Inject database into any client that implements the injector interface
        """
        client.inject_database(self.db_connection)


def main():
    print("=== Interface Injection (Dependency Injection) ===")
    print("The dependency provider defines the injection interface\n")
    
    # Setup
    print("1. Creating database connection:")
    db = DatabaseConnection("production_db")
    
    print("\n2. Creating service container:")
    container = ServiceContainer(db)
    
    print("\n3. Creating repository (without dependencies):")
    repo = Repository()
    
    print("\n4. Container injects dependencies:")
    container.inject_dependencies(repo)
    
    print("\n5. Using the repository with injected dependency:")
    repo.find_all("users")
    repo.find_all("products")
    
    print("\n✅ Interface Injection Benefits:")
    print("- Clear contract for how dependencies should be injected")
    print("- Useful in frameworks where the framework controls injection")
    print("- Client explicitly declares what it needs via interface")
    print("\n⚠️  Considerations:")
    print("- More complex than constructor or setter injection")
    print("- Less commonly used in modern applications")
    print("- Framework-dependent approach")


if __name__ == "__main__":
    main()
