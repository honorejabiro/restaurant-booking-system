from django.contrib import admin
from .models import RestaurantTable

@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_premium')
    list_filter = ('is_premium',)
