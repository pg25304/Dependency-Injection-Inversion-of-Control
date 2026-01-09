from abc import ABC, abstractmethod
from typing import Protocol


# Interface definition (using Protocol - Python 3.8+)
class Notifier(Protocol):
    def send(self, message: str) -> bool:
        """Send notification and return success status"""
        ...


# Alternative abstract base class version
class NotifierABC(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        """Send notification and return success status"""
        pass


# Concrete implementations
class EmailNotifier:
    def send(self, message: str) -> bool:
        print(f"Sending email: {message}")
        return True  # Mock success


class SMSNotifier:
    def send(self, message: str) -> bool:
        print(f"Sending SMS: {message}")
        return True  # Mock success


class PushNotifier:
    def send(self, message: str) -> bool:
        print(f"Sending push notification: {message}")
        return True


# Service class with setter injection
class NotificationService:
    def __init__(self):
        self._notifier: Notifier | None = None

    def set_notifier(self, notifier: Notifier) -> None:
        """Dependency injection via setter method"""
        self._notifier = notifier

    def send_notification(self, message: str) -> bool:
        if not self._notifier:
            raise ValueError("No notifier configured")
        return self._notifier.send(message)


# Usage examples
if __name__ == "__main__":
    service = NotificationService()

    # Use email notifier
    service.set_notifier(EmailNotifier())
    service.send_notification("Hello via Email!")

    # Switch to SMS notifier
    service.set_notifier(SMSNotifier())
    service.send_notification("Hello via SMS!")

    # Switch to push notifier
    service.set_notifier(PushNotifier())
    service.send_notification("Hello via Push!")