#!/usr/bin/python
# -*- coding: latin-1 -*-

"""
TODO:
- Reordenar sem reload - FEITO
- Refiltrar sem reload
- http://code.google.com/appengine/docs/python/config/cron.html - FEITO
- http://code.google.com/appengine/docs/python/backends/overview.html
- http://tablesorter.com/docs/example-ajax.html
"""

stockattrs = ['pl', 'pvp', 'psr', 'divyield', 'pativo', 'pcapgiro', 'pebit',
    'pativcircliq','evebit', 'mrgebit', 'mrgliq', 'liqcor', 'roic', 'roe', 
    'liquidez', 'patrimliq', 'divbrutpatr', 'growth', 'diff']
       
indicatorsorder = {'pl':False, 'pvp':False, 'psr':False, 'divyield':True, 'pativo':False, 'pcapgiro':False, 
    'pebit':False,'pativcircliq':False,'evebit':False, 'mrgebit':True, 'mrgliq':True, 'liqcor':True, 'roic':True, 
    'roe':True, 'liquidez':True, 'patrimliq':True, 'divbrutpatr':False, 'growth':True, 'diff':True}
    
attrnames = {'pl':'P/L', 'pvp':'P/VP', 'psr':'PSR', 'divyield':'Div. Yield', 'pativo':'P/Ativos', 'pcapgiro':'P/Cap. Giro', 
    'pebit':'P/EBIT','pativcircliq':'P/Ativ Circ Liq','evebit':'EV/EBIT', 'mrgebit':'Marg. EBIT', 'mrgliq':'Marg. Liquida', 
    'liqcor':'Liquidez Corr', 'roic':'ROIC', 'roe':'ROE', 'liquidez':'Liquidez 2 meses', 'patrimliq':'Patrimonio Liquido', 
    'divbrutpatr':'Divida Bruta/Patrimonio', 'growth':'Crescimento', 'diff':'Oscilacao'}

attrtips = { 'pl' : "Preço da ação dividido pelo lucro por ação. O P/L é o número de anos que se levaria para reaver o capital aplicado na compra de uma ação, através do recebimento do lucro gerado pela empresa, considerando que esses lucros permaneçam constantes.",
'pvp' : "Preço da ação dividido pelo Valor Patrimonial por ação. Informa quanto o mercado está disposto a pagar sobre o Patrimônio Líquido da empresa.",
'pebit' : "Preço da ação dividido pelo EBIT por ação. EBIT é o Lucro antes dos Impostos e Despesas Financeiras. É uma boa aproximação do lucro operacional da empresa.",
'psr' : "Price Sales Ratio: Preço da ação dividido pela Receita Líquida por ação.",
'divyield' : "Dividend Yield: Dividendo pago por ação dividido pelo preço da ação. É o rendimento gerado para o dono da ação pelo pagamento de dividendos.",
'pativo' : "Preço da ação dividido pelos Ativos totais por ação.", 
'pcapgiro' : "Preço da ação dividido pelo capital de giro por ação. Capital de giro é o Ativo Circulante menos Passivo Circulante.", 
'pebit' : "Preço da ação dividido pelo EBIT por ação. EBIT é o Lucro antes dos Impostos e Despesas Financeiras. É uma boa aproximação do lucro operacional da empresa.",
'pativcircliq' : "Preço da ação dividido pelos Ativos Circulantes Líquidos por ação. Ativo Circ. Líq. é obtido subtraindo os ativos circulantes pelas dívidas de curto e longo prazo, ou seja, após o pagamento de todas as dívidas, quanto sobraria dos ativos mais líquidos da empresa (caixa, estoque, etc)",
'evebit' : "Valor da Firma (Enterprise Value) dividido pelo EBIT.",
'mrgebit' : "EBIT dividido pela Receita Líquida: Indica a porcentagem de cada R$1 de venda que sobrou após o pagamento dos custos dos produtos/serviços vendidos, das despesas com vendas, gerais e administrativas.",
'mrgliq' : "Lucro Líquido dividido pela Receita Líquida.", 
'liqcor' : "Ativo Circulante dividido pelo Passivo Circulante: Reflete a capacidade de pagamento da empresa no curto prazo.",
'roic' : "Retorno sobre o Capital Investido: Calculado dividindo-se o EBIT por (Ativos - Fornecedores - Caixa). Informa o retorno que a empresa consegue sobre o capital total aplicado.",
'roe' : "Retorno sobre o Patrimônio Líquido: Lucro líquido dividido pelo Patrimônio Líquido.",
'liquidez' : "Volume médio de negociação da ação nos últimos 2 meses (R$).",
'patrimliq' : "O patrimônio líquido representa os valores que os sócios ou acionistas têm na empresa em um determinado momento. No balanço patrimonial, a diferença entre o valor dos ativos e dos passivos e resultado de exercícios futuros representa o PL (Patrimônio Líquido), que é o valor contábil devido pela pessoa jurídica aos sócios ou acionistas.",
'divbrutpatr' : "Dívida Bruta total (Dívida+Debêntures) dividido pelo Patrimônio Líquido.",
'growth' : "Crescimento da Receita Líquida nos últimos 5 anos.",
'diff' : "Diferença do preço da ação com relação ao último dia."}

ibrx = ["AEDU3","ALLL3","AMBV4","AMIL3","BBAS3","BBDC3","BBDC4","BBRK3","BISA3","BRAP4","BRFS3","BRKM5","BRML3",
"BRPR3","BRSR6","BRTO4","BTOW3","BVMF3","CCRO3","CESP6","CIEL3","CMIG4","CPFE3","CPLE6","CRUZ3","CSAN3","CSMG3",
"CSNA3","CTIP3","CYRE3","DASA3","DTEX3","ECOR3","ELET3","ELET6","ELPL4","EMBR3","ENBR3","EVEN3","EZTC3","FIBR3",
"GETI4","GFSA3","GGBR4","GOAU4","GOLL4","HGTX3","HRTP3","HYPE3","ITSA4","ITUB4","JBSS3","KLBN4","LAME4","LIGT3",
"LLXL3","LREN3","MMXM3","MPLU3","MPXE3","MRFG3","MRVE3","MULT3","MYPK3","NATU3","ODPV3","OGXP3","PCAR4","PDGR3",
"PETR3","PETR4","POMO4","POSI3","PSSA3","QGEP3","RADL3","RAPT4","RDCD3","RENT3","RSID3","SANB11","SBSP3","SULA11",
"SUZB5","TAMM4","TBLE3","TCSA3","TIMP3","TNLP3","TNLP4","TOTS3","TRPL4","UGPA3","USIM3","USIM5","VAGR3","VALE3",
"VALE5","VIVT4","WEGE3"]
