

def merchant(request):
	m_dict = dict()
	if 'merchant' in request.session.keys():
		merchant = request.session['merchant']
		m_dict['merchant_base'] = 'customized/{0}_base.html'.format(merchant) 
		m_dict['merchant']=merchant
	return m_dict
