from rest_framework import serializers
from .models import Order, OrderItem, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity', 'notes']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'total_price', 'status', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        keep_items = []
        for item_data in items_data:
            if "id" in item_data:
                item = OrderItem.objects.get(id=item_data["id"])
                item.dish = item_data.get("dish", item.dish)
                item.quantity = item_data.get("quantity", item.quantity)
                item.notes = item_data.get("notes", item.notes)
                item.save()
                keep_items.append(item.id)
            else:
                OrderItem.objects.create(order=instance, **item_data)

        for item in instance.items.all():
            if item.id not in keep_items:
                item.delete()

        return instance