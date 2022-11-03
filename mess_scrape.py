from requests import get
from bs4 import BeautifulSoup
from json import loads

songUrls = []
for i in range (1, 9):
    response = get('https://genius.com/api/artists/49350/songs?page={}&sort=popularity'.format(i)).content
    parsedResponse = loads(response)
    for s in parsedResponse['response']['songs']:
        songUrls.append(s['url'])

for url in songUrls:
    print(url)
    # response = get(url).text
    # print(parsedResponse)
