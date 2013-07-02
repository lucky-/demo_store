from django.contrib import admin
from store import models




class buyerInline(admin.TabularInline):
	model = models.buyer_data
	exclude = ('user',)
	


class itemsAdmin(admin.ModelAdmin):
	exclude = ('merchant',)
	list_display = ('name', 'price')
	def queryset(self, request):
		local_set = super(ordersAdmin, self).queryset(request)
		if request.user.is_superuser:
		    return local_set
		return local_set.filter(merchant=request.user.groups.all()[0])
admin.site.register(models.items, itemsAdmin)

class ordersAdmin(admin.ModelAdmin):
	inlines = [
        buyerInline,
    ]
	exclude = ('merchant',)
	def queryset(self, request):
		local_set = super(ordersAdmin, self).queryset(request)
		if request.user.is_superuser:
		    return local_set
		return local_set.filter(merchant=request.user.groups.all()[0])
admin.site.register(models.orders, ordersAdmin)

