from django.conf.urls import patterns, include, url
from .api import iOSLoginBAWF

urlpatterns = patterns('',
                       url(r'^ios/data/', 'bayareaweddingfairs_tickets.api.TicketsAPI', name='TicketsAPI_ajax'),
                       url(r'^ios/login/', iOSLoginBAWF, name='iOSLoginBAWF_ajax'),
                       url(r'^main/$', 'bayareaweddingfairs_tickets.views.Main'),
                       url(r'^buy/(?P<id>.+)/$', 'bayareaweddingfairs_tickets.views.BuyTickets'),
                       url(r'^promocode/', 'bayareaweddingfairs_tickets.views.PromoCode_Validate', name='promocode'),
                       url(r'^checkajax/', 'bayareaweddingfairs_tickets.views.checkout_ajax', name='checkout_ajax'),

                       # url(r'^shortlist/(?P<option_search_id>[^\.]+)/$', 'yapjoy_vendors.views.productlist'),
                       # url(r'^shortlist_req/(?P<option_search_id>[^\.]+)/$', 'yapjoy_vendors.views.productlist_req'),
                       # url(r'^message/(?P<product_id>[^\.]+)/(?P<receiver_id>[^\.]+)/$', 'yapjoy_vendors.views.vendor_message'),
                       )
