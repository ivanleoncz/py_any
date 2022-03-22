from django.db import models

from django_countries.fields import CountryField


class Visitor(models.Model):

    ip = models.GenericIPAddressField()
    country = CountryField()
    city = models.CharField(max_length=64)
    amount_of_requests = models.PositiveIntegerField(default=0)
    last_request = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visitors"
        verbose_name_plural = "Visitors"

    def __str__(self):
        return f"{self.ip} from {self.country.name} ({self.city}): " \
               f"{self.amount_of_requests} requests (last was {self.last_request}"

    def save(self, *args, **kwargs):
        self.amount_of_requests += 1
        super().save(*args, **kwargs)