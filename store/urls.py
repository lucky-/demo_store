from django.conf.urls import patterns, url
from store import  views


urlpatterns = patterns('',
	url(r'^ajaxadd/$', views.ajaxadd),
	url(r'^error_page/$', views.error_page, name='error_page'),
	url(r'^cart/$', views.shoppingcart),
	url(r'^cart2/$', views.cart2),
	url(r'^clearcart/$', views.clearcart),
	url(r'^purchased/$', views.purchased),
	url(r'^item/(?P<item_id>\d+)/$', views.item, name='item'),
	url(r'^(?P<merchant>\w{0,50})/$', views.store_front, name='store_front'),
	
) 


