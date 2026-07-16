from django.contrib import admin
from .models import Category, FoodItem, Order, OrderItem

# Purane waale registration ke niche ye jod do
admin.site.register(Category)
admin.site.register(FoodItem)

# Naye Order waale models
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'total_amount', 'is_delivered', 'created_at']
    list_filter = ['is_delivered', 'created_at']
    inlines = [OrderItemInline]