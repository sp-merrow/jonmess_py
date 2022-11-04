from requests import get
from bs4 import BeautifulSoup
from json import loads

messLyrics = []
songUrls = []
for i in range (1, 9):
    response = get('https://genius.com/api/artists/49350/songs?page={}&sort=popularity'.format(i)).content
    parsedResponse = loads(response)
    for s in parsedResponse['response']['songs']:
        if "intrument" not in s['url'] and "Instrument" not in s['url']:
            songUrls.append(s['url'])

for page in songUrls:
    messStuff = []
    workingPage = get(page).content
    soupLyrics = BeautifulSoup(workingPage, "html.parser").find('div', attrs={"class":"Lyrics__Container-sc-1ynbvzw-6 YYrds"})

    if 'Jon Mess' not in soupLyrics.text:
        continue

    italics = soupLyrics.find_all('i')

    messy = False
    for ele in italics:
        if 'Jon Mess' in ele.text:
            messy = True

    if messy:
        for lyric in italics:
            if lyric.text != 'Jon Mess':
                messLyrics.append(lyric.text)

    openBracketElements = []

    for count, ele in enumerate(soupLyrics):
        if '[' in ele.text:
             openBracketElements.append(count)

    messElements = []
    for count, ele in enumerate(soupLyrics):
        if 'Jon Mess' in ele.text and '&' not in ele.text and '[' in ele.text:
            messElements.append(count)

    slices = []
    for messNum in messElements:
        for bCount, brackNum in enumerate(openBracketElements):
            if brackNum == messNum and openBracketElements.index(brackNum) != len(openBracketElements)-1 and messNum != messElements[-1]:
                slices.append([messNum, openBracketElements[bCount+1]])
            elif messNum == messElements[-1] and brackNum == openBracketElements[-1]:
                slices.append([messNum, "e"])

    print(slices)
