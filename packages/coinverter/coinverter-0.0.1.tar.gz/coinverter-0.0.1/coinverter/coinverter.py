import requests
import json

def cotacao(de, para, valor = 1):

    url = 'http://economia.awesomeapi.com.br/json/last/' + de + '-' + para

    cotacao = requests.get(url).content

    dic_contacao = json.loads(cotacao)

    return float(dic_contacao[f'{de}{para}']["bid"]) * valor 

