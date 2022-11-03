from requests import get
from bs4 import BeautifulSoup
from json import loads

songPageList = []
for i in range (1, 9):
    response = get('https://genius.com/api/artists/49350/songs?page={}&sort=popularity'.format(i)).content
    parsedResponse = loads(response)
    for s in parsedResponse['response']['songs']:
        songPageList.append(s)

print(len(songPageList))
