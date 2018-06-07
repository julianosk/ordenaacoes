#!/usr/bin/env python

import time
import logging
from datetime import datetime,timedelta
from google.appengine.api import urlfetch
from google.appengine.ext import webapp,db
from google.appengine.api import memcache

import urllib2

from models.models import *

from BeautifulSoup import BeautifulSoup,NavigableString

class UpdateHandler(webapp.RequestHandler):

    # The get method is executed once per day,
    # and it creates a new Day entry from the last
    # 24 hours worth of pings.
    def get(self):

        # https://developers.google.com/appengine/docs/python/urlfetch/asynchronousrequests?hl=pl
        
        url = 'http://fundamentus.com.br/detalhes.php?papel=VALE3'
        memcache.delete("goodStocks")
        rpc = urlfetch.create_rpc(deadline=600)
        urlfetch.make_fetch_call(rpc,url)

        result = urlfetch.fetch(url)
        try:
            

            result = rpc.get_result()
            soup = BeautifulSoup(result.content)
            su = StockUpdate(last = str(soup.body.table.findAll("tr")[1].findAll("td")[3].span.string))
            
            lastsaved = StockUpdate.all().order('-updated_on').get()
            if lastsaved is None:
                logging.info("lastsaved is None")
            elif lastsaved.last != su.last:
                logging.info("diff!")
            else:
                logging.info("nao atualiza!")


            if (lastsaved is None) or (lastsaved.last != su.last):

                url = "http://www.fundamentus.com.br/resultado.php"
                
                rpc = urlfetch.create_rpc(deadline=600)
                urlfetch.make_fetch_call(rpc,url)

                #result = urlfetch.fetch(url,deadline=60,method=urlfetch.POST)
                # result = urllib2.urlopen(url,timeout=60)

                # if result.status_code == 200:
                try:

                    result = rpc.get_result()
                    logging.info("Fundamentus fetched")
                    #        query = Stock.all()
                    # db.delete(Stock.all())
                    #        logging.info("Stocks deleted")
                    soup = BeautifulSoup(result.content)
                    # soup = BeautifulSoup(result.read())
                    updated = []
                    num = 0
                    lines = soup.body.table.tbody.findAll("tr")
                    # sss= Stock.all()
                    # for st in sss:
                    #     logging.info("atual " + str(st.name))

                    for i in range(0,len(lines)):
                        tr = lines[i]
                        
                        colunas = tr.findAll("td")
                        sname = str(colunas[0].span.a.string) # nome
                        quote = float(str(colunas[1].string).replace('.','').replace(',','.')) # Cotacao
                        pl = float(str(colunas[2].string).replace('.','').replace(',','.')) # P/L
                        pvp = float(str(colunas[3].string).replace('.','').replace(',','.')) # P/VP
                        psr = float(str(colunas[4].string).replace('.','').replace(',','.')) # PSR
                        sdivyield = str(colunas[5].string).replace('.','').replace(',','.') #Dividend Yield - Maior Melhor
                        divyield = float(sdivyield[0:sdivyield.find('%')])
                        pativo = float(str(colunas[6].string).replace('.','').replace(',','.')) #P/Ativo
                        pcapgiro = float(str(colunas[7].string).replace('.','').replace(',','.')) #P/Cap.Giro
                        pebit = float(str(colunas[8].string).replace('.','').replace(',','.')) #P/EBIT
                        pativcircliq = float(str(colunas[9].string).replace('.','').replace(',','.')) #P/Ativ Circ. Liq
                        evebit = float(str(colunas[10].string).replace('.','').replace(',','.')) #EV/EBIT - Menor Melhor 
                        smrgebit = str(colunas[11].string).replace('.','').replace(',','.') #Mrg Ebit
                        mrgebit = float(smrgebit[0:smrgebit.find('%')])
                        smrgliq = str(colunas[12].string).replace('.','').replace(',','.') #Mrg Liq.
                        mrgliq = float(smrgliq[0:smrgliq.find('%')])
                        liqcor = float(str(colunas[13].string).replace('.','').replace(',','.')) #Liquidez Corrente - Maior Melhor > 1
                        sroic = str(colunas[14].string).replace('.','').replace(',','.') #ROIC - Maior Melhor
                        roic = float(sroic[0:sroic.find('%')])
                        sroe = str(colunas[15].string).replace('.','').replace(',','.') #ROE - Maior Melhor - Maior que 0
                        roe = float(sroe[0:sroe.find('%')])
                        liquidez = float(str(colunas[16].string).replace('.','').replace(',','.')) #Liquidez 2 meses > 100.000
                        patrimliq = float(str(colunas[17].string).replace('.','').replace(',','.')) #Patrimonio Liquido
                        divbrutpatr = float(str(colunas[18].string).replace('.','').replace(',','.')) #Div. Brut/ Patrim.
                        sgrowth = str(colunas[19].string).replace('.','').replace(',','.') #Crescimento - Maior Melhor > 5%
                        growth = float(sgrowth[0:sgrowth.find('%')])
                        
                        stock = Stock.all().filter('name = ',sname).get()

                        if stock is None:
                            stock = Stock(name = sname)
                            stock.diff = 0.0
                            stock.oscillation = 0.0
                        else:
                            stock.diff = quote - stock.quote
                            if stock.quote != 0.0:
                                stock.oscillation = stock.diff*100/stock.quote
                            else:
                                stock.oscillation = 0.0

                        # logging.info("oscillation = "+str(stock.oscillation))
                        # logging.info("diff = "+str(stock.diff))

                        stock.quote = quote
                        stock.pl = pl
                        stock.pvp = pvp
                        stock.psr = psr
                        stock.divyield = divyield
                        stock.pativo = pativo
                        stock.pcapgiro = pcapgiro
                        stock.pebit = pebit
                        stock.pativcircliq = pativcircliq
                        stock.evebit = evebit
                        stock.mrgebit = mrgebit
                        stock.mrgliq = mrgliq
                        stock.liqcor = liqcor
                        stock.roic = roic
                        stock.roe = roe
                        stock.liquidez = liquidez
                        stock.patrimliq = patrimliq
                        stock.divbrutpatr = divbrutpatr
                        stock.growth = growth
                        

                        """
                        stock = Stock(name = name,
                            quote = quote,
                            pl = pl,
                            pvp = pvp,
                            psr = psr,
                            divyield = divyield,
                            pativo = pativo,
                            pcapgiro = pcapgiro,
                            pebit = pebit,
                            pativcircliq = pativcircliq,
                            evebit = evebit, 
                            mrgebit = mrgebit,
                            mrgliq = mrgliq,
                            liqcor = liqcor,
                            roic = roic,
                            roe = roe,
                            liquidez = liquidez,
                            patrimliq = patrimliq,
                            divbrutpatr = divbrutpatr,
                            growth = growth)
                        """         
                        updated.append(stock)
                        num += 1
                        
                        if num == 400:
                            logging.info("400 - !")
                            db.put(updated)
                            updated = []
                        
                        
                    db.put(updated)

                    logging.info("Stocks put %d" %num)

                    db.put(su)
                    if memcache.get('lastQuote') is not None:
                        memcache.delete('lastQuote')
                    # memcache.add('lastQuote', soup.body.table.findAll("tr")[1].findAll("td")[3].span.string)
                    memcache.add('lastQuote', su.last+' # '+str(su.updated_on))
                    
                
                except urllib2.URLError, e:
                    logging.info("Deu erro na urllib2!")

        except urllib2.URLError, e:
            logging.info("Deu erro na urllib2!")
        
"""
http://www.investidorjovem.com.br/achando-acoes-para-investir-a-formula-magica-de-joel-greenblatt
P/L entre 1 e 20
ROE maior que 0%
P/VP entre 0 e 10
Liquidez corrente maior que 1
Margem de Ebtida maior que 0    
Crescimento anual maior que 5% (para filtrar empresas que crescam mais que o PIB Brasileiro)
Liquidez das acoes maior que 100.000 (para tirar as nao negociadas)
"""
"""
#        quote #Cotacao
#        pl #P/L - Menor Melhor
#        evebit #EV/EBIT - Menor Melhor 
#        growth #Crescimento - Maior Melhor
#        divyield #Dividend Yield - Maior Melhor
#        roe #ROE - Maior Melhor
#        roic #ROIC - Maior Melhor
"""
            
            
        # return HttpResponseRedirect('/')
