
from django.test import TestCase
from store import models
from django.test import Client


#make sure switching stores works
class store_switch(TestCase):
    def test_switch(self):
	a_client = Client(HTTP_USER_AGENT='Mozilla/5.0')
	b_client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        a_resp=a_client.get('/store/Bookstore/')
	b_client.get('/store/Shoestore/')
	b_resp=b_client.get('/store/Bookstore/')
        self.assertEqual(a_resp.request['PATH_INFO'], b_resp.request['PATH_INFO'])


#testing of shopping cart page 1
class shopping_cart(TestCase):
	#test posting with incomplete form
	def inc_post(self):
		a_client = Client(HTTP_USER_AGENT='Mozilla/5.0')
		#missing password
		a_resp = a_client.post('/store/cart/', {'post_method': 'login', 'username': 'somename'})
		self.assertEqual(a_resp.context['e_message'], 'Incorrect user name or password')
		#missing username
		a_resp = a_client.post('/store/cart/', {'post_method': 'login', 'ps': 'somename'})
		self.assertEqual(a_resp.context['e_message'], 'Incorrect user name or password')
		#incorrect data
		a_resp = a_client.post('/store/cart/', {'post_method': 'login', 'username': '0', 'ps':'0'})
		self.assertEqual(a_resp.context['e_message'], 'Incorrect user name or password')
		#new users lacking usename/ps
		a_resp = a_client.post('/store/cart/', dict(post_method='create', name='something', address='something', city='something', state='something', zip_code='something', phone='something', email='something') )
		self.assertEqual(a_resp.context['e_message'], 'Login info error.  Please try a new name & password.')





		
		
		

