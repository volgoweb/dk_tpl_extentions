# -*- coding: utf-8 -*-

from django import template
from django.http import QueryDict

register = template.Library()

# Заменяет или добавляет указанные параметры в текущем адресе 
# и возвращает этот измененный адрес
# Для работы данного тега необходимо включать в контекст шаблона переменную request
# Пример использования: {% url params newparam='bla' newparam2=var_in_context.param modified_param='new_value' %}
@register.simple_tag(takes_context=True)
def url_params(context, **kwargs):
	req = context['request']
	base_url = req.get_full_path()

	# получаем словарь параметров текущего url
	current_get_params = dict(req.GET.copy())
	for name in kwargs:
		current_get_params[name] = kwargs[name]

	new_query = []
	for name in current_get_params:
		value = current_get_params[name]
		if type(value) is list:
			value = value[0]
		# чтобы выполнить замену пробела (который автоматически появляется взамен "+") конвертируем в строку
		value = str(value)
		value = value.replace(' ', '+')
		new_query.append( '%s=%s' % (name, value) )
	new_url = req.path + '?' + '&'.join(new_query)
	# raise False

	return new_url

	
