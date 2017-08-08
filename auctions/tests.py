from django.test import TestCase
from .models import Auction
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from .forms import AuctionForm
import pytz 
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .views import post_auction_view

#User = get_user_model()
#u = User.objects.get(username='babatunde', email='babatunde.asifat@gmail.com', password='yaas')

#from .views import MyView, my_view


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.get(username='jide')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = post_auction_view(request)
        # Use this syntax for class-based views.
        #response = MyView.as_view()(request)
        self.assertEqual(response.status_code, 200)



# class AuctionTest(TestCase):

# 	def create_auction(self, title="Auction_1", description="Latest auction", minimum_price=200.20, 
# 		deadline= (datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(seconds = 259200)), seller = u):

# 		return Auction.objects.create(title=title, description=description, minimum_price=minimum_price, 
# 			deadline=deadline,
# 		 timestamp= datetime.utcnow().replace(tzinfo=pytz.utc))

# 	def test_auction_creation(self):
# 		auction = self.create_auction()
# 		self.assertTrue(isinstance(auction, Auction))
# 		self.assertEqual(auction.__unicode__(), auction.title)


# # models test
# class WhateverTest(TestCase):

#     def create_whatever(self, title="only a test", body="yes, this is only a test"):
#         return Whatever.objects.create(title=title, body=body, created_at=timezone.now())

#     def test_whatever_creation(self):
#         w = self.create_whatever()
#         self.assertTrue(isinstance(w, Whatever))
#         self.assertEqual(w.__unicode__(), w.title)