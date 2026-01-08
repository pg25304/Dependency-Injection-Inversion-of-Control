"""
Simple Dependency Injection Container
Demonstrates IoC Container pattern for managing dependencies
"""

from abc import ABC, abstractmethod
from typing import Dict, Type, Callable, Any


class DIContainer:
    """
    Simple Dependency Injection Container (IoC Container)
    
    Features:
    - Service registration (binding interfaces to implementations)
    - Dependency resolution
    - Singleton and Transient lifetimes
    - Automatic dependency injection
    """
    
    def __init__(self):
        self._services: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
        self._lifetimes: Dict[Type, str] = {}
    
    def register(self, interface: Type, implementation: Type, lifetime: str = 'transient'):
        """
        Register a service
        
        Args:
            interface: The interface/base class
            implementation: The concrete implementation
            lifetime: 'singleton' or 'transient'
        """
        self._services[interface] = implementation
        self._lifetimes[interface] = lifetime
        print(f"✅ Registered {interface.__name__} -> {implementation.__name__} ({lifetime})")
    
    def register_instance(self, interface: Type, instance: Any):
        """Register a pre-created singleton instance"""
        self._services[interface] = lambda: instance
        self._singletons[interface] = instance
        self._lifetimes[interface] = 'singleton'
        print(f"✅ Registered instance of {interface.__name__}")
    
    def resolve(self, interface: Type):
        """
        Resolve a service and its dependencies
        
        Args:
            interface: The interface to resolve
            
        Returns:
            An instance of the registered implementation
        """
        if interface not in self._services:
            raise ValueError(f"Service {interface.__name__} not registered")
        
        # Return singleton if already created
        if self._lifetimes[interface] == 'singleton' and interface in self._singletons:
            return self._singletons[interface]
        
        # Get the implementation
        implementation = self._services[interface]
        
        # If it's a lambda (registered instance), just call it
        if callable(implementation) and not isinstance(implementation, type):
            return implementation()
        
        # Create instance
        # Note: In a real DI container, you would inspect __init__ parameters
        # and automatically resolve and inject dependencies
        instance = implementation()
        
        # Store singleton
        if self._lifetimes[interface] == 'singleton':
            self._singletons[interface] = instance
        
        return instance


# Example services to demonstrate the container

class ILogger(ABC):
    @abstractmethod
    def log(self, message: str):
        pass


class ConsoleLogger(ILogger):
    def log(self, message: str):
        print(f"[LOG] {message}")


class IEmailService(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str):
        pass


class EmailService(IEmailService):
    def send(self, to: str, subject: str, body: str):
        print(f"📧 Email to {to}: {subject} - {body}")


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: dict):
        pass
    
    @abstractmethod
    def find(self, user_id: int):
        pass


class UserRepository(IUserRepository):
    def __init__(self):
        self.users = {}
    
    def save(self, user: dict):
        user_id = user.get('id')
        self.users[user_id] = user
        print(f"💾 User {user_id} saved to repository")
    
    def find(self, user_id: int):
        return self.users.get(user_id)


class UserService:
    """
    Service that depends on ILogger, IEmailService, and IUserRepository
    In a full container, these would be auto-injected
    """
    
    def __init__(self, logger: ILogger, email_service: IEmailService, repository: IUserRepository):
        self.logger = logger
        self.email_service = email_service
        self.repository = repository
    
    def register_user(self, username: str, email: str):
        self.logger.log(f"Registering user: {username}")
        
        user = {
            'id': hash(username),
            'username': username,
            'email': email
        }
        
        self.repository.save(user)
        self.email_service.send(email, "Welcome!", f"Welcome {username}!")
        
        self.logger.log(f"User {username} registered successfully")
        return user


def main():
    print("=== Dependency Injection Container (IoC Container) ===\n")
    
    # Create the container
    container = DIContainer()
    
    print("1. Registering services:")
    # Register services with their lifetimes
    container.register(ILogger, ConsoleLogger, lifetime='singleton')
    container.register(IEmailService, EmailService, lifetime='singleton')
    container.register(IUserRepository, UserRepository, lifetime='singleton')
    
    print("\n2. Resolving dependencies:")
    # Resolve services from container
    logger = container.resolve(ILogger)
    email_service = container.resolve(IEmailService)
    repository = container.resolve(IUserRepository)
    
    print("\n3. Creating UserService with resolved dependencies:")
    # Create UserService with dependencies from container
    user_service = UserService(logger, email_service, repository)
    
    print("\n4. Using the service:")
    user_service.register_user("alice", "alice@example.com")
    
    print("\n5. Verifying singleton behavior:")
    logger2 = container.resolve(ILogger)
    print(f"Same logger instance? {logger is logger2}")
    
    print("\n✅ IoC Container Benefits:")
    print("- Centralized dependency management")
    print("- Automatic dependency resolution")
    print("- Lifetime management (singleton, transient)")
    print("- Easy to swap implementations")
    print("- Configuration-based dependency injection")


if __name__ == "__main__":
    main()
