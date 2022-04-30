import urllib
from lxml.html import fromstring
import requests

url = 'http://microformats.org/'
content = urllib.request.urlopen(url).read()
doc = fromstring(content)
doc.make_links_absolute(url)


# we create a class to put the information in
class Card(object):
	def __init__(self, **kw):
		for name, value in kw:
			settatr(self, name, value)

class Phone(object):
	def __init__(self, phone, types=()):
		self.phone, self.types = phone, types

def get_text(el, class_name):
	els = el.find_class(class_name)
	if els:
		return els[0].text_content()
	else:
		return ''

def get_value(el):
 	    return get_text(el, 'value') or el.text_content()
 	
def get_all_texts(el, class_name):
	return [e.text_content() for e in els.find_class(class_name)]

def parse_addresses(el):
    # Ideally this would parse street, etc.
    return el.find_class('adr')


for el in doc.find_class('hcard'):
	card = Card()
	card.el = el
	card.fn = get_text(el, 'fn')
	card.tels = []
	for tel_el in card.find_class('tel'):
		card.tels.append(Phone(get_value(tel_el),get_all_texts(tel_el, 'type')))
		card.addresses = parse_addresses(el)














