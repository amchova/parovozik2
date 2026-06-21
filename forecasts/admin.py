from django.contrib import admin
from .models import Forecast, Purchase

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'region', 'price', 'created_at', 'author')
    list_filter = ('category', 'region')
    search_fields = ('title', 'description')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'forecast', 'purchased_at')
    list_filter = ('purchased_at',)