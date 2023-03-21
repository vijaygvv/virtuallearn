from django.contrib import admin

# Register your models here.
from django.contrib import admin

from main.models import Post, Cart, Order

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass



