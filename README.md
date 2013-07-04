demo_store
==========

Installation:

Download the 'store' app.  Put it in your project folder.  Add it to installed apps.

To use the demo store, the following is required:
1)sessions must be enabled
2)(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'myapp/login.html'}) must be put in the site level URLS
3)(r'^store/', include('store.urls')) must be put in the site level URLS
5)"store.store_context.merchant" must be added to your list of template context processors



Sample Data
=============
If you would also like to use the sample templates and data, please put the sampledata file in your project folder
1)In settings, choose sqllite3 as your database and link it to sample.db in sampledata
2)Also in settings, make sure sampledata/staticfiles is listed in your STATICFILES_DIRS
3)Third, in settings, make sure your media root is set to /sampledata/media



The sample data contails 3 stores with REALLLY bad front end templates. The urls for them are '/store/Bookstore', '/store/Treestore/', and '/store/Shoestore/'  Additionally, a superuser exists username:happy.  three staff users exist book_master, tree_master, and shoe_master.  The password for all accounts is happy1.  



Customizing
========
Stores are based on Groups.  A new group represents a new store.
The group must be given all privilages pertaining to store models.


Customized templates should go in the customized folder inside templates.  They should have the name of the group + '_base.html'
Template parent structure can be seen in the samples.



