#!/usr/bin/env python

# Importing the controllers that will handle
# the generation of the pages:
from controllers import crons,mainh

# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
import locale

# This is the main method that maps the URLs
# of your application with controller classes.
# If a URL is requested that is not listed here,
# a 404 error is displayed.
"""
TODO:

- Passar processamento de cron para backend
- dica quando o mouse passar por cima na cabeca da tabela

DONE:
- Diferenca da cotacao com relacao a anterior
	- adicionar valor no Model
	- colocar linha na tabela
- cotacao(+/-diferenca) (ao inves de uma coluna)
- quando refiltrar, alterar os checkboxes de reordenacao
- Reordenar sem reload - DONE
- Cron Job para atualizar valores - DONE
- botao retirar todos filtros
- mudar visual (jqueryui?)
	- spinner min e max
- Implementar Refiltragem
	- Com reload
	- Sem reload

Fontes:
- http://code.google.com/appengine/docs/python/config/cron.html - FEITO
- http://code.google.com/appengine/docs/python/backends/overview.html
- http://tablesorter.com/docs/example-ajax.html
http://www.investidorjovem.com.br/achando-acoes-para-investir-a-formula-magica-de-joel-greenblatt
"""


def main():

	# locale.setlocale(locale.LC_ALL, ('pt_BR', 'iso8859-1'))
	template.register_template_library('customfilters')

	application = webapp.WSGIApplication([
		('/', mainh.MainHandler),
		('/ibrx', mainh.IBrXHandler),
		('/refilter', mainh.RefilterHandler),
		('/mail', mainh.MailHandler),
		# ('/update', crons.UpdateHandler),
		('/crons/update', crons.UpdateHandler),
	],debug=True)
	
	util.run_wsgi_app(application)

	


if __name__ == '__main__':
	main()
