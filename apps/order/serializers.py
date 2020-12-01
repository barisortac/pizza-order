from django.db import transaction
from rest_framework import serializers
from rest_framework.compat import MinValueValidator
from rest_framework.exceptions import NotAcceptable

from customer.models import Customer
from customer.serializers import validate_is_customer_active
from .models import Order, OrderItem, OrderStatusEnum


def validate_order_status(
        order_status: OrderStatusEnum,
        crud_order_item: bool = False
):
    if crud_order_item:
        status_enums = [
            OrderStatusEnum.RECEIVED.value,
            OrderStatusEnum.PREPARING.value
        ]
    else:
        status_enums = [i.value for i in OrderStatusEnum]

    if order_status not in status_enums:
        raise NotAcceptable(
            detail=f'Status or order should be in {status_enums}',
            code='bad_order_status'
        )


class OrderItemListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for item in validated_data:
            instance.orderitem_set.create(
                **item
            )

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)])
    queryset = OrderItem.objects.filter(is_active=True)

    class Meta:
        fields = ('id', 'pizza', 'quantity', 'pizza_size', 'is_active')
        model = OrderItem
        list_serializer_class = OrderItemListSerializer

    def to_representation(self, instance):
        data = super(OrderItemSerializer, self).to_representation(instance)
        order_id = instance.order.id
        data['order_id'] = order_id

        return data


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, source="orderitem_set")
    customer_id = serializers.IntegerField(
        validators=[validate_is_customer_active]
    )

    class Meta:
        fields = ('id', 'customer_id', 'order_items', 'status')
        model = Order

    def create(self, validated_data):
        with transaction.atomic():
            order_items = validated_data.pop('orderitem_set')
            order = Order.objects.create(**validated_data)

            for item in order_items:
                OrderItem.objects.create(
                    **item,
                    order_id=order.id
                )

            return order

    def to_representation(self, instance):
        data = super().to_representation(instance)
        customer = data.get('customer_id') and Customer.objects.get(
            id=data.get('customer_id')
        )
        if customer:
            data.pop('customer_id')
            data['customer'] = customer._json()

        # couldn't find a better way to filter is_active=True order_items
        # when find, this section will be updated
        order_items = data.get('order_items')
        _order_items = []
        if order_items:
            for item in order_items:
                if item.get("is_active"):
                    _order_items.append(item)
            data['order_items'] = _order_items

        return data
