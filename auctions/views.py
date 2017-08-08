from .forms import AuctionForm, AuctionUpdateForm, AuctionBidForm, ConfirmAuctionUpdateForm,ConfirmPostAuctionForm
from django.contrib import messages
from django.utils.translation import ugettext as _ 
from .models import Auction, Bid
from decimal import Decimal
from .description import GetAllAuction
import datetime
import pytz 
from django.shortcuts import render,HttpResponseRedirect,Http404
from django.template.defaultfilters import slugify
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
#from .translation import welcome_translated
from django.utils import translation,timezone
#from django.utils.translation import ugettext
#from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import PyExchangeRates
import json,ast
from django.core.mail import send_mail, send_mass_mail
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core import serializers
from django.contrib.auth import get_user_model
from auctions.process_bidders import get_bidder_email
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from django.utils.timezone import activate


# Create an 'Exchange' object, this holds all the information about the currencies and exchange rates
# Get a free API key from https://openexchangerates.org/signup/free
exchange = PyExchangeRates.Exchange('7481ea7007ab448cbc7d40094e1225a6') 
from django.utils.decorators import decorator_from_middleware

User = get_user_model()
#activate(settings.TIME_ZONE)

# Create your views here.
#onchange='if(this.value != 0) { this.form.submit(); }'
def home(request):	
	if request.user.is_authenticated():
		lang = request.session.get('lang')
		lang_in_db = ""
		try:
			profile = UserProfile.objects.get(user=request.user)
			#get_profile, create_profile1 = UserProfile.objects.get_or_create(user=request.user)
			if lang and lang != None:
				profile.language_preference = lang
	 			profile.save()	
				lang_in_db = profile.language_preference
			else:
				pass
	 	except UserProfile.DoesNotExist:
			profile = UserProfile.objects.create(user=request.user)
			if lang and lang != None:
				profile.language_preference = lang
				profile.save()	
				lang_in_db = profile.language_preference
			else:
				pass
		lang_in_db = profile.language_preference
		translation.activate(lang_in_db)
	auctions = Auction.objects.select_for_update()
	request.session['cur'] = "EUR"
	currency = request.session.get('cur')
	if request.POST.get("cur") == "eur":
		request.session['cur'] = "EUR"
		currency = request.session.get('cur')
	if request.POST.get("cur") == "usd":
		request.session['cur'] = "USD"
		currency = request.session.get('cur')
	if request.POST.get("cur") == "aud":
		request.session['cur'] = "AUD"
		currency = request.session.get('cur')
	if request.POST.get("lang") == "swedish":
		translation.activate('sv')
		request.session['lang'] = "sv"
		lang = request.session.get('lang')
		page_message = "Your language choice is Swedish until you logout"
		messages.success(request, _(page_message))
	if request.POST.get("lang") == "english":
		translation.activate('en-us')
		request.session['lang'] = "en-us"
		lang = request.session.get('lang')
		page_message = "Your language choice is English until you logout"
		messages.success(request, page_message)	
	template = 'auctions/list.html'
	context = {'auction': auctions, 'currency':currency,}
	return render(request,template,context)


def post_auction_view(request):
	#go back to emailing user after auction is posted later
	#before user is redirected, add a message to show user they are redirected as they are not logged in
	if request.user.is_authenticated():
		auction_obj = Auction()
		form = AuctionForm((request.POST or None), instance = auction_obj)
		btn  = "Submit"
		#system_deadline = timezone.now()+timedelta(days = 2, hours=23, minutes=58) datetime.utcnow().replace(tzinfo=pytz.utc)
		#print "timezone is", timezone.now()
		#system_deadline = datetime.utcnow().replace(tzinfo=pytz.utc)+timedelta(days = 2, hours=23, minutes=58) 
		system_deadline = datetime.utcnow().replace(tzinfo=pytz.utc)+timedelta(days = 2, hours=23, minutes=59) 
		if form.is_valid():
			new_auction = form.save(commit = False)
			#form = ConfirmPostAuctionForm((request.POST or None), instance = auction_obj)
			user_deadline = new_auction.deadline
			diff = user_deadline - system_deadline
			minutes = divmod(diff.days * 86400 + diff.seconds, 60)
			minutes_left = minutes[0]
			#new_user.first_name = "Justin" this is where you can do stuff with the model form
			#new_auction.deadline = default=datetime.now()+timedelta(hours=72)
			if minutes_left >= 0:
				new_auction.previous_bid = new_auction.minimum_price
				new_auction.seller = request.user
				new_auction.slug = slugify(new_auction.title)
				#new_auction.save()
				#messages.success(request, "Auction posted Successfully")
				#return HttpResponseRedirect("/")
			else:
				messages.success(request, "More than a minute has passed since you wanted to post this auction. Deadline must be at least 3 days from today. Reload the page or add future date")
				context = {
					"form":form,
					"submit_btn": btn,
					"deadline": user_deadline
						}
				return render(request, "form.html", context)
			form = ConfirmPostAuctionForm((request.POST or None), instance=auction_obj)
			option = request.POST.get('option', '')
			request.session['option_form'] = "option_form"
			if option == "Yes":
				new_auction.save()
				#new_user.d_version = new_user.d_version + 1
				form.save()
				#del request.session['option_form']
				page_message = "You have successful posted a new auction description"
				context = {"page_message": page_message}
				return render(request, "auctions/modify_complete.html", context)
			if option=="No":
				page_message = "You canceled, auction not posted"
				del request.session['option_form']
				context = {"page_message": page_message}
				return render(request, "auctions/modify_complete.html", context)
			sure = "Are you sure want to post this auction? Click Yes to continue"
			context = {
			"form":form, "submit_btn": btn, "confirm_message":sure
			}
			return render(request, "form.html", context)


		context = {
					"form":form,
					"submit_btn": btn,
						}
		return render(request, "form.html", context)

	else:
		return HttpResponseRedirect('%s'%(reverse("auth_login")))

def bid_on_auction(request, slug):	
	if request.user.is_authenticated():
		#try:
			auction = Auction.objects.get(slug=slug)
			bidders = Bid.objects.all().filter(auction=auction)
			#print "all bidders are", bidders
			seller_email = auction.seller.email

			if auction.banned:
				page_message = "You cannot bid on Banned Auctions"
				context = {"page_message": page_message}
				return render(request, "auctions/modify_complete.html", context)
			else:
				bid = Bid() #New bid object
				bid.auction = auction #Assign auction to bid
				description = auction.description
				minimum_price = auction.minimum_price
				version = auction.d_version # version no for description
				version_for_bid = auction.bid_version# version no for bid
				old_version = request.session.get('d_version') #get from request the present version
				previous_bid_version = request.session.get('bid_version') #get from request the present version
				if auction.seller != request.user and not auction.banned:
					form = AuctionBidForm((request.POST or None), instance=auction)
					request.session['d_version'] = version
					request.session['bid_version'] = version_for_bid #Save 1 in session
					btn  = "Bid"
					if form.is_valid():
							bidding = form.save(commit = False)
							latest_version = bidding.d_version
							if old_version == None:
								pass
							if old_version != latest_version:
								description = auction.description
								messages.success(request, "Auction description has been updated since the last time")
								context = {
								"form":form, "submit_btn": btn, "description":description,
									}
								return render(request, "form.html", context)
							
							latest_bid_version = bidding.bid_version
							if previous_bid_version != latest_bid_version:
								previous_bid = auction.previous_bid
								#previous_bid = bid.previous_bid
								messages.success(request, "New bids since the last time. Please resubmit a bid higher than (EUR)")
								context = {
									"form":form, "submit_btn": btn, "minimum_price":previous_bid,
									}
								return render(request, "form.html", context)
							else:
								if ((bidding.bid_price>auction.previous_bid) == True) and (bidding.bid_price>auction.minimum_price):
									deadline = bidding.deadline
									now = datetime.utcnow().replace(tzinfo=pytz.utc)
									diff = (deadline - now)
									print "diff is", diff
									minutes = divmod(diff.days * 86400 + diff.seconds, 60)
									minutes_left = minutes[0]
									print "minutes left", minutes_left
									new_deadline = deadline+timedelta(days = 0, hours = 0, minutes =5)
									bidding.previous_bid = bidding.bid_price
									bid.user = request.user
									bid.bid_amount = bidding.bid_price
									#bid.previous_bid = bidding.bid_price
									if minutes_left <= 5:
										bidding.deadline = deadline+timedelta(days = 0, hours = 0, minutes =5)
										pass
									bidding.save()
									bidding.bid_version = bidding.bid_version + 1
									form.save()
								elif (bidding.bid_price<=auction.minimum_price):
									minimum_price = auction.minimum_price
									#previous_bid = bid.previous_bid
									messages.success(request, "New bids must be greater than Minimum price of (EUR)")
									context = {
									"form":form, "submit_btn": btn,"minimum_price":minimum_price,
									}
									return render(request, "form.html", context)
								else:
									previous_bid = auction.previous_bid
									messages.success(request, "New bids must be greater than the previous bid of (EUR)")
									context = {
									"form":form, "submit_btn": btn,"minimum_price":previous_bid,
									}
									return render(request, "form.html", context)
							bid.save()
							#Get winning bidder here and the list of all bidders on the current auction
							winner, list_of_bidders_email = get_bidder_email(bidders, seller_email)
							auction.current_winning_bidder = winner.username
							auction.save()

							page_message = "You have placed a new bid"
							context = {"page_message": page_message}
							return render(request, "auctions/modify_complete.html", context)
					context = {
					"form":form, "submit_btn": btn, "description":description,
						}
					return render(request, "form.html", context)
				else:
					page_message = "You cannot bid on own auctions"
					context = {"page_message": page_message}
					return render(request, "auctions/modify_complete.html", context)
		#except :
				#raise Http404
	else:
		return HttpResponseRedirect('%s'%(reverse("auth_login")))

def single_auction(request, slug):

	try:
		auction = Auction.objects.get(slug = slug)
		form = AuctionUpdateForm((request.POST or None), instance=auction)
		btn  = "Modify Auction"
		#request.session['slug_for_description'] = slug
		if form.is_valid():
					new_user = form.save(commit = False)
					#Get the current description version
					form = ConfirmAuctionUpdateForm((request.POST or None), instance=auction)
					option = request.POST.get('option', '')
					request.session['option_form'] = "option_form"
					if option == "Yes":
						new_user.save()
						new_user.d_version = new_user.d_version + 1
						form.save()
						del request.session['option_form']
						page_message = "You have successful updated your auction description"
						context = {"page_message": page_message}
						return render(request, "auctions/modify_complete.html", context)
					if option=="No":
						page_message = "You canceled, description not modified"
						del request.session['option_form']
						context = {"page_message": page_message}
						return render(request, "auctions/modify_complete.html", context)
				#else:
				# 	page_message = "You decided to cancel"
				# 	context = {"page_message": page_message}
				# 	return render(request, "auctions/modify_complete.html", context)
		sure = "Are you sure want to update description? Click Yes to continue"
		context = {
		"form":form, "submit_btn": btn, "confirm_message":sure
			}
		return render(request, "form.html", context)
	except :
		raise Http404


def seller_view(request):
	if request.user.is_authenticated():
		seller = request.user
		auction = Auction.objects.all().filter(seller = seller)
		template = 'auctions/seller.html'
		context = {'auction': auction}
		return render(request,template,context)
	else:
		return HttpResponseRedirect('%s'%(reverse("auth_login")))


def search(request):
	try:
		q = request.GET.get('q')
	except:
			q = None
	if q:
		auctions = Auction.objects.filter(title__icontains = q)
		#auctions = auctions.values_list('title', flat=True)
		context ={'query': q, 'auction': auctions}
		template = 'auctions/results.html'
	else:	
		template = 'auctions/list.html'
		context ={}
	return render(request, template, context)


def translate_view(request):
	print translation.get_language()
	#output = ugettext("Welcome to my site.")
	#Set language for user session
	if request.POST.get("lang") == "swedish":
		translation.activate('sv')
		request.session['lang'] = "sv"
		print request.session.get('lang')
		page_message = ("Your language preference is now swedish")
		print page_message
		context = {"page_message": page_message}
		return render(request, "auctions/translation.html", context)
	if request.POST.get("lang") == "english":
		translation.activate('en-us')
		request.session['lang'] = "en-us"
		print request.session.get('lang')
		page_message = "Your language preference is now English"
		context = {"page_message": page_message}
		return render(request, "auctions/translation.html", context)

