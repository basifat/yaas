from django.conf.urls import patterns, include, url
from auctions import views
from django.contrib import admin
# from auctions.api import EntryResource
from tastypie.api import Api
from auctions.api.resources import AuctionResourceGet, AuctionResource, UserResource

auction_resource = AuctionResourceGet()

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(AuctionResourceGet())


v2_api = Api(api_name='v2')
v2_api.register(AuctionResource())
v2_api.register(UserResource())
#v1_api.register(UserResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yaas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include(v1_api.urls)),
    url(r'^api/', include(v2_api.urls)),
    url(r'^api/', include(auction_resource.urls)),
    url(r'^$', 'auctions.views.home', name='home'),
    url(r'^s/$', 'auctions.views.search', name='search'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', 'accounts.views.activation_view', name='activation_view'),
    url(r'^accounts/logout/$', 'accounts.views.logout_view', name='auth_logout'),
    url(r'^accounts/login/$', 'accounts.views.login_view', name='auth_login'),
    url(r'^accounts/register/$', 'accounts.views.registration_view', name='auth_register'),
    url(r'^accounts/modify/$', 'accounts.views.modify_view', name='modify_view'),
    url(r'^auctions/post/$', 'auctions.views.post_auction_view', name='post_auction_view'),
    url(r'^auctions/seller/(?P<slug>[\w-]+)/$', 'auctions.views.single_auction', name='single_auction'),
    url(r'^bid/(?P<slug>[\w-]+)/$', 'auctions.views.bid_on_auction', name='bid_on_auction'),
    url(r'^auctions/seller/$', 'auctions.views.seller_view', name='seller_view'),
)
