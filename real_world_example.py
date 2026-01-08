"""
Real-World Example: E-commerce Order Processing System
Demonstrates DI and IoC principles in a practical scenario
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict


# ============================================================================
# Abstractions (Interfaces) - Dependency Inversion Principle
# ============================================================================

class IPaymentGateway(ABC):
    """Payment processing abstraction"""
    
    @abstractmethod
    def process_payment(self, amount: float, card_info: dict) -> dict:
        pass


class IInventoryService(ABC):
    """Inventory management abstraction"""
    
    @abstractmethod
    def check_availability(self, product_id: str, quantity: int) -> bool:
        pass
    
    @abstractmethod
    def reserve_items(self, product_id: str, quantity: int) -> bool:
        pass


class INotificationService(ABC):
    """Notification abstraction"""
    
    @abstractmethod
    def send_notification(self, recipient: str, message: str):
        pass


class ILogger(ABC):
    """Logging abstraction"""
    
    @abstractmethod
    def log(self, level: str, message: str):
        pass


class IOrderRepository(ABC):
    """Order persistence abstraction"""
    
    @abstractmethod
    def save(self, order: dict) -> str:
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> dict:
        pass


# ============================================================================
# Concrete Implementations
# ============================================================================

class StripePaymentGateway(IPaymentGateway):
    """Stripe payment implementation"""
    
    def process_payment(self, amount: float, card_info: dict) -> dict:
        print(f"  💳 Processing ${amount:.2f} via Stripe")
        return {
            'success': True,
            'transaction_id': f"stripe_{hash(str(amount))}",
            'amount': amount
        }


class PayPalPaymentGateway(IPaymentGateway):
    """PayPal payment implementation"""
    
    def process_payment(self, amount: float, card_info: dict) -> dict:
        print(f"  💳 Processing ${amount:.2f} via PayPal")
        return {
            'success': True,
            'transaction_id': f"paypal_{hash(str(amount))}",
            'amount': amount
        }


class InventoryService(IInventoryService):
    """Inventory management implementation"""
    
    def __init__(self):
        self.stock = {
            'PROD001': 100,
            'PROD002': 50,
            'PROD003': 25
        }
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        available = self.stock.get(product_id, 0)
        is_available = available >= quantity
        print(f"  📦 Checking inventory for {product_id}: {available} available, need {quantity} -> {is_available}")
        return is_available
    
    def reserve_items(self, product_id: str, quantity: int) -> bool:
        if self.check_availability(product_id, quantity):
            self.stock[product_id] -= quantity
            print(f"  ✅ Reserved {quantity} of {product_id}")
            return True
        return False


class EmailNotificationService(INotificationService):
    """Email notification implementation"""
    
    def send_notification(self, recipient: str, message: str):
        print(f"  📧 Email to {recipient}: {message}")


class SMSNotificationService(INotificationService):
    """SMS notification implementation"""
    
    def send_notification(self, recipient: str, message: str):
        print(f"  📱 SMS to {recipient}: {message}")


class ConsoleLogger(ILogger):
    """Console logging implementation"""
    
    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [{timestamp}] [{level}] {message}")


class OrderRepository(IOrderRepository):
    """In-memory order repository"""
    
    def __init__(self):
        self.orders = {}
    
    def save(self, order: dict) -> str:
        order_id = order['order_id']
        self.orders[order_id] = order
        print(f"  💾 Order {order_id} saved to database")
        return order_id
    
    def find_by_id(self, order_id: str) -> dict:
        return self.orders.get(order_id)


# ============================================================================
# Business Logic with Dependency Injection
# ============================================================================

class OrderService:
    """
    Order processing service with injected dependencies
    
    This class demonstrates:
    - Constructor injection for required dependencies
    - Dependency on abstractions (IoC principle)
    - Single Responsibility (order processing logic only)
    - Open/Closed Principle (extend by injecting new implementations)
    """
    
    def __init__(
        self,
        payment_gateway: IPaymentGateway,
        inventory_service: IInventoryService,
        notification_service: INotificationService,
        logger: ILogger,
        order_repository: IOrderRepository
    ):
        # All dependencies injected via constructor
        self.payment_gateway = payment_gateway
        self.inventory_service = inventory_service
        self.notification_service = notification_service
        self.logger = logger
        self.order_repository = order_repository
    
    def process_order(self, customer: dict, items: List[dict], payment_info: dict) -> dict:
        """
        Process an order through the entire pipeline
        
        Benefits of DI:
        - Easy to test (inject mocks)
        - Easy to swap implementations (different payment gateways, etc.)
        - No tight coupling to concrete implementations
        """
        order_id = f"ORD{hash(str(datetime.now()))}"
        
        self.logger.log("INFO", f"Processing order {order_id} for {customer['name']}")
        
        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in items)
        
        # Check inventory
        self.logger.log("INFO", "Checking inventory availability")
        for item in items:
            if not self.inventory_service.check_availability(item['id'], item['quantity']):
                self.logger.log("ERROR", f"Item {item['id']} not available")
                self.notification_service.send_notification(
                    customer['email'],
                    f"Order {order_id} failed: Item not available"
                )
                return {'success': False, 'reason': 'Inventory unavailable'}
        
        # Reserve inventory
        self.logger.log("INFO", "Reserving inventory")
        for item in items:
            self.inventory_service.reserve_items(item['id'], item['quantity'])
        
        # Process payment
        self.logger.log("INFO", f"Processing payment of ${total:.2f}")
        payment_result = self.payment_gateway.process_payment(total, payment_info)
        
        if not payment_result['success']:
            self.logger.log("ERROR", "Payment failed")
            return {'success': False, 'reason': 'Payment failed'}
        
        # Save order
        order = {
            'order_id': order_id,
            'customer': customer,
            'items': items,
            'total': total,
            'payment': payment_result,
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        }
        
        self.order_repository.save(order)
        
        # Send confirmation
        self.notification_service.send_notification(
            customer['email'],
            f"Order {order_id} confirmed! Total: ${total:.2f}"
        )
        
        self.logger.log("INFO", f"Order {order_id} completed successfully")
        
        return {
            'success': True,
            'order_id': order_id,
            'total': total
        }


# ============================================================================
# Demonstration
# ============================================================================

def main():
    print("=" * 80)
    print("REAL-WORLD EXAMPLE: E-COMMERCE ORDER PROCESSING")
    print("Demonstrating Dependency Injection and Inversion of Control")
    print("=" * 80)
    print()
    
    # ========================================================================
    # Scenario 1: Using Stripe payment gateway
    # ========================================================================
    print("📦 SCENARIO 1: Order with Stripe Payment Gateway")
    print("-" * 80)
    
    order_service = OrderService(
        payment_gateway=StripePaymentGateway(),
        inventory_service=InventoryService(),
        notification_service=EmailNotificationService(),
        logger=ConsoleLogger(),
        order_repository=OrderRepository()
    )
    
    customer = {
        'name': 'Alice Johnson',
        'email': 'alice@example.com'
    }
    
    items = [
        {'id': 'PROD001', 'name': 'Laptop', 'price': 999.99, 'quantity': 1},
        {'id': 'PROD002', 'name': 'Mouse', 'price': 29.99, 'quantity': 2}
    ]
    
    result = order_service.process_order(customer, items, {'card': '1234'})
    print(f"\n✅ Result: {result}")
    print()
    
    # ========================================================================
    # Scenario 2: Using PayPal and SMS notifications
    # ========================================================================
    print("📦 SCENARIO 2: Order with PayPal and SMS Notifications")
    print("-" * 80)
    
    # Easy to swap implementations - just inject different services!
    order_service_2 = OrderService(
        payment_gateway=PayPalPaymentGateway(),  # Different payment gateway
        inventory_service=InventoryService(),
        notification_service=SMSNotificationService(),  # Different notification
        logger=ConsoleLogger(),
        order_repository=OrderRepository()
    )
    
    customer_2 = {
        'name': 'Bob Smith',
        'email': '+1234567890'
    }
    
    items_2 = [
        {'id': 'PROD003', 'name': 'Keyboard', 'price': 79.99, 'quantity': 1}
    ]
    
    result_2 = order_service_2.process_order(customer_2, items_2, {'paypal': 'bob@paypal.com'})
    print(f"\n✅ Result: {result_2}")
    print()
    
    # ========================================================================
    # Benefits Summary
    # ========================================================================
    print("=" * 80)
    print("🎯 BENEFITS DEMONSTRATED:")
    print("=" * 80)
    print()
    print("1. ✅ Dependency Injection:")
    print("   - OrderService depends on abstractions, not concrete classes")
    print("   - All dependencies injected via constructor")
    print("   - Easy to swap implementations (Stripe ↔ PayPal)")
    print()
    print("2. ✅ Inversion of Control:")
    print("   - OrderService doesn't create its dependencies")
    print("   - Framework/container controls dependency creation")
    print("   - Dependencies flow from outside")
    print()
    print("3. ✅ SOLID Principles:")
    print("   - Single Responsibility: Each class has one job")
    print("   - Open/Closed: Extend by adding new implementations")
    print("   - Liskov Substitution: Can swap implementations")
    print("   - Interface Segregation: Focused interfaces")
    print("   - Dependency Inversion: Depend on abstractions")
    print()
    print("4. ✅ Testability:")
    print("   - Easy to inject mock objects for testing")
    print("   - Can test OrderService in isolation")
    print("   - No need for real payment gateway in tests")
    print()
    print("5. ✅ Flexibility:")
    print("   - Switch payment gateways without code changes")
    print("   - Add new notification channels easily")
    print("   - Configure different setups for different environments")


if __name__ == "__main__":
    main()
