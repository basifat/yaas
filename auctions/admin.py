from django.contrib import admin
from .models import Auction, Bid
from kombu.transport.django import models as kombu_models

# Register your models here.

def ban_auction(modeladmin, request, queryset):
	for obj in queryset:
		if obj.active == True and obj.banned == False:
			#obj.update(banned=True, active=False)
			obj.banned = True
			obj.active = False
			obj.save()
    		#queryset.update(banned=True, active=False)
ban_auction.short_description = "Mark selected Auctions as Banned"
	
#
class AuctionAdmin(admin.ModelAdmin):
	list_display = ['title', 'description', 'bid_price']
	ordering = ['bid_price']
	prepopulated_fields ={"slug":("title",)}
	actions = [ban_auction]
	
	class Meta:
			model = Auction

class BidAdmin(admin.ModelAdmin):
	list_display = ['auction', 'user', 'bid_amount']
	ordering = ['auction']
	
	class Meta:
			model = Bid

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(kombu_models.Message)

