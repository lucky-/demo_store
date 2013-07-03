from django.shortcuts import render_to_response
from store import models
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse
import json
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from decimal import *


def store_front(request,merchant):
	request.session['merchant']=merchant
	for_sale = models.items.objects.filter(Q(merchant__name__exact = merchant) & ~Q(stock=0))
	if 'cart' in request.session.keys():
		cart_items = len(request.session['cart'])
	else:
		cart_items = 0
	return render_to_response('store/front.html', dict(for_sale = for_sale, merchant_base = 'customized/{0}_base.html'.format(merchant), merchant=merchant, cart_items = cart_items, show_cart=True), context_instance=RequestContext(request))


def item(request, item_id):
	merchant = request.session['merchant']
	item = models.items.objects.get(pk=item_id)
	if 'cart' in request.session.keys():
		cart_items = len(request.session['cart'])
	else:
		cart_items = 0
	return render_to_response('store/item.html', dict(item=item, merchant_base = 'customized/{0}_base.html'.format(merchant), merchant=merchant, cart_items = cart_items, show_cart=True), context_instance=RequestContext(request))


def ajaxadd(request):
	pk = int(request.GET['item_pk'])
	if 'cart' in request.session.keys():
		cart = request.session['cart']
		if pk not in cart:
			cart.append(pk)
			request.session['cart'] = cart
	else:
		request.session['cart'] = [pk]
	return HttpResponse(json.dumps(('success',len(request.session['cart']))), content_type="application/json")


def shoppingcart(request):
	merchant = request.session['merchant']
	items = models.items.objects.filter(pk__in=request.session['cart'])
	shipping = Group.objects.get(name=merchant).base_shipping
	base_price = Decimal(0)
	for item in items:
		shipping += item.m_shipping
		base_price += item.price
	total = shipping + base_price
	request.session['total']=total
	return render_to_response('store/cart.html', dict(items=items, merchant_base = 'customized/{0}_base.html'.format(merchant), merchant=merchant, shipping = shipping, base_price = base_price, total=total), context_instance=RequestContext(request))


def clearcart(request):
	merchant = request.session['merchant']
	request.session.flush()
	return redirect('store.views.store_front', merchant )
		




	



	
