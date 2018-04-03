from bs4 import BeautifulSoup
import requests
import os

baseUrl = r"http://www.canalrcn.com/"

def programsUrl():
    return os.path.join(baseUrl, "programas")

def titleAndLinkFor(programHtml):
    urlTag = programHtml.find("a")
    return urlTag.contents[0], urlTag["href"]



result = requests.get(programsUrl())
soup = BeautifulSoup(result.content, "html.parser")

programs = soup.find_all("div", "views-field-title") # "views-field-field-imagen-programa")
for program in programs:
    print(titleAndLinkFor(program))




