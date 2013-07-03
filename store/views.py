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
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from decimal import *
import datetime


def store_front(request,merchant):
	request.session['merchant']=merchant
	for_sale = models.items.objects.filter(Q(merchant__name__exact = merchant) & ~Q(stock=0))
	if 'cart' in request.session.keys():
		cart_items = len(request.session['cart'])
	else:
		cart_items = 0
	return render_to_response('store/front.html', dict(for_sale = for_sale, merchant_base = 'customized/{0}_base.html'.format(merchant), merchant=merchant, cart_items = cart_items, show_cart=True), context_instance=RequestContext(request))


def error_page(request, e_message):
	return render_to_response('store/error_page.html', dict(e_message=e_message, merchant_base = 'customized/{0}_base.html'.format(merchant)), context_instance=RequestContext(request))

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
	item = models.items.objects.get(pk=pk)
	if 'cart' in request.session.keys():
		cart = request.session['cart']
		if item not in cart:
			cart.append(item)
			request.session['cart'] = cart
	else:
		request.session['cart'] = [item]
	return HttpResponse(json.dumps(('success',len(request.session['cart']))), content_type="application/json")


def shoppingcart(request):
	merchant = request.session['merchant']
	#check if order has already been created
	if 'the_order' in request.session.keys():
		return redirect('store.views.cart2' )
	if request.method=='POST':
		the_order = models.orders(paid=False, date = datetime.datetime.now(), merchant=Group.objects.get(name=merchant), total=request.session['total'], shipped=False, ship_date=datetime.datetime.now() )
		the_order.save()
		for item in request.session['cart']:
			the_order.items.add(item) 
		the_order.save()
		request.session['the_order']=the_order
		#if user already exists
		if request.POST['post_method']=='login':
			user = authenticate(username=request.POST['username'], password=request.POST['pw'])
			if user is not None:
				buyer = models.buyer_data.objects.get(user=user)
			else:	
				e_message = 'Incorrect user name or password'
				return 	redirect('store.views.error_page', e_message )
		# for new users
		else:
			try:
				user = 	User.objects.create_user(request.POST['username'], '', request.POST['pw'])
				user.save()
			except Exception, e:
				e_message = 'User name error.  Please try a new name.'
				return 	redirect('store.views.error_page', e_message )
			data_fields = ['name', 'address', 'city', 'state', 'zip_code', 'phone', 'email']
			keys = request.POST.keys()
			kwargs = dict(user=user, orders=the_order)
			for field in data_fields:
				if field not in keys:
					e_message = 'You failed to fill in the "{0}" field'.format(field)
					return redirect('store.views.error_page', e_message )
				kwargs[field] = request.POST[field]
			buyer = models.buyer_data(**kwargs) 
			buyer.save()
		request.session['buyer'] = buyer
		return redirect('store.views.cart2' )
	
	else:
		items = request.session['cart']
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



		

def cart2(request):
	if request.method=='POST':
		pass
	else:
		return render_to_response('store/cart2.html', dict(order=request.session['the_order'], buyer=request.session['buyer'], merchant_base = 'customized/{0}_base.html'.format(merchant)), context_instance=RequestContext(request))



	
