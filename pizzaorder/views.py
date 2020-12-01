from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class MainView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        return Response({
            "name": "Pizza Order API"
        })

    def post(self, request):
        return Response({
            "version": "v1",
            "name": "I am an API!"
        })