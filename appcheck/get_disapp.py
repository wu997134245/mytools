import urllib
import requests
import json



a = requests.get(url = 'http://127.0.0.1:8888')

aj = json.loads(a.text)
print aj['uat']


#print aj
