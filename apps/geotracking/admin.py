from django.contrib import admin

from .models import Visitor


class VisitorAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'ip_address', 'country', 'city', 'days_visited', 'created', 'updated']
    list_filter = 'country',
    search_fields = ['country', 'city']
    date_hierarchy = 'updated'
    empty_value_display = '-empty-'


# Register your models here.
admin.site.register(Visitor, VisitorAdmin)
