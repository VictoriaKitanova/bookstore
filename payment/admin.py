"""
Register the model on the admin section thing
"""
from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


class OrderItemInline(admin.StackedInline):
    """
    Create an orderItem inline
    """
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    """
    Extend our Order model
    """
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user",
              "full_name",
              "email",
              "shipping_address",
              "amount_paid",
              "date_ordered",
              "shipped",
              "date_shipped"
            ]
    inlines = [OrderItemInline]

# Unregister order model
admin.site.unregister(Order)

# Re-register our order and orderadmin models
admin.site.register(Order, OrderAdmin)
