from django.db import models


class AuctionMonth(models.Model):
    days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    rate = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    created = models.DateTimeField()

    class Meta:
        verbose_name = "Auction for a Month"
        verbose_name_plural = "Auctions for a Month"


class AuctionTrimester(models.Model):
    days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    rate = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    created = models.DateTimeField()

    class Meta:
        verbose_name = "Auction for a Trimester"
        verbose_name_plural = "Auctions for a Trimester"


class AuctionSemester(models.Model):
    days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    rate = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    created = models.DateTimeField()

    class Meta:
        verbose_name = "Auction for a Semester"
        verbose_name_plural = "Auctions for a Semester"


class AuctionYear(models.Model):
    days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    rate = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    created = models.DateTimeField()

    class Meta:
        verbose_name = "Auction for a Year"
        verbose_name_plural = "Auctions for a Year"
