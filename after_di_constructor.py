"""
Example: Constructor Injection (Dependency Injection)
This demonstrates loose coupling through constructor-based DI
"""

from abc import ABC, abstractmethod


class MessageService(ABC):
    """
    Abstract interface (Dependency Inversion Principle)
    High-level modules depend on abstractions, not concrete implementations
    """
    
    @abstractmethod
    def send_message(self, recipient, message):
        pass


class EmailService(MessageService):
    """Concrete implementation for email"""
    
    def send_message(self, recipient, message):
        print(f"📧 Email sent to {recipient}: {message}")


class SMSService(MessageService):
    """Concrete implementation for SMS"""
    
    def send_message(self, recipient, message):
        print(f"📱 SMS sent to {recipient}: {message}")


class PushNotificationService(MessageService):
    """Concrete implementation for push notifications"""
    
    def send_message(self, recipient, message):
        print(f"🔔 Push notification sent to {recipient}: {message}")


class NotificationService:
    """
    Benefits of Constructor Injection:
    - Loosely coupled to MessageService interface
    - Easy to test (inject mock implementations)
    - Easy to extend (new message services can be added)
    - Follows Dependency Inversion Principle
    - Dependencies are explicit and immutable
    """
    
    def __init__(self, message_service: MessageService):
        # Dependency injected through constructor
        self.message_service = message_service
    
    def notify(self, recipient, message):
        self.message_service.send_message(recipient, message)


def main():
    print("=== Constructor Injection (Dependency Injection) ===")
    print("Benefits: Loose coupling, testability, flexibility\n")
    
    # Inject EmailService
    print("1. Using Email Service:")
    email_notifier = NotificationService(EmailService())
    email_notifier.notify("user@example.com", "Hello via email!")
    
    # Inject SMSService (no code change in NotificationService!)
    print("\n2. Using SMS Service:")
    sms_notifier = NotificationService(SMSService())
    sms_notifier.notify("+1234567890", "Hello via SMS!")
    
    # Inject PushNotificationService
    print("\n3. Using Push Notification Service:")
    push_notifier = NotificationService(PushNotificationService())
    push_notifier.notify("user_device_id", "Hello via push!")
    
    print("\n✅ Benefits achieved:")
    print("- NotificationService doesn't know about concrete implementations")
    print("- Easy to swap implementations without modifying NotificationService")
    print("- Easy to test with mock implementations")
    print("- Follows SOLID principles (especially D - Dependency Inversion)")


if __name__ == "__main__":
    main()
