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
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


def store_front(request, merchant):
	request.session['merchant']=merchant
	for_sale = models.items.objects.filter(Q(merchant__name__exact = merchant) & ~Q(stock=0))
	if 'cart' in request.session.keys():
		cart_items = len(request.session['cart'])
	else:
		cart_items = 0
	return render_to_response('store/front.html', dict(for_sale = for_sale, merchant_base = 'customized/{0}_base.html'.format(merchant), merchant=merchant, cart_items = cart_items, show_cart=True), context_instance=RequestContext(request))


def error_page(request):
	return render_to_response('store/error_page.html', dict(e_message=request.session['e_message']), context_instance=RequestContext(request))


def item(request, item_id):
	item = models.items.objects.get(pk=item_id)
	if 'cart' in request.session.keys():
		cart_items = len(request.session['cart'])
	else:
		cart_items = 0
	return render_to_response('store/item.html', dict(item=item, cart_items = cart_items, show_cart=True), context_instance=RequestContext(request))


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
		
		#if user already exists
		if request.POST['post_method']=='login':
			user = authenticate(username=request.POST['username'], password=request.POST['ps'])
			if user is not None:
				buyer = models.buyer_data.objects.get(user=user)
			else:	
				request.session['e_message'] = 'Incorrect user name or password'
				return 	redirect('store.views.error_page')
		# for new users
		else:
			
			data_fields = ['name', 'address', 'city', 'state', 'zip_code', 'phone', 'email']
			kwargs = dict( merchant=Group.objects.get(name=merchant))
			for field in data_fields:
				if not request.POST[field]:
					request.session['e_message'] =  'You failed to fill in the "{0}" field'.format(field)
					return 	redirect('store.views.error_page')
				kwargs[field] = request.POST[field]
			try:
				user = 	User.objects.create_user(request.POST['username'], '', request.POST['ps'])
				user.save()
			except Exception, e:
				request.session['e_message'] = 'Login info error.  Please try a new name & password.'
				return 	redirect('store.views.error_page')
			kwargs['user'] = user
			buyer = models.buyer_data(**kwargs) 
			buyer.save()
		request.session['buyer'] = buyer
		the_order = models.orders(paid=False, date = datetime.datetime.now(), total=request.session['total'], shipped=False, buyer_data=buyer, ship_date=datetime.datetime.now() )
		the_order.save()
		for item in request.session['cart']:
			the_order.items.add(item) 
		the_order.save()
		request.session['the_order']=the_order
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
		return render_to_response('store/cart.html', dict(items=items, shipping = shipping, base_price = base_price, total=total), context_instance=RequestContext(request))


def clearcart(request):
	merchant = request.session['merchant']
	request.session.flush()
	return redirect('store.views.store_front', merchant )



		

def cart2(request):
	
	return render_to_response('store/cart2.html', dict( order=request.session['the_order'], buyer=request.session['buyer'], ), context_instance=RequestContext(request))


def purchased(request):
	the_order = request.session['the_order']
	the_order.paid = True
	the_order.save()
	merchant = request.session['merchant']
	request.session.flush()
	request.session['merchant'] = merchant
	return render_to_response('store/purchased.html', dict(), context_instance=RequestContext(request))



@login_required
def view_orders(request):
	the_user = request.user
	orders = models.orders.objects.filter(Q(buyer_data__user=the_user) & Q(paid=True))
	return render_to_response('store/view_orders.html', dict( orders=orders), context_instance=RequestContext(request))
	



	
