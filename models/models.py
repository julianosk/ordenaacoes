#!/usr/bin/env python

from google.appengine.ext import db


class StockUpdate(db.Model):
    last = db.StringProperty(required=True)
    updated_on = db.DateTimeProperty(auto_now_add = 1)

class Stock(db.Model):
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    
    quote = db.FloatProperty() #Cotacao
    pl = db.FloatProperty() #P/L - Menor Melhor - entre 1 e 30
    pvp = db.FloatProperty() #P/VP - Menor Melhor - Entre 0 e 20
    psr = db.FloatProperty() #PSR - Menor Melhor
    divyield = db.FloatProperty() #Dividend Yield - Maior Melhor
    pativo = db.FloatProperty() #P/Ativo - Menor Melhor
    pcapgiro = db.FloatProperty() #P/Cap.Giro - Menor Melhor
    pebit = db.FloatProperty() #P/EBIT - Menor Melhor
    pativcircliq = db.FloatProperty() #P/Ativ Circ. Liq - Menor Melhor
    evebit = db.FloatProperty() #EV/EBIT - Menor Melhor 
    mrgebit = db.FloatProperty() #Mrg Ebit - Maior Melhor
    mrgliq = db.FloatProperty() #Mrg Liq. - Maior Melhor
    liqcor = db.FloatProperty() #Liquidez Corrente - Maior Melhor > 1
    roic = db.FloatProperty() #ROIC - Maior Melhor
    roe = db.FloatProperty() #ROE - Maior Melhor - Maior que 0
    liquidez = db.FloatProperty() #Liquidez 2 meses - Maior Melhor - Maior que 100.000
    patrimliq = db.FloatProperty() #Patrimonio Liquido - Maior Melhor
    divbrutpatr = db.FloatProperty() #Div. Brut/ Patrim. - Menor Melhor
    growth = db.FloatProperty() #Crescimento - Maior Melhor > 5%
    diff = db.FloatProperty() #Diferenca entre a ultima cotacao e a anterior
    oscillation = db.FloatProperty(default=0.0) #Oscilacao entre a ultima cotacao e a anterior


    posquote = db.IntegerProperty()
    pospl = db.IntegerProperty()
    pospvp = db.IntegerProperty()
    pospsr = db.IntegerProperty()
    posdivyield = db.IntegerProperty()
    pospativo = db.IntegerProperty()
    pospcapgiro = db.IntegerProperty()
    pospebit = db.IntegerProperty()
    pospativcircliq = db.IntegerProperty()
    posevebit = db.IntegerProperty() 
    posmrgebit = db.IntegerProperty()
    posmrgliq = db.IntegerProperty()
    posliqcor = db.IntegerProperty()
    posroic = db.IntegerProperty()
    posroe = db.IntegerProperty()
    posliquidez = db.IntegerProperty()
    pospatrimliq = db.IntegerProperty()
    posdivbrutpatr = db.IntegerProperty()
    posgrowth = db.IntegerProperty()

    possum = db.IntegerProperty()    

