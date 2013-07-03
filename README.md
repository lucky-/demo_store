demo_store
==========



Required:
Sessions
include cartdiv tag
include navdiv tag
(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'myapp/login.html'}),
store_context processor
