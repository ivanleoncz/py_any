from django.contrib import admin

from .models import AuctionMonth, AuctionTrimester, AuctionSemester, AuctionYear

admin.site.register(AuctionMonth)
admin.site.register(AuctionTrimester)
admin.site.register(AuctionSemester)
admin.site.register(AuctionYear)