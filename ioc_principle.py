"""
Inversion of Control (IoC) Principle
Demonstrates the concept of inverting control flow
"""


# ============================================================================
# BEFORE IoC: Traditional Control Flow
# ============================================================================

class TraditionalLibrary:
    """
    Traditional library where the library controls the flow
    The application code is called BY the library
    """
    
    def process_data(self, data):
        # Library controls everything
        print(f"Library processing: {data}")
        return data.upper()


def traditional_approach():
    """
    Traditional approach: Application controls the flow
    Application decides when to call library code
    """
    print("=== Traditional Approach (No IoC) ===")
    print("Application controls the flow\n")
    
    library = TraditionalLibrary()
    
    # Application decides what to do and when
    data = "hello"
    print(f"Application: Processing '{data}'")
    result = library.process_data(data)
    print(f"Application: Got result '{result}'")
    print()


# ============================================================================
# AFTER IoC: Inverted Control Flow
# ============================================================================

class Framework:
    """
    Framework with IoC: Framework controls the flow
    Application code is called BY the framework
    This is "Don't call us, we'll call you" principle
    """
    
    def __init__(self):
        self.handlers = []
    
    def register_handler(self, handler):
        """Application registers callbacks/handlers"""
        self.handlers.append(handler)
        print(f"✅ Handler registered: {handler.__name__}")
    
    def run(self, data):
        """
        Framework controls the flow
        Framework decides WHEN to call application code
        """
        print(f"\nFramework: Starting processing pipeline for '{data}'")
        
        result = data
        for handler in self.handlers:
            print(f"Framework: Calling {handler.__name__}")
            result = handler(result)
        
        print(f"Framework: Pipeline complete. Final result: '{result}'")
        return result


# Application-defined handlers (callbacks)
def uppercase_handler(data):
    """Application handler 1"""
    result = data.upper()
    print(f"  Handler: Uppercased to '{result}'")
    return result


def exclamation_handler(data):
    """Application handler 2"""
    result = data + "!!!"
    print(f"  Handler: Added exclamations '{result}'")
    return result


def ioc_approach():
    """
    IoC Approach: Framework controls the flow
    Application just registers handlers
    Framework decides when to call them
    """
    print("=== IoC Approach (Inversion of Control) ===")
    print("Framework controls the flow\n")
    
    framework = Framework()
    
    # Application registers its handlers (inversion of control)
    framework.register_handler(uppercase_handler)
    framework.register_handler(exclamation_handler)
    
    # Framework controls when handlers are called
    framework.run("hello")
    print()


# ============================================================================
# Real-world IoC Example: Event-Driven System
# ============================================================================

class EventBus:
    """
    Event-driven system demonstrating IoC
    The EventBus controls when event handlers are invoked
    """
    
    def __init__(self):
        self.listeners = {}
    
    def subscribe(self, event_type: str, handler):
        """Application subscribes to events"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(handler)
        print(f"✅ Subscribed to '{event_type}': {handler.__name__}")
    
    def publish(self, event_type: str, data):
        """
        Framework publishes events and calls handlers
        Control is inverted: framework calls application code
        """
        print(f"\n📢 Event published: '{event_type}' with data: {data}")
        
        if event_type in self.listeners:
            for handler in self.listeners[event_type]:
                print(f"  → Invoking {handler.__name__}")
                handler(data)


# Application event handlers
def on_user_created(user_data):
    print(f"    Handler: Sending welcome email to {user_data['email']}")


def on_user_created_log(user_data):
    print(f"    Handler: Logging user creation: {user_data['username']}")


def on_user_created_analytics(user_data):
    print(f"    Handler: Tracking user signup in analytics")


def event_driven_ioc():
    """Event-driven system demonstrating IoC"""
    print("=== Event-Driven IoC Example ===")
    print("EventBus controls when handlers are called\n")
    
    event_bus = EventBus()
    
    # Application subscribes to events (registers callbacks)
    event_bus.subscribe('user_created', on_user_created)
    event_bus.subscribe('user_created', on_user_created_log)
    event_bus.subscribe('user_created', on_user_created_analytics)
    
    # When event is published, EventBus controls the flow
    user_data = {'username': 'alice', 'email': 'alice@example.com'}
    event_bus.publish('user_created', user_data)
    print()


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 70)
    print("INVERSION OF CONTROL (IoC) DEMONSTRATION")
    print("=" * 70)
    print()
    
    traditional_approach()
    print("-" * 70)
    print()
    
    ioc_approach()
    print("-" * 70)
    print()
    
    event_driven_ioc()
    print("-" * 70)
    print()
    
    print("🎯 Key IoC Concepts:")
    print()
    print("1. Hollywood Principle: \"Don't call us, we'll call you\"")
    print("   - Application doesn't call framework")
    print("   - Framework calls application code")
    print()
    print("2. Control Flow Inversion:")
    print("   - Traditional: App → Library")
    print("   - IoC: Framework → App")
    print()
    print("3. Benefits:")
    print("   - Loose coupling between components")
    print("   - Framework manages lifecycle and flow")
    print("   - Application focuses on business logic")
    print("   - Easier to extend and maintain")
    print()
    print("4. Common IoC Patterns:")
    print("   - Dependency Injection (DI)")
    print("   - Event-driven architecture")
    print("   - Template method pattern")
    print("   - Strategy pattern")
    print("   - Plugin architectures")


if __name__ == "__main__":
    main()
