"""
Unit Tests Demonstrating How DI Improves Testability

These tests show how Dependency Injection makes it easy to:
- Inject mock objects for testing
- Test components in isolation
- Verify behavior without external dependencies
"""

import unittest
from unittest.mock import Mock, MagicMock
from typing import List


# Import the interfaces from real_world_example
from abc import ABC, abstractmethod


class IPaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float, card_info: dict) -> dict:
        pass


class IInventoryService(ABC):
    @abstractmethod
    def check_availability(self, product_id: str, quantity: int) -> bool:
        pass
    
    @abstractmethod
    def reserve_items(self, product_id: str, quantity: int) -> bool:
        pass


class INotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient: str, message: str):
        pass


class ILogger(ABC):
    @abstractmethod
    def log(self, level: str, message: str):
        pass


class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order: dict) -> str:
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> dict:
        pass


class OrderService:
    """The service we're testing (simplified version)"""
    
    def __init__(
        self,
        payment_gateway: IPaymentGateway,
        inventory_service: IInventoryService,
        notification_service: INotificationService,
        logger: ILogger,
        order_repository: IOrderRepository
    ):
        self.payment_gateway = payment_gateway
        self.inventory_service = inventory_service
        self.notification_service = notification_service
        self.logger = logger
        self.order_repository = order_repository
    
    def process_order(self, customer: dict, items: List[dict], payment_info: dict) -> dict:
        """Process an order"""
        order_id = "TEST_ORDER_001"
        
        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in items)
        
        # Check inventory
        for item in items:
            if not self.inventory_service.check_availability(item['id'], item['quantity']):
                self.logger.log("ERROR", f"Item {item['id']} not available")
                self.notification_service.send_notification(
                    customer['email'],
                    f"Order failed: Item not available"
                )
                return {'success': False, 'reason': 'Inventory unavailable'}
        
        # Reserve inventory
        for item in items:
            self.inventory_service.reserve_items(item['id'], item['quantity'])
        
        # Process payment
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
            'status': 'completed'
        }
        
        self.order_repository.save(order)
        self.notification_service.send_notification(
            customer['email'],
            f"Order {order_id} confirmed! Total: ${total:.2f}"
        )
        self.logger.log("INFO", f"Order {order_id} completed successfully")
        
        return {'success': True, 'order_id': order_id, 'total': total}


# ============================================================================
# Unit Tests - Demonstrating DI Benefits
# ============================================================================

class TestOrderServiceWithDI(unittest.TestCase):
    """
    Tests demonstrating how DI makes testing easier
    
    Benefits:
    - Can inject mock objects
    - Test in isolation without real services
    - Verify interactions with dependencies
    - Fast, reliable tests (no network, database, etc.)
    """
    
    def setUp(self):
        """Create mock dependencies before each test"""
        self.mock_payment = Mock(spec=IPaymentGateway)
        self.mock_inventory = Mock(spec=IInventoryService)
        self.mock_notification = Mock(spec=INotificationService)
        self.mock_logger = Mock(spec=ILogger)
        self.mock_repository = Mock(spec=IOrderRepository)
        
        # Create service with mock dependencies (Dependency Injection!)
        self.order_service = OrderService(
            payment_gateway=self.mock_payment,
            inventory_service=self.mock_inventory,
            notification_service=self.mock_notification,
            logger=self.mock_logger,
            order_repository=self.mock_repository
        )
        
        # Test data
        self.customer = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        self.items = [
            {'id': 'PROD001', 'name': 'Test Product', 'price': 99.99, 'quantity': 1}
        ]
    
    def test_successful_order_processing(self):
        """Test successful order with all dependencies mocked"""
        # Arrange - Configure mocks
        self.mock_inventory.check_availability.return_value = True
        self.mock_inventory.reserve_items.return_value = True
        self.mock_payment.process_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN123',
            'amount': 99.99
        }
        
        # Act - Process order
        result = self.order_service.process_order(
            self.customer,
            self.items,
            {'card': '1234'}
        )
        
        # Assert - Verify result
        self.assertTrue(result['success'])
        self.assertEqual(result['order_id'], 'TEST_ORDER_001')
        self.assertEqual(result['total'], 99.99)
        
        # Verify interactions with dependencies
        self.mock_inventory.check_availability.assert_called_once_with('PROD001', 1)
        self.mock_inventory.reserve_items.assert_called_once_with('PROD001', 1)
        self.mock_payment.process_payment.assert_called_once()
        self.mock_repository.save.assert_called_once()
        
        # Verify notification was sent
        self.mock_notification.send_notification.assert_called_once()
        call_args = self.mock_notification.send_notification.call_args
        self.assertEqual(call_args[0][0], 'test@example.com')
        self.assertIn('confirmed', call_args[0][1])
    
    def test_order_fails_when_inventory_unavailable(self):
        """Test order failure when item is out of stock"""
        # Arrange - Mock inventory as unavailable
        self.mock_inventory.check_availability.return_value = False
        
        # Act
        result = self.order_service.process_order(
            self.customer,
            self.items,
            {'card': '1234'}
        )
        
        # Assert - Order should fail
        self.assertFalse(result['success'])
        self.assertEqual(result['reason'], 'Inventory unavailable')
        
        # Verify payment was NOT attempted
        self.mock_payment.process_payment.assert_not_called()
        
        # Verify error notification was sent
        self.mock_notification.send_notification.assert_called_once()
        call_args = self.mock_notification.send_notification.call_args
        self.assertIn('failed', call_args[0][1])
    
    def test_order_fails_when_payment_fails(self):
        """Test order failure when payment is declined"""
        # Arrange
        self.mock_inventory.check_availability.return_value = True
        self.mock_inventory.reserve_items.return_value = True
        self.mock_payment.process_payment.return_value = {
            'success': False,
            'error': 'Card declined'
        }
        
        # Act
        result = self.order_service.process_order(
            self.customer,
            self.items,
            {'card': '1234'}
        )
        
        # Assert
        self.assertFalse(result['success'])
        self.assertEqual(result['reason'], 'Payment failed')
        
        # Verify order was NOT saved
        self.mock_repository.save.assert_not_called()
    
    def test_logging_behavior(self):
        """Test that appropriate logging occurs"""
        # Arrange
        self.mock_inventory.check_availability.return_value = True
        self.mock_inventory.reserve_items.return_value = True
        self.mock_payment.process_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN123'
        }
        
        # Act
        self.order_service.process_order(self.customer, self.items, {'card': '1234'})
        
        # Assert - Verify logging calls
        self.assertTrue(self.mock_logger.log.called)
        
        # Check that INFO logs were made
        log_calls = self.mock_logger.log.call_args_list
        info_logs = [call for call in log_calls if call[0][0] == 'INFO']
        self.assertGreater(len(info_logs), 0)


# ============================================================================
# Comparison: Testing WITHOUT DI (Difficult)
# ============================================================================

class TightlyCoupledOrderService:
    """
    Example of a service WITHOUT DI - hard to test!
    
    Problems:
    - Creates its own dependencies
    - Can't inject mocks
    - Tests would hit real services
    - Slow, unreliable tests
    """
    
    def __init__(self):
        # Hard-coded dependencies - can't be mocked!
        from real_world_example import (
            StripePaymentGateway,
            InventoryService,
            EmailNotificationService,
            ConsoleLogger,
            OrderRepository
        )
        
        self.payment_gateway = StripePaymentGateway()
        self.inventory_service = InventoryService()
        self.notification_service = EmailNotificationService()
        self.logger = ConsoleLogger()
        self.order_repository = OrderRepository()
    
    def process_order(self, customer, items, payment_info):
        # Same logic, but can't test easily!
        pass


class TestTightlyCoupledService(unittest.TestCase):
    """
    Tests for tightly coupled service
    
    Problems demonstrated:
    - Can't inject mocks
    - Would need real Stripe account for tests
    - Would need real database
    - Tests are slow and unreliable
    - Can't verify interactions
    """
    
    def test_this_would_be_difficult(self):
        """
        This test would be problematic because:
        1. Can't mock dependencies
        2. Would hit real services
        3. Need network, database, etc.
        4. Slow and flaky
        5. Can't verify internal behavior
        """
        # This is why DI is important for testing!
        pass


# ============================================================================
# Main
# ============================================================================

def main():
    """Run the tests"""
    print("=" * 80)
    print("UNIT TESTS - Demonstrating DI Benefits for Testing")
    print("=" * 80)
    print()
    
    # Run the tests
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    print()
    print("=" * 80)
    print("KEY TAKEAWAYS:")
    print("=" * 80)
    print()
    print("✅ WITH Dependency Injection:")
    print("   - Can inject mock objects")
    print("   - Test components in isolation")
    print("   - Fast, reliable tests (no network/database)")
    print("   - Can verify interactions with dependencies")
    print("   - Easy to test edge cases and failures")
    print()
    print("❌ WITHOUT Dependency Injection:")
    print("   - Hard-coded dependencies")
    print("   - Tests hit real services")
    print("   - Slow, flaky tests")
    print("   - Need real credentials/infrastructure")
    print("   - Difficult to test error scenarios")
    print()
    print("🎯 Conclusion: DI makes code significantly more testable!")


if __name__ == '__main__':
    main()
