from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.filter(is_active=True)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        record = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(record)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            record = serializer.save()
            return Response(record._json(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        record = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            record, data=request.data, partial=True
        )

        if serializer.is_valid(raise_exception=True):
            record = serializer.save()
            return Response(record._json())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=pk)

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
