from rest_framework import serializers
from .models import RestaurantTable
from .models import Booking

class RestaurantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTable
        fields = ['id', 'table_number', 'capacity', 'is_premium', 'image']
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'table', 'booking_time', 'number_of_guests', 'status']
        read_only_fields = ['user', 'status']

    def validate(self, data):
        # Technical Logic: Check if the table is already booked for this specific time
        # This is a 'Filter' query in the Django ORM
        existing_bookings = Booking.objects.filter(
            table=data['table'],
            booking_time=data['booking_time']
        ).exclude(status='CANCELLED')

        if existing_bookings.exists():
            raise serializers.ValidationError("This table is already reserved for the selected time.")
        
        return data