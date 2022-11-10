from requests import get
from bs4 import BeautifulSoup
from json import loads

messLyrics = []
songUrls = []

notLyrics = {';', 'Tillian', ']', 'Kurt Travis', 'Jonny Craig'}

for i in range (1, 9):
    response = get('https://genius.com/api/artists/49350/songs?page={}&sort=popularity'.format(i)).content
    parsedResponse = loads(response)
    for s in parsedResponse['response']['songs']:
        if "intrument" not in s['url'] and "Instrument" not in s['url']:
            songUrls.append(s['url'])

for page in songUrls:
    messStuff = []
    workingPage = get(page).content
    soupLyrics = BeautifulSoup(workingPage, "html.parser").find_all('div', attrs={"class":"Lyrics__Container-sc-1ynbvzw-6 YYrds"})

    if 'Jon Mess' not in soupLyrics[0].text or 'Jon Mess' not in soupLyrics[1].text:
        continue

    for lyricSheet in soupLyrics:
        italics = lyricSheet.find_all('i')

        veryMessy = False
        for ele in italics:
            if 'Jon Mess' in ele.text:
                veryMessy = True

        if veryMessy:
            for lyric in italics:
                if lyric.text != 'Jon Mess':
                    messLyrics.append(lyric.text)

        openBracketElements = []
        closeBracketElements = []

        for count, ele in enumerate(lyricSheet):
            if '[' in ele.text:
                openBracketElements.append(count)
                print("Open bracket: {}".format(ele.text))

        for count, ele in enumerate(lyricSheet):
            if ']' in ele.text:
                closeBracketElements.append(count)
                print("Closed bracket: {}".format(ele.text))

        messElements = []
        for count, ele in enumerate(lyricSheet):
            if 'Jon Mess' in ele.text and '[' in ele.text:
                messElements.append(count+1)

        slice = []
        for messNum in messElements:
            for bCount, brackNum in enumerate(openBracketElements):
                onlyMess, messy = False, False
                elmntText = ""
                if openBracketElements[bCount] != closeBracketElements[bCount]:
                    for eCount, elmnt in enumerate(lyricSheet):
                        if eCount in range(openBracketElements[bCount], closeBracketElements[bCount]+1):
                            elmntText += elmnt.text
                            if 'Jon Mess' in elmnt.text and '&' not in elmnt.text:
                                onlyMess = True
                            if elmnt.name == 'i' and 'Jon Mess' in elmntText:
                                messy = True
                                
                else:
                    for eCount, elmnt in enumerate(lyricSheet):
                        if eCount == bCount:
                            elmntText = elmnt.text
                        if elmnt.name == 'i' and 'Jon Mess' in elmntText:
                            messy = True
                if 'Jon Mess' in elmntText and '&' not in elmntText:
                    onlyMess = True

                #debug
                if onlyMess:
                    print("ONLY MESS")
                if messy:
                    print("MESSY")

                if brackNum == messNum and openBracketElements.index(brackNum) != len(openBracketElements)-1 and messNum != messElements[-1]:
                    if onlyMess:
                        newSlice = [messNum, closeBracketElements[bCount]]
                        if newSlice:
                            slice = newSlice
                    elif messy and not onlyMess:
                        for eCount, elmnt in enumerate(lyricSheet):
                            if elmnt.name == 'i':
                                newSlice = [messNum, closeBracketElements[bCount]]
                                if newSlice:
                                    slice = newSlice
                            
                        
                elif messNum == messElements[-1] and brackNum == closeBracketElements[-1]:
                    if onlyMess or (not messy and not onlyMess):
                        newSlice = [messNum, closeBracketElements[bCount]]
                        if newSlice:
                            slice = newSlice

        print(slice)
        
        if slice:
            for count, ele in enumerate(lyricSheet):
                for sl in range(slice[0], slice[1]):
                    if count == sl and ele.text and ele.text not in notLyrics:
                        print("Lyric number ", count, "is ", ele.text)

