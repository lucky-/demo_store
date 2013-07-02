from django.shortcuts import render_to_response
from store import models
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q


def store_front(request,merchant):
	for_sale = models.items.objects.filter(Q(merchant__name__exact = merchant) & ~Q(stock=0))
	return render_to_response('store/front.html', dict(for_sale = for_sale, merchant_base = 'customized/{0}_base.html'.format(merchant)), context_instance=RequestContext(request))
