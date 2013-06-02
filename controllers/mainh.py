#!/usr/bin/env python
# -*- coding: latin-1 -*-

import os
from datetime import datetime
import consts
import logging
import operator

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api import mail
from models.models import *

import urllib

from BeautifulSoup import BeautifulSoup,NavigableString

# This controller handles the
# generation of the front page.

"""

"""

class MainHandler(webapp.RequestHandler):
    def get(self):
        logging.info("index")

        stockattrs = consts.stockattrs

        filters = {}
        for att in stockattrs:
            filters['min'+att] = 0
            filters['max'+att] = 0
        filters['minpl'] = 1
        filters['maxpl'] = 20
        filters['minroe'] = 0
        filters['minpvp'] = 0
        filters['maxpvp'] = 10
        filters['minliqcor'] = 1
        filters['minmrgebit'] = 0
        filters['mingrowth'] = 5
        filters['minliquidez'] = 100000

        boolfilters = {}
        for att in stockattrs:
            boolfilters['min'+att] = False
            boolfilters['max'+att] = False
        boolfilters['minpl'] = True
        boolfilters['maxpl'] = True
        boolfilters['minroe'] = True
        boolfilters['minpvp'] = True
        boolfilters['maxpvp'] = True
        boolfilters['minliqcor'] = True
        boolfilters['minmrgebit'] = True
        boolfilters['mingrowth'] = True
        boolfilters['minliquidez'] = True

        boolreturn = {}
        for att in stockattrs:
            boolreturn[att] = False
        boolreturn['pl'] = True
        # boolreturn['roe'] = True
        boolreturn['evebit'] = True
        # boolreturn['roic'] = True
        boolreturn['growth'] = True
        boolreturn['divyield'] = True
        boolreturn['quote'] = True

        selected = []
        selected.append('pl')
        # selected.append('roe')
        selected.append('evebit')
        # selected.append('roic')
        selected.append('growth')
        selected.append('divyield')
                  
        template_values = {
            'stocks': goodStocks(),
            'lastQuote': lastQuote(),
            'stockattrs' : consts.stockattrs,
            'filters' : filters,
            'boolfilters' : boolfilters,
            'boolreturn' : boolreturn,
            'selected' : selected,
            'attrnames' : consts.attrnames,
            'attrtips' : consts.attrtips,
        }
        # logging.info("index end")
        #    payload = dict(stocks = stocks)
        # return render_to_response('index.html', template_values)


        # We are using the template module to output the page.

        path = os.path.join(os.path.dirname(__file__), '../views' ,'index.html')

        self.response.out.write(template.render(path,template_values))


class RefilterHandler(webapp.RequestHandler):
    def post(self):

        logging.info("refilter")
        stockattrs = consts.stockattrs
        
        filters = {}
        boolfilters = {}
        boolreturn = {}
        


        selected = []
        for att in stockattrs:
            if self.request.get("cmin"+att) == "1":
                filters['min'+att] = float(self.request.get("min"+att))
                boolfilters['min'+att] = True
            if self.request.get("cmax"+att) == "1":
                filters['max'+att] = float(self.request.get("max"+att))
                boolfilters['max'+att] = True
            if self.request.get("return"+att) == "1":
                boolreturn[att] = True
                selected.append(att)


        filteredStocks = sortStocks(filterStocks(filters), selected)

        for att in stockattrs:
            if 'min'+att not in filters:
                filters['min'+att] = 0
            if 'max'+att not in filters:
                filters['max'+att] = 0
            if 'min'+att not in boolfilters:
                boolfilters['min'+att] = False
            if 'max'+att not in boolfilters:
                boolfilters['max'+att] = False
            if att not in boolreturn:
                boolreturn[att] = False

        template_values = {
            'stocks': filteredStocks,
            'lastQuote': "Refiltragem!",#lastQuote(),
            'stockattrs' : consts.stockattrs,
            'filters' : filters,
            'boolfilters' : boolfilters,
            'boolreturn' : boolreturn,
            'selected' : selected,
            'attrnames' : consts.attrnames,
        }
        # logging.info("refilter end")

        path = os.path.join(os.path.dirname(__file__), '../views' ,'table.html')

        self.response.out.write(template.render(path,template_values))

class MailHandler(webapp.RequestHandler):
    def post(self):

        form_fields = {
          "privatekey": "6LcnKt8SAAAAAGgST1o4Bxzybc_-pDHz-X1LAUxh",
          "remoteip": self.request.remote_addr,
          "challenge": self.request.get("recaptcha_challenge_field"),
          "response": self.request.get("recaptcha_response_field")
        }
        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url="http://www.google.com/recaptcha/api/verify",
                                payload=form_data,
                                method=urlfetch.POST,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if result.status_code == 200:
            response = result.content
            logging.info(response)
            if "true" in response:
                # logging.info("envia email!")
                mail.send_mail(sender="Contato OrdenaAções <contato@ordenaacoes.appspotmail.com>",
                    to="Juliano Krieger <julianosk@gmail.com>",
                    subject="Contato OrdenaAções",
                    body="Contato: "+self.request.get("name")+" <"+self.request.get("email")+">\n\nMensagem:\n"+self.request.get("message"))
                self.response.out.write("true")
            else:
                self.response.out.write("false")



def goodStocks():
    """
    http://www.investidorjovem.com.br/achando-acoes-para-investir-a-formula-magica-de-joel-greenblatt
    P/L entre 1 e 20
    ROE maior que 0%
    P/VP entre 0 e 10
    Liquidez corrente maior que 1
    Margem de Ebtida maior que 0
    Crescimento anual maior que 8% (para filtrar empresas que crescam mais que o PIB Brasileiro)
    Liquidez das acoes maior que 100 milhoes (para tirar as Small caps de terceira linha
    """
    
    goodStocks = memcache.get("goodStocks")
    if goodStocks is not None:
        return goodStocks
    else:
        filters = {}
        filters['minpl'] = 1
        filters['maxpl'] = 20
        filters['minroe'] = 0
        filters['minpvp'] = 0
        filters['maxpvp'] = 10
        filters['minliqcor'] = 1
        filters['minmrgebit'] = 0
        filters['mingrowth'] = 5
        filters['minliquidez'] = 100000
        indicators = ['pl', 'evebit', 'growth', 'roe', 'roic', 'divyield']
        goodStocks = sortStocks(filterStocks(filters), indicators)
        if not memcache.add("goodStocks", goodStocks):
            logging.error("Memcache set failed.")
        return goodStocks

def lastQuote():
    last = StockUpdate.all().order('-updated_on').get()
    if last is not None:
        return last.last
    else:
        return ""

    # lastQuote = memcache.get("lastQuote")
    # if lastQuote is not None:
    #     return lastQuote
    # else:
    #     last = StockUpdate.all().order('-updated_on').get()
    #     if last is not None:
    #         memcache.add('lastQuote', last.last)#memcache.add('lastQuote', last.last+' # '+str(last.updated_on))
    #     else:
    #         return "xx/xx/xxxx"

def filterStocks(filters):
    filts = []
    for stock in Stock.all().order('name'):
        insert = True
        for attr in consts.stockattrs:
            if ('min'+attr) in filters:
                # logging.info('min'+attr+' = '+filters[('min'+attr)])
                if getattr(stock, attr) < filters[('min'+attr)]:
                    # logging.info('min'+attr+' = ' + str(filters[('min'+attr)])+' | '+stock.name+ ' = ' + str(getattr(stock, attr)))
                    insert = False
                    break
            if ('max'+attr) in filters:
                # logging.info('max'+attr+' = '+filters[('max'+attr)])
                if getattr(stock, attr) > filters[('max'+attr)]:
                    # logging.info('max'+attr+' = ' + str(filters[('max'+attr)])+' | '+stock.name+ ' = ' + str(getattr(stock, attr)))
                    insert = False
                    break
        if insert:
            filts.append(stock)
    
    logging.info('num stocks = %d' %len(filts))
    return filts    
    
def sortStocks(stocks,indicators):
    for indicator in indicators:
        stocks.sort(key=operator.attrgetter(indicator),reverse=consts.indicatorsorder[indicator])
        for index,stock in enumerate(stocks):
            setattr(stock, 'pos'+indicator, index+1)
    
    for stock in stocks:
        stock.possum = 0
        for indicator in indicators:
            stock.possum += getattr(stock,'pos'+indicator)
        
    stocks.sort(key=operator.attrgetter("possum"))
    
    return stocks

class IBrXHandler(webapp.RequestHandler):
    def get(self):
        logging.info("index init")

        stockattrs = consts.stockattrs

        filters = {}
        for att in stockattrs:
            filters['min'+att] = 0
            filters['max'+att] = 0
        filters['minpl'] = 1
        filters['maxpl'] = 20
        filters['minroe'] = 0
        filters['minpvp'] = 0
        filters['maxpvp'] = 10
        filters['minliqcor'] = 1
        filters['minmrgebit'] = 0
        filters['mingrowth'] = 5
        filters['minliquidez'] = 100000

        boolfilters = {}
        for att in stockattrs:
            boolfilters['min'+att] = False
            boolfilters['max'+att] = False
        boolfilters['minpl'] = True
        boolfilters['maxpl'] = True
        boolfilters['minroe'] = True
        boolfilters['minpvp'] = True
        boolfilters['maxpvp'] = True
        boolfilters['minliqcor'] = True
        boolfilters['minmrgebit'] = True
        boolfilters['mingrowth'] = True
        boolfilters['minliquidez'] = True

        boolreturn = {}
        for att in stockattrs:
            boolreturn[att] = False
        boolreturn['pl'] = True
        boolreturn['roe'] = True
        boolreturn['evebit'] = True
        boolreturn['roic'] = True
        boolreturn['growth'] = True
        boolreturn['divyield'] = True
        boolreturn['quote'] = True

        selected = []
        selected.append('pl')
        selected.append('roe')
        selected.append('evebit')
        selected.append('roic')
        selected.append('growth')
        selected.append('divyield')
                  
        template_values = {
            'stocks': self.goodStocks(),
            'lastQuote': lastQuote(),
            'stockattrs' : consts.stockattrs,
            'filters' : filters,
            'boolfilters' : boolfilters,
            'boolreturn' : boolreturn,
            'selected' : selected,
            'attrnames' : consts.attrnames,
        }
        logging.info("index end")
        #    payload = dict(stocks = stocks)
        # return render_to_response('index.html', template_values)


        # We are using the template module to output the page.

        path = os.path.join(os.path.dirname(__file__), '../views' ,'index.html')

        self.response.out.write(template.render(path,template_values))

    def goodStocks(self):
        """
        http://www.investidorjovem.com.br/achando-acoes-para-investir-a-formula-magica-de-joel-greenblatt
        P/L entre 1 e 20
        ROE maior que 0%
        P/VP entre 0 e 10
        Liquidez corrente maior que 1
        Margem de Ebtida maior que 0
        Crescimento anual maior que 8% (para filtrar empresas que crescam mais que o PIB Brasileiro)
        Liquidez das acoes maior que 100 milhoes (para tirar as Small caps de terceira linha
        """
        
        goodStocks = memcache.get("ibrxStocks")
        if goodStocks is not None:
            return goodStocks
        else:
            indicators = ['pl', 'evebit', 'growth', 'roe', 'roic', 'divyield']
            goodStocks = sortStocks(self.ibrxFilter(), indicators)
            if not memcache.add("ibrxStocks", goodStocks):
                logging.error("Memcache set failed.")
            return goodStocks

    def ibrxFilter(self):
        filts = []
        for stock in Stock.all():
            if stock.name in consts.ibrx:
                filts.append(stock)
        
        logging.info('num stocks = %d' %len(filts))
        return filts  




