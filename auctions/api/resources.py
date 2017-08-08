from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from auctions.models import Auction
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication 
from django.conf import settings
from accounts.models import UserProfile


#curl --user "jide":"123" "http://127.0.0.1:8000/api/auction/?username=jide&api_key=049oflfdkd09dkdkjd93093jdjdid93hud8393"
#curl --dump-header - -H "Content-Type: application/json" -X POST --data '
#{"title": "This will prbbly be my lst post.", "pub_date": "2011-05-22T00:46:38", "slug": "another-post", "title": "Another Post", "user": "/api/v1/user/1/"}' 
#curl --dump-header - -H "Content-Type: application/json" -X POST --data '{bid_price: "124",bid_version: 6,current_winning_bidder: "tunde",description: "Hello you there",due: true, minimum_price: "120",previous_bid: "124",title: "Latest new one"}' "http://127.0.0.1:8000/api/auction/?username=jide&api_key=049oflfdkd09dkdkjd93093jdjdid93hud8393"
#http://localhost:8000/api/v1/entry/
#curl --dump-header - -H "Content-Type: application/json" -X POST --data '{bid_price: "33",bid_version: 2,current_winning_bidder: "",d_version: 0,deadline: "2015-11-08T17:13:12",description: "Boy boy",due: true,minimum_price: "0.01",previous_bid: "33",resource_uri: "",test_data: true,timestamp: "2015-11-08T16:59:10.906000",title: "Second auction by tunde again"}' "http://127.0.0.1:8000/api/auction/?username=jide&api_key=049oflfdkd09dkdkjd93093jdjdid93hud8393"


class AuctionResourceGet(ModelResource):
	#user = fields.ForeignKey(UserResource, 'user')
	class Meta:
	    queryset = Auction.objects.all()
	    allowed_methods = ['get']
	    excludes = ['active', 'adjucated', 'banned']
	    resource_name = 'auction'



class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        allowed_methods = ['get', 'post', 'delete', 'put']
        fields = ['language_preference']
       # authorization = Authorization()
        include_resource_uri = False
        include_absolute_url = False

class UserResource(ModelResource):
	#profile = fields.ToOneField('resources.UserProfileResource', attribute = 'userprofile', related_name='user', full=True, null=True)
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		allowed_methods = ['get', 'post']
		fields = ['username']
		filtering = {
		    'username': ALL,
					}
		#authorization = Authorization()

class AuctionResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	class Meta:
	    queryset = Auction.objects.all()
	    #allowed_methods = ['get']
	    resource_name = 'auction'
	    #authorization = Authorization()
	    filtering = {
            'user': ALL_WITH_RELATIONS,
        }