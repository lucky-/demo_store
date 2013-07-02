from django.db import models
from django.contrib.auth.models import Group, User


# Create your models here.





class items(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=300)
	stock = models.IntegerField()
	merchant = models.ForeignKey(Group)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	picture = models.FileField(upload_to='images')
	#marginal shipping
	m_shipping = models.DecimalField(max_digits=8, decimal_places=2)
	



class orders(models.Model):
	date = models.DateTimeField()
	merchant = models.ForeignKey(Group)
	items = models.ManyToManyField(items)
	total = models.DecimalField(max_digits=8, decimal_places=2)
	shipped = models.BooleanField()
	ship_date = models.DateTimeField()
	tracking = models.CharField(max_length=50, default='-none-')
	def __unicode__(self):
		return self.date.strftime('%Y-%m-%d') + '_shipped=' + str(self.shipped)


class buyer_data(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length = 30)
	zip_code=models.CharField(max_length=30)
	phone = models.CharField(max_length=30)
	email = models.EmailField()
	orders = models.ForeignKey(orders)



#add fields to 'groups' for merchant
if not hasattr(Group, 'base_shipping'):
    base_shipping_field = models.DecimalField(max_digits=8, decimal_places=2)
    base_shipping_field.contribute_to_class(Group, 'base_shipping')

