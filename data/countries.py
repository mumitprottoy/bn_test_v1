import json

file = open('data/countries+cities.json', 'r')
country_list= json.loads(file.read())