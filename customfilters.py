#!/usr/bin/env python

import re
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

numeric_test = re.compile("^\d+$")

@register.filter
def getattribute(value, arg):
	"""Gets an attribute of an object dynamically from a string name"""
	
	if hasattr(value, str(arg)):
		return getattr(value, arg)
	elif hasattr(value, 'has_key') and value.has_key(arg):
		return value[arg]
	elif numeric_test.match(str(arg)) and len(value) > int(arg):
		return value[int(arg)]
	else:
		return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)

@register.filter
def getpos(value, arg):
	if hasattr(value, str(arg)):
		return getattr(value, 'pos'+arg)
	else:
		return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getpos', getpos)

@register.filter
def getmin(value, arg):
	if hasattr(value, 'has_key') and value.has_key('min'+arg):
		return value['min'+arg]
	else:
		return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getmin', getmin)

@register.filter
def getmax(value, arg):
	if hasattr(value, 'has_key') and value.has_key('max'+arg):
		return value['max'+arg]
	else:
		return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getmax', getmax)

@register.filter
def concat(value, arg):
	"""Concatenate two strings"""
	return value+arg

register.filter('concat', concat)


# Then, in template:
# {% load getattribute %}
# {{ object|getattribute:dynamic_string_var }}
