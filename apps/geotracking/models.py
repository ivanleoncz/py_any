from django.db import models

from django_countries.fields import CountryField


class Visitor(models.Model):

    ip = models.GenericIPAddressField()
    country = CountryField(null=True)
    city = models.CharField(null=True, max_length=64)
    amount_of_requests = models.PositiveIntegerField(default=0)
    last_request = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"

    def __str__(self):
        return f"{self.ip} from {self.country.name} ({self.city}): " \
               f"{self.amount_of_requests} requests (last was {self.last_request})"
