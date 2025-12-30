from django.db import models
from django.contrib.auth.models import User

class RestaurantTable(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    # Analytics: Is this a premium spot (window/VIP)?
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Table {self.table_number} ({self.capacity} seats)"

class Reservation(models.Model):
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    reservation_time = models.DateTimeField()
    # The 'Money Maker' field: How much revenue did this booking generate?
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Status for the Manager/Worker view
    is_confirmed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer_name} - Table {self.table.table_number}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    booking_time = models.DateTimeField()
    number_of_guests = models.IntegerField()
    
    # NEW: Status field for lifecycle management
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)