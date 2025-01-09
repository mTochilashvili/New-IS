from django.test import TestCase
from .models import Order, OrderItem, Dish

class OrderModelTests(TestCase):

    def setUp(self):
        self.dish1 = Dish.objects.create(name='Dish 1', price=10.00)
        self.dish2 = Dish.objects.create(name='Dish 2', price=15.00)

    def test_order_creation(self):
        order = Order.objects.create(table_number=1)
        OrderItem.objects.create(order=order, dish=self.dish1, quantity=2)
        OrderItem.objects.create(order=order, dish=self.dish2, quantity=1)
        order.calculate_total_price()
        order.save()

        self.assertEqual(order.total_price, 35.00)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.items.count(), 2)

    def test_order_status_change(self):
        order = Order.objects.create(table_number=1)
        order.status = 'in_progress'
        order.save()

        self.assertEqual(order.status, 'in_progress')

    def test_total_price_calculation(self):
        order = Order.objects.create(table_number=1)
        OrderItem.objects.create(order=order, dish=self.dish1, quantity=3)
        OrderItem.objects.create(order=order, dish=self.dish2, quantity=2)
        order.calculate_total_price()
        order.save()

        self.assertEqual(order.total_price, 60.00)

    def test_dish_creation(self):
       dish = Dish.objects.create(name='Dish 3', price=20.00)
       self.assertEqual(dish.name, 'Dish 3')
       self.assertEqual(dish.price, 20.00)

    def test_order_item_quantity_update(self):
       order = Order.objects.create(table_number=1)
       item = OrderItem.objects.create(order=order, dish=self.dish1, quantity=1)
       item.quantity = 5
       item.save()
       self.assertEqual(item.quantity, 5)

    def test_order_item_deletion(self):
       order = Order.objects.create(table_number=1)
       item1 = OrderItem.objects.create(order=order, dish=self.dish1, quantity=2)
       item2 = OrderItem.objects.create(order=order, dish=self.dish2, quantity=1)
       order.calculate_total_price()
       self.assertEqual(order.total_price, 35.00)

       item1.delete()
       order.calculate_total_price()
       order.save()
       self.assertEqual(order.total_price, 15.00)
   

   

   

   
