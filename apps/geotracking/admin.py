from django.contrib import admin

from .models import Visitor


class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip', 'country', 'city', 'amount_of_requests', 'last_request']
    list_filter = 'country',
    search_fields = ['country', 'city']
    date_hierarchy = 'last_request'
    empty_value_display = '-empty-'


# Register your models here.
admin.site.register(Visitor, VisitorAdmin)
