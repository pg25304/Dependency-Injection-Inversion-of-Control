# Dependency Injection & Inversion of Control

A comprehensive guide and implementation examples for **Dependency Injection (DI)** and **Inversion of Control (IoC)** design patterns in Python.

## 📚 What's Included

This repository contains practical examples demonstrating:

1. **Dependency Injection Patterns**
   - Constructor Injection
   - Setter Injection
   - Interface Injection

2. **Inversion of Control Concepts**
   - Control flow inversion
   - Event-driven architecture
   - Framework vs Library

3. **DI Container Implementation**
   - Service registration
   - Dependency resolution
   - Lifetime management (Singleton, Transient)

4. **Real-World Example**
   - E-commerce order processing system
   - Multiple implementations (Stripe, PayPal)
   - SOLID principles in action

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher

### Running the Examples

```bash
# Before DI - Demonstrates tight coupling
python before_di.py

# Constructor Injection - Most common DI pattern
python after_di_constructor.py

# Setter Injection - Optional dependencies
python after_di_setter.py

# Interface Injection - Framework-based DI
python after_di_interface.py

# IoC Principle - Control flow inversion
python ioc_principle.py

# DI Container - IoC Container implementation
python di_container.py

# Real-world example - E-commerce system
python real_world_example.py
```

## 📖 Concepts Explained

### Dependency Injection (DI)

**Dependency Injection** is a design pattern where dependencies are provided to a class from the outside rather than created inside the class.

**Benefits:**
- ✅ Loose coupling between components
- ✅ Easy to test (inject mocks)
- ✅ Easy to swap implementations
- ✅ Follows SOLID principles

**Example:**
```python
# ❌ Without DI (tight coupling)
class Service:
    def __init__(self):
        self.logger = ConsoleLogger()  # Hard-coded dependency

# ✅ With DI (loose coupling)
class Service:
    def __init__(self, logger: ILogger):
        self.logger = logger  # Injected dependency
```

### Inversion of Control (IoC)

**Inversion of Control** is a principle where the control flow is inverted - instead of your code calling a library, a framework calls your code.

**The Hollywood Principle:** "Don't call us, we'll call you"

**Example:**
```python
# Traditional: You call the library
result = library.process(data)

# IoC: Framework calls your code
framework.register_handler(my_handler)
framework.run()  # Framework decides when to call my_handler
```

### Three Types of Dependency Injection

#### 1. Constructor Injection
Dependencies are passed through the constructor.

```python
class UserService:
    def __init__(self, repository: IRepository, logger: ILogger):
        self.repository = repository
        self.logger = logger
```

**Best for:** Required dependencies that don't change

#### 2. Setter Injection
Dependencies are set through setter methods after object creation.

```python
class UserService:
    def set_logger(self, logger: ILogger):
        self.logger = logger
```

**Best for:** Optional dependencies or runtime configuration

#### 3. Interface Injection
The dependency provides an injection method.

```python
class Injectable(ABC):
    @abstractmethod
    def inject_dependency(self, dependency):
        pass

class UserService(Injectable):
    def inject_dependency(self, dependency):
        self.dependency = dependency
```

**Best for:** Framework-controlled injection

## 🏗️ File Structure

```
.
├── README.md                    # This file
├── before_di.py                 # Code without DI (tight coupling)
├── after_di_constructor.py      # Constructor injection example
├── after_di_setter.py           # Setter injection example
├── after_di_interface.py        # Interface injection example
├── ioc_principle.py             # IoC concept demonstration
├── di_container.py              # Simple DI container implementation
├── real_world_example.py        # E-commerce system example
└── test_examples.py             # Unit tests
```

## 🎯 Key Principles

### SOLID Principles

These examples demonstrate all SOLID principles:

1. **S - Single Responsibility Principle**
   - Each class has one job

2. **O - Open/Closed Principle**
   - Extend behavior by adding new implementations, not modifying existing code

3. **L - Liskov Substitution Principle**
   - Can swap implementations without breaking code

4. **I - Interface Segregation Principle**
   - Focused, specific interfaces

5. **D - Dependency Inversion Principle**
   - Depend on abstractions, not concrete implementations

### Design Patterns Used

- **Dependency Injection** - All examples
- **Strategy Pattern** - Different payment gateways
- **Observer Pattern** - Event-driven IoC
- **Repository Pattern** - Data access abstraction
- **Service Layer Pattern** - Business logic organization

## 🧪 Testing

Run the unit tests:

```bash
python test_examples.py
```

The tests demonstrate how DI makes code more testable by allowing mock dependencies to be injected.

## 📚 Learn More

### Recommended Reading
- [Dependency Injection Principles, Practices, and Patterns](https://www.manning.com/books/dependency-injection-principles-practices-patterns) by Steven van Deursen and Mark Seemann
- [Clean Architecture](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164) by Robert C. Martin
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

### Related Concepts
- **Dependency Inversion Principle (DIP)** - The "D" in SOLID
- **Inversion of Control (IoC)** - General principle
- **Service Locator Pattern** - Alternative to DI (less recommended)
- **Factory Pattern** - Creating objects
- **Abstract Factory Pattern** - Creating families of objects

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📝 License

This project is open source and available for educational purposes.

## 💡 Use Cases

### When to Use DI
- Building testable applications
- Creating modular, maintainable code
- Supporting multiple implementations
- Following SOLID principles
- Enterprise applications

### When to Use IoC Containers
- Large applications with many dependencies
- Plugin architectures
- Framework development
- Complex dependency graphs
- Automatic dependency resolution needed

## 🔍 Common Mistakes to Avoid

1. **Service Locator Anti-pattern**
   - Don't use a global service locator
   - Use constructor injection instead

2. **Over-engineering**
   - Don't add DI if you have simple, stable dependencies
   - Use pragmatically

3. **Hidden Dependencies**
   - Make dependencies explicit in constructors
   - Avoid property injection for required dependencies

4. **Circular Dependencies**
   - Refactor to break circular dependencies
   - Usually indicates design issues

## ✨ Summary

This repository provides a complete guide to Dependency Injection and Inversion of Control with:

- ✅ Clear before/after examples
- ✅ Multiple DI patterns demonstrated
- ✅ Working DI container implementation
- ✅ Real-world practical example
- ✅ Unit tests showing testability benefits
- ✅ Best practices and common pitfalls

Happy learning! 🎉