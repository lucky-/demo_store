from django.shortcuts import render_to_response
from store import models
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse


def store_front(request,merchant):
	for_sale = models.items.objects.filter(Q(merchant__name__exact = merchant) & ~Q(stock=0))
	return render_to_response('store/front.html', dict(for_sale = for_sale, merchant_base = 'customized/{0}_base.html'.format(merchant), merchant=merchant), context_instance=RequestContext(request))


def item(request, merchant, item_id):
	item = models.items.objects.get(pk=item_id)
	return render_to_response('store/item.html', dict(item=item, merchant_base = 'customized/{0}_base.html'.format(merchant), merchant=merchant), context_instance=RequestContext(request))



	
