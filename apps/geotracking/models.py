
from django.db import models

from django_countries.fields import CountryField


class Visitor(models.Model):

    device_id = models.CharField(max_length=32,
                                 help_text="Token generated upon request and stored as Persistent Cookie")
    ip_address = models.GenericIPAddressField()
    referrer = models.CharField(null=True, blank=True, max_length=256,
                                help_text="Page which served the link to the request.")
    country = CountryField(null=True)
    city = models.CharField(null=True, max_length=64)
    days_visited = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"

    def __str__(self):
        return f"{self.device_id} : {self.ip_address}"
