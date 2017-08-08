# from __future__ import absolute_import

# from celery.task.schedules import crontab
# from celery.decorators import periodic_task

# from yaas.celery import app
# from auctions.models import Auction, Bid



# #@periodic_task(run_every=(crontab(minute='*/1')), name="add", ignore_result=True)
# @app.task
# def add(x, y):
#     return x + y


# @app.task
# def mul(x, y):
#     return x * y


# @app.task
# def xsum(numbers):
#     return sum(numbers)


# @app.task
# def choose_winner():
# 	winner_amount = 0
# 	auctions = Auction.objects.filter(due = True)
# 	for due_auction in auctions:
# 		slug = due_auction.slug
# 		bids = Bid.objects.filter(auction__slug = slug)
# 		for items in bids:
# 			if items.bid_amount>winner_amount:
# 				winner_amount = items.bid_amount
# 				winner = items.user
# 				winner_email = items.user.email
# 			print "Bids are", items
# 		print winner_amount
# 		print winner
# 		print winner_email
# 		print "End of first item"
# 		winner_amount = 0
# 		due_auction.adjucated = True
# 		due_auction.save()
# 	return winner_email, winner_amount
