from bs4 import BeautifulSoup as BS
from zipfile import ZipFile
import urllib.request
import os
import re
import time


def exitscript(st):
    os.system('cls')
    print(st)
    print("Exiting in 5 secs ...")
    time.sleep(5)
    exit()

os.system('cls')
name = input("Enter name of the movie --> ")
html = urllib.request.urlopen("http://www.yifysubtitles.com/search?q="+("+".join(name.split(" "))))
soup = BS(html, "html.parser")

if not soup.find('div', {'style': 'text-align:center;'}) is None:
    if soup.find('div', {'style': 'text-align:center;'}).text == "no results":
        exitscript("\033[1;31;40m No results found")

list1 = soup.findAll('li', {'class': 'media media-movie-clickable'})
list2 = BS(str(list1), "html.parser").findAll('div', {'class': 'media-body'})
url = ""
print("Choose from the list --> ")

for i in range(len(list1)):
    os.system('cls')
    print("\033[1;37;40m Is this the movie ? {y/n}")
    print("\033[1;32;40m Movie --> "+soup.findAll('h3', {'class': 'media-heading'})[i].text)
    print("\033[1;32;40m Year --> "+BS(str(BS(str(list2[i]), "html.parser").findAll('div', {'class': 'col-xs-12'})[2]), "html.parser").findAll('span', {'class': 'movinfo-section'})[0].text[:4])
    print("\033[1;32;40m Genre --> "+soup.findAll('div', {'itemprop': 'genre'})[i].text)
    print("\033[1;32;40m Description --> "+soup.findAll('span', {'itemprop': 'description'})[i].text)
    temp = input()
    if temp == "y" or temp == "Y":
        url = BS(str(list2[i]), "html.parser").find('a').get('href')
        break
    else:
        os.system('cls')

if url == "":
    exitscript("\033[1;31;40m No results found")

os.system('cls')
print("\033[1;34;40m Processing - Stage(I)")
html = urllib.request.urlopen("http://www.yifysubtitles.com"+url)
soup = BS(html, "html.parser")
dict1 = {}

flags = BS(str(soup.find('tbody').findAll('td', {'class': 'flag-cell'})), "html.parser")

for i in range(len(soup.find('tbody').findAll('tr'))):
    if BS(str(flags), "html.parser").findAll('span', {'class': 'sub-lang'})[i].text == "English":
        dict1[BS(str(soup.find('tbody').findAll('td', {'class': 'rating-cell'})), "html.parser").findAll('span')[i].text] = i

if dict == {}:
    exitscript("\033[1;31;40m No further results found")

dict1 = {int(v): int(k) for k, v in dict1.items()}
i = max(dict1, key=dict1.get)
url = BS(str(soup.find('tbody').findAll('td', {'class': 'download-cell'})), "html.parser").findAll('a', attrs={'href': re.compile("/subtitles/")})[i].get('href')

os.system('cls')
print("\033[1;35;40m Processing - Stage(II)")
html = urllib.request.urlopen("http://www.yifysubtitles.com"+url)
soup = BS(html, "html.parser")
url = soup.find('a', {'class': 'btn-icon download-subtitle'}).get('href')

os.system('cls')
print("\033[1;36;40m Processing - Stage(III)")
urllib.request.urlretrieve(url, "subtitle.zip")
zip = ZipFile("subtitle.zip")
zip.extractall()
zip.close()
os.remove("subtitle.zip")

for file in os.listdir(os.getcwd()):
    if file.endswith(".srt"):
        subname = file

for file in os.listdir(os.getcwd()):
    if file.endswith(".3g2") or file.endswith(".3gp") or file.endswith(".amv") or file.endswith(".asf") or file.endswith(".avi") or file.endswith(".drc") or file.endswith(".flv") or file.endswith(".gifv") or file.endswith(".m4v") or file.endswith(".mkv") or file.endswith(".mng") or file.endswith(".mov") or file.endswith(".qt") or file.endswith(".mp4") or file.endswith(".mpg") or file.endswith(".mpeg") or file.endswith(".nsv") or file.endswith(".ogv") or file.endswith(".ogg") or file.endswith(".rm") or file.endswith(".rmvb") or file.endswith(".vob") or file.endswith(".webm") or file.endswith(".wmv"):
        filename = os.path.splitext(file)[0]
        os.rename(subname, filename+".srt")

os.remove("IntelliSubDownloader.py")

exitscript("\033[1;32;40m Subtitle - Downloaded and Renamed")
