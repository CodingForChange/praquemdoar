import json
from TwitterAPI import TwitterAPI
from config import TWITTER_API_KEY, TWITTER_API_SECRET
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
from app.models import Doacao, Ong
from app.emails import tweet_email

api = TwitterAPI(TWITTER_API_KEY, TWITTER_API_SECRET,
                 TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

request = api.request('statuses/filter', {'track': 'praquemdoar'})

for tweet in request:
    if len(tweet['entities']['hashtags']) >= 2:
        twt = tweet['entities']['hashtags'][1]['text']
        doacoes = Doacao.query.filter(Doacao.tags.like('%' + twt + '%'))
        if doacoes.count() > 0:
            for doacao in doacoes:
                post = api.request('statuses/update', {'status': '@' + tweet['user']['screen_name'] + ' ' + doacao.nome + ' ' + doacao.get_url() + ' #' + doacao.ong.nickname})
    
        else:
            post = api.request('statuses/update', {'status': '@' + tweet['user']['screen_name'] + ' Veja ONGs que precisam de coisas http://www.praquemdoar.com.br'})
            ongs = Ong.query.all()
            for ong in ongs:
                tweet_email('[Pra Quem Doar] @' + tweet['user']['screen_name'] + ' Quer doar ' + twt + ' no Twitter', 
                              'Pra Quem Doar',
                              'no-reply@praquemdoar.com.br',
                              'O usuario do Twetter @' + tweet['user']['screen_name'] + ' quer doar ' + twt + '! Entre em contato caso tenha interesse!',
                              ong.email)
