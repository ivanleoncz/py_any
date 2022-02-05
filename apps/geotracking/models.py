from django.db import models

from django_countries.fields import CountryField


class Visitors(models.Model):

    ip = models.GenericIPAddressField()
    country = CountryField()
    city = models.CharField(max_length=64)
    amount_of_requests = models.PositiveIntegerField(default=1)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Visitors"
        verbose_name_plural = "Visitors"

    def __str__(self):
        return f"{self.ip} from {self.country.name} ({self.city})"
