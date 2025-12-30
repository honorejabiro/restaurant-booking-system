from rest_framework import generics
from .models import RestaurantTable, Booking
from .serializers import RestaurantTableSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated

class RestaurantTableList(generics.ListCreateAPIView):
    queryset = RestaurantTable.objects.all()
    serializer_class = RestaurantTableSerializer
    permission_classes = [IsAuthenticated]

class BookingListCreate(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optimization: Only fetch bookings for the authenticated user
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Association: Link the new booking to the user making the request
        serializer.save(user=self.request.user)