"""
Example: Setter Injection (Dependency Injection)
Dependencies are injected through setter methods after object creation
"""

from abc import ABC, abstractmethod


class Logger(ABC):
    """Abstract logger interface"""
    
    @abstractmethod
    def log(self, message):
        pass


class ConsoleLogger(Logger):
    """Log to console"""
    
    def log(self, message):
        print(f"[CONSOLE] {message}")


class FileLogger(Logger):
    """Log to file"""
    
    def __init__(self, filename):
        self.filename = filename
    
    def log(self, message):
        print(f"[FILE:{self.filename}] {message}")


class UserService:
    """
    Setter Injection allows optional dependencies or runtime changes
    
    Use cases:
    - Optional dependencies (can work without logger)
    - Dependencies that might change during object lifetime
    - Circular dependencies (though better avoided)
    """
    
    def __init__(self):
        self.logger = None
    
    def set_logger(self, logger: Logger):
        """Inject dependency through setter method"""
        self.logger = logger
    
    def create_user(self, username):
        if self.logger:
            self.logger.log(f"Creating user: {username}")
        
        # User creation logic
        print(f"✅ User '{username}' created successfully")
        
        if self.logger:
            self.logger.log(f"User {username} creation completed")
        
        return {"username": username, "id": hash(username)}


def main():
    print("=== Setter Injection (Dependency Injection) ===")
    print("Use case: Optional dependencies or runtime configuration\n")
    
    # 1. Without logger (optional dependency)
    print("1. UserService without logger:")
    user_service = UserService()
    user_service.create_user("alice")
    
    # 2. Inject ConsoleLogger via setter
    print("\n2. UserService with ConsoleLogger:")
    user_service.set_logger(ConsoleLogger())
    user_service.create_user("bob")
    
    # 3. Change logger at runtime (Setter injection advantage)
    print("\n3. Switching to FileLogger at runtime:")
    user_service.set_logger(FileLogger("users.log"))
    user_service.create_user("charlie")
    
    print("\n✅ Setter Injection Benefits:")
    print("- Dependencies are optional")
    print("- Can change dependencies at runtime")
    print("- Allows circular dependencies (though not recommended)")
    print("\n⚠️  Considerations:")
    print("- Dependencies can be null (need null checks)")
    print("- Less explicit than constructor injection")
    print("- Object might be in incomplete state before setter is called")


if __name__ == "__main__":
    main()
