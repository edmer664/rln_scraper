#! python3
import requests
from bs4 import *
from os import makedirs,getcwd,path

#TODO catch novel title
novel_title = input('Novel Title:\n').lower()
chapter_max = int(input("Chapters to download:\n"))
#* Url format
novel_title = novel_title.replace(" ","-")
#*make directory
makedirs(f'.\\{novel_title}')
url = f"https://www.readlightnovel.org/{novel_title}/"
#TODO iterate chapters
for chapter in range(1,chapter_max):
    currentURL = url + f"chapter-{chapter}"
    #*get response
    response = requests.get(currentURL)
    soup = BeautifulSoup(response.text,'html.parser')
    text = soup.select(".desc")
#TODO bind all files    
    content = ""
    for char in text:
        #!print(char.getText())
        content += char.getText()
    with open(path.join(f"{getcwd()}",f"{novel_title}\\{novel_title}-chapter{chapter}.txt"),'x',encoding="utf-8") as file:
        file.write(content)