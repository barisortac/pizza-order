from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customer.models import Customer
from .models import Order, PizzaFlavorEnum, PizzaSizeEnum, OrderStatusEnum, \
    OrderItem
from .serializers import OrderSerializer


class OrderViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(
            name="John Doe",
            email="example@example.com",
            phone="9012345678"
        )
        cls.inactive_customer = Customer.objects.create(
            name="John the Inactive",
            email="inactive@example.com",
            phone="9012345578"
        )
        cls.inactive_customer.is_active = False
        cls.inactive_customer.save()
        cls.orders = [
            Order.objects.create(customer=cls.customer) for _ in range(15)
        ]
        cls.order = cls.orders[0]
        cls.order_items_payload = [
            {
                "pizza": [i.value for i in PizzaFlavorEnum][0],
                "quantity": 12,
                "pizza_size": [i.value for i in PizzaSizeEnum][0],
            },
        ]

        cls.order_items = []
        for order in cls.orders:
            item = OrderItem.objects.create(
                order=order, **cls.order_items_payload[0]
            )
            cls.order_items.append(item)

        cls.valid_order_payload = {
            "customer_id": cls.customer.id,
            "order_items": cls.order_items_payload
        }
        cls.invalid_order_payload = {
            "order_items": cls.order_items_payload
        }
        cls.valid_order_with_inactive_customer = {
            "customer_id": cls.inactive_customer.id,
            "order_items": cls.order_items_payload
        }

    def test_can_browse_all_orders(self):
        response = self.client.get(reverse("api:order-list"))

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.orders), len(response.data['data']))

        for order in self.orders:
            self.assertIn(
                OrderSerializer(instance=order).data,
                response.data['data']
            )

    def test_can_read_a_specific_order(self):
        response = self.client.get(
            reverse("api:order-detail", args=[self.order.id])
        )

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(
            OrderSerializer(instance=self.order).data,
            response.data
        )

    def test_can_add_order(self):
        response = self.client.post(
            reverse("api:order-list"),
            self.valid_order_payload,
            format="json"
        )

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_cannot_add_invalid_order(self):
        response = self.client.post(
            reverse("api:order-list"),
            self.invalid_order_payload,
            format="json"
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_cannot_add_order_with_inactive_customer(self):
        response = self.client.post(
            reverse("api:order-list"),
            self.valid_order_with_inactive_customer,
            format="json"
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_add_order_item(self):
        response = self.client.put(
            reverse("api:order-add_item", args=[self.order.id]),
            self.order_items_payload,
            format="json"
        )
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_delete_order(self):
        order = self.orders[10]
        order_id = order.id
        response = self.client.delete(
            reverse("api:order-detail", args=[order_id]),
        )

        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(
            reverse("api:order-detail", args=[order_id])
        )

        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_cannot_add_order_item_if_order_status_not_suitable(self):
        self.order.status = OrderStatusEnum.DELIVERED
        self.order.save()
        response = self.client.put(
            reverse("api:order-add_item", args=[self.order.id]),
            self.order_items_payload,
            format="json"
        )
        self.assertEquals(status.HTTP_406_NOT_ACCEPTABLE, response.status_code)

    def test_delete_order_item(self):
        order = [i for i in self.orders if i.orderitem_set.count() > 0][0]
        _item_filter = order.orderitem_set.filter(is_active=True)
        order_item = _item_filter.first()
        initial_item_count = _item_filter.count()
        response = self.client.delete(
            reverse("api:item-detail", args=[order_item.id]),
        )
        last_item_count = _item_filter.count()

        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEquals(last_item_count, initial_item_count - 1)
