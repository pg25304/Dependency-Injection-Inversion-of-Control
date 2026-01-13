"""
Example: Code WITHOUT Dependency Injection
This demonstrates tight coupling between classes
"""


class EmailService:
    """Concrete implementation of email sending"""
    
    def send_email(self, recipient, message):
        print(f"Sending email to {recipient}: {message}")


class NotificationService:
    """
    Problem: NotificationService is tightly coupled to EmailService
    - Hard to test (can't mock EmailService)
    - Hard to extend (can't switch to SMS without modifying this class)
    - Violates Open/Closed Principle
    """
    
    def __init__(self):
        # Direct instantiation creates tight coupling
        self.email_service = EmailService()
    
    def notify(self, recipient, message):
        self.email_service.send_email(recipient, message)


def main():
    print("=== Before Dependency Injection ===")
    print("Problem: Tight coupling between classes\n")
    
    notification_service = NotificationService()
    notification_service.notify("user@example.com", "Hello from tightly coupled code!")
    
    print("\nIssues:")
    print("1. NotificationService creates its own EmailService")
    print("2. Cannot easily switch to SMS or other notification methods")
    print("3. Hard to unit test NotificationService in isolation")
    print("4. Violates the Dependency Inversion Principle")


if __name__ == "__main__":
    main()
