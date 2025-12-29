from rest_framework import generics
from .models import RestaurantTable
from .serializers import RestaurantTableSerializer
from rest_framework.permissions import IsAuthenticated

class RestaurantTableList(generics.ListCreateAPIView):
    queryset = RestaurantTable.objects.all()
    serializer_class = RestaurantTableSerializer
    permission_classes = [IsAuthenticated]