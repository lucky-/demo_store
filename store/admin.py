from django.contrib import admin
from store import models
from django import forms
from django.contrib.auth.models import Group
from django.db.models import Q




class ordersInline(admin.TabularInline):
	model = models.orders
	def queryset(self, request):
		local_set = super(ordersInline, self).queryset(request)
		if request.user.is_superuser:
		    return local_set
		return local_set.filter(paid=True)


class itemsAdmin(admin.ModelAdmin):
	list_display = ('name', 'price')
	def get_form(self, request, obj=None, **kwargs):
		form = super(itemsAdmin, self).get_form(request, obj, **kwargs)
		if not request.user.is_superuser:
			g_name=request.user.groups.all()[0].name
			q_set = Group.objects.filter(name=g_name)
			form.base_fields['merchant'] = forms.ModelChoiceField(queryset=q_set, empty_label=None) 
		return form
	def queryset(self, request):
		local_set = super(itemsAdmin, self).queryset(request)
		if request.user.is_superuser:
		    return local_set
		return local_set.filter(merchant=request.user.groups.all()[0])
admin.site.register(models.items, itemsAdmin)

class buyerAdmin(admin.ModelAdmin):
	inlines = [
        ordersInline,
    ]
	exclude = ('merchant', 'user')
	def queryset(self, request):
		local_set = super(buyerAdmin, self).queryset(request)
		if request.user.is_superuser:
		    return local_set
		return local_set.filter(Q(merchant=request.user.groups.all()[0]) & Q(hide=False))
admin.site.register(models.buyer_data, buyerAdmin)

