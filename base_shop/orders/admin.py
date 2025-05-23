from django.contrib import admin
from .models import Order,OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'get_items')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

    def get_items(self, obj):
        return ", ".join([f"{item.product.name} x{item.quantity}" for item in obj.items.all()])
    get_items.short_description = '購入商品'

admin.site.register(Order, OrderAdmin)
