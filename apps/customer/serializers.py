from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Customer


def validate_is_customer_active(pk):
    customer = get_object_or_404(queryset=Customer.objects.all(), pk=pk)
    if not customer.is_active:
        raise serializers.ValidationError("The customer is inactive!")
    return customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'phone', 'email')
        model = Customer
