from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, \
    validate_order_status


class OrderViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer
    item_serializer_class = OrderItemSerializer
    queryset = Order.objects.filter(is_active=True)

    def list(self, request):
        if request.query_params:
            order_status = request.query_params.get("status")
            if order_status:
                validate_order_status(order_status=order_status)
                self.queryset = self.queryset.filter(status=order_status)

            customer_id = request.query_params.get("customer_id")
            if customer_id:
                self.queryset = self.queryset.filter(customer_id=customer_id)

        serializer = self.serializer_class(self.queryset, many=True)
        result = serializer.data

        return Response({
            "total_count": len(result),
            "data": result
        })

    def retrieve(self, request, pk=None):
        record = get_object_or_404(self.queryset, pk=pk, is_active=True)
        serializer = self.serializer_class(record)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        record = get_object_or_404(self.queryset, pk=pk, is_active=True)
        record.is_active = False
        record.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        if 'order_items' in request.data:
            return Response(
                {
                    "order_items": "Order items should be "
                                   "updated in /order/item/ endpoint!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        record = get_object_or_404(self.queryset, pk=pk, is_active=True)
        serializer = self.serializer_class(
            record, data=request.data, partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='item', url_name='add_item')
    def add_order_item(self, request, pk=None):
        record = get_object_or_404(self.queryset, pk=pk, is_active=True)
        validate_order_status(order_status=record.status, crud_order_item=True)
        serializer = self.item_serializer_class(record, data=request.data,
                                                many=True)
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()

            return Response(order._json(), status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.filter(is_active=True)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk, is_active=True)
        serializer = self.serializer_class(user)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        record = get_object_or_404(self.queryset, pk=pk, is_active=True)
        record.is_active = False
        record.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, *args, **kwargs):
        record = get_object_or_404(self.queryset, pk=pk, is_active=True)
        serializer = self.serializer_class(
            record, data=request.data, partial=True
        )
        validate_order_status(order_status=record.order.status)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
