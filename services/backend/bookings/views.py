from rest_framework import generics
from .models import RestaurantTable, Booking
from .serializers import RestaurantTableSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAdminUser

class RestaurantTableList(generics.ListCreateAPIView):
    queryset = RestaurantTable.objects.all()
    serializer_class = RestaurantTableSerializer
    permission_classes = [IsAuthenticated]

class UserDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(my_bookings, many=True)
        
        return Response({
            "role": "Customer",
            "my_reservations": serializer.data,
            "loyalty_points": my_bookings.count() 
        })


class ManagerDashboard(APIView):
    permission_classes = [IsAdminUser] 

    def get(self, request):
        all_bookings = Booking.objects.all().count()
        pending = Booking.objects.filter(status='PENDING').count()
        
        return Response({
            "role": "Manager",
            "total_reservations": all_bookings,
            "needs_attention": pending
        })

class CapacitySummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_tables = RestaurantTable.objects.count()
        # Count only active (not cancelled) bookings for today
        booked_today = Booking.objects.filter(
            booking_time__date=timezone.now().date()
        ).exclude(status='CANCELLED').count()

        return Response({
            "total_capacity": total_tables,
            "current_bookings": booked_today,
            "available_tables": total_tables - booked_today
        })

class BookingListCreate(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optimization: Only fetch bookings for the authenticated user
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Association: Link the new booking to the user making the request
        serializer.save(user=self.request.user)