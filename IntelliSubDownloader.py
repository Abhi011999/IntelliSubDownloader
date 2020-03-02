from bs4 import BeautifulSoup as BS
import zipfile
import urllib.request
import os
import re
import time

red = '\033[91m'
green = '\033[92m'
blue = '\033[94m'
yellow = '\033[93m'
url = ""
dict1 = {}
found  = 0

def exitscript(st):
    os.system('cls')
    print(st)
    print("Exiting in 5 secs ...")
    time.sleep(5)
    exit()

os.system('cls')

name = input("Enter name of the movie --> ")
html = urllib.request.urlopen("http://www.yifysubtitles.com/search?q=" + ("+".join(name.split(" "))))
soup = BS(html, "html.parser")

if not soup.find('div', {'style': 'text-align:center;'}) is None:
    if soup.find('div', {'style': 'text-align:center;'}).text == "no results":
        exitscript(red + "No results found")

list1 = soup.findAll('li', {'class': 'media media-movie-clickable'})
list2 = BS(str(list1), "html.parser").findAll('div', {'class': 'media-body'})

for i in range(len(list1)):
    os.system('cls')
    print(yellow + "Is this the movie ? (y for yes , enter to skip)\n")
    print(yellow + "Movie --> " + green + soup.findAll('h3', {'class': 'media-heading'})[i].text)
    print(yellow + "Year --> " + green + BS(str(BS(str(list2[i]), "html.parser").findAll('div', {'class': 'col-xs-12'})[2]), "html.parser").findAll('span', {'class': 'movinfo-section'})[0].text[:4])
    print(yellow + "Genre --> " + green + soup.findAll('div', {'itemprop': 'genre'})[i].text)
    print(yellow + "Description --> " + green + soup.findAll('span', {'itemprop': 'description'})[i].text)
    temp = input()
    if temp == "y" or temp == "Y":
        url = BS(str(list2[i]), "html.parser").find('a').get('href')
        break
    else:
        os.system('cls')

if url == "":
    exitscript(red + "No results found")

os.system('cls')

print(yellow + "Retrieving language - " + blue + "Stage(I)")
html = urllib.request.urlopen("http://www.yifysubtitles.com" + url)
soup = BS(html, "html.parser")

flags = BS(str(soup.find('tbody').findAll('td', {'class': 'flag-cell'})), "html.parser")

for i in range(len(soup.find('tbody').findAll('tr'))):
    if BS(str(flags), "html.parser").findAll('span', {'class': 'sub-lang'})[i].text == "English":
        dict1[BS(str(soup.find('tbody').findAll('td', {'class': 'rating-cell'})), "html.parser").findAll('span')[i].text] = i

if dict == {}:
    exitscript(red + "No further results found")

dict1 = {int(v): int(k) for k, v in dict1.items()}
i = max(dict1, key=dict1.get)
url = BS(str(soup.find('tbody').findAll('td', {'class': 'download-cell'})), "html.parser").findAll('a', attrs={'href': re.compile("/subtitles/")})[i].get('href')

os.system('cls')

print(yellow + "Downloading subtitle - " + blue + "Stage(II)")
html = urllib.request.urlopen("http://www.yifysubtitles.com" + url)
soup = BS(html, "html.parser")
url = soup.find('a', {'class': 'btn-icon download-subtitle'}).get('href')

os.system('cls')

print(yellow + "Extracting and renaming - " + blue + "Stage(III)")
urllib.request.urlretrieve(url, "subtitle.zip")
zip = zipfile.ZipFile('subtitle.zip' , mode='r')

for zip_info in zip.infolist():
        if zip_info.filename[-1] == '/':
            continue
        zip_info.filename = os.path.basename(zip_info.filename)
        zip.extract(zip_info, ".")

zip.close()
os.remove("subtitle.zip")

for file in os.listdir():
    if file.endswith(".srt"):
        subname = file

for file in os.listdir():
    if file.endswith(".3g2") or file.endswith(".3gp") or file.endswith(".amv") or file.endswith(".asf") or file.endswith(".avi") or file.endswith(".drc") or file.endswith(".flv") or file.endswith(".gifv") or file.endswith(".m4v") or file.endswith(".mkv") or file.endswith(".mng") or file.endswith(".mov") or file.endswith(".qt") or file.endswith(".mp4") or file.endswith(".mpg") or file.endswith(".mpeg") or file.endswith(".nsv") or file.endswith(".ogv") or file.endswith(".ogg") or file.endswith(".rm") or file.endswith(".rmvb") or file.endswith(".vob") or file.endswith(".webm") or file.endswith(".wmv"):
        filename = os.path.splitext(file)[0]
        os.rename(subname, filename+".srt")
        found = 1

if found == 1:
    exitscript(green + "Subtitle - Downloaded and Renamed")
else:
    os.remove(subname)
    exitscript(red + "No supported media files found!")
