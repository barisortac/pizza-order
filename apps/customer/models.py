from django.db import models

from pizzaorder.models import CoreModel


class Customer(CoreModel):
    name = models.CharField(
        max_length=100,
        verbose_name='Name',
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='Email',
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Phone',
        null=True,
        blank=True
    )
