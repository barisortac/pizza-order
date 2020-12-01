from django.db import models

from pizzaorder.models import CoreModel, CoreEnum


class PizzaFlavorEnum(str, CoreEnum):
    MARGARITA = "margarita"
    MARINARA = "marinara"
    SALAMI = "salami"


class OrderStatusEnum(str, CoreEnum):
    RECEIVED = "received"
    PREPARING = "preparing"
    ON_DELIVERY = "on_delivery"
    DELIVERED = "delivered"
    CANCELED = "canceled"
    TURN_BACK = "turn_back"  # after delivery


class PizzaSizeEnum(str, CoreEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Order(CoreModel):
    status = models.CharField(
        max_length=50,
        verbose_name='Order Status',
        choices=OrderStatusEnum.choose_list(),
        db_index=True,
        default=OrderStatusEnum.RECEIVED,
    )
    customer = models.ForeignKey(
        "customer.Customer",
        verbose_name='Customer',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.customer.name} - {self.status}"

    def _json(self):
        tmp_json = super()._json()
        tmp_json['order_items'] = [i._json() for i in self.orderitem_set.all()]
        tmp_json['customer'] = self.customer._json()
        tmp_json['status'] = self.status

        return tmp_json


class OrderItem(CoreModel):
    order = models.ForeignKey(
        Order,
        verbose_name="Order",
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=0)
    pizza_size = models.CharField(
        max_length=50,
        verbose_name='Size',
        choices=PizzaSizeEnum.choose_list(),
        db_index=True
    )
    pizza = models.CharField(
        max_length=50,
        verbose_name='Pizza Flavor',
        choices=PizzaFlavorEnum.choose_list(),
        db_index=True
    )

    def __str__(self):
        return f"{self.id} - {self.pizza} - {self.pizza_size} - {self.quantity}"

    def _json(self):
        tmp_json = super()._json()
        tmp_json.pop('order')
        tmp_json['order_id'] = self.order.id

        return tmp_json
