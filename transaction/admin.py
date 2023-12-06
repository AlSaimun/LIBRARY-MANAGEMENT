from django.contrib import admin
from .models import Borrow, PaymentGateWaySettings
# Register your models here.

@admin.register(Borrow)
class BookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date')
    fieldsets = (
        ('General', {
            'fields': ('user', 'book', 'return_date',),
        }),
    )
admin.site.register(PaymentGateWaySettings)