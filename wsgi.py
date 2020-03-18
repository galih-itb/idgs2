from flask import Flask, render_template, request, session
from bs4 import BeautifulSoup
import requests
import os
import modulGS_OO as MG

application.secret_key = 'bismillaah'
application = Flask(__name__)

# specify the url
url = 'https://scholar.google.com/citations?hl=en&user=M1_IJLAAAAAJ'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
tes = MG.GS_Scraper(soup)
nama = tes.NamaAkun()

@application.route('/', methods=['GET', 'POST'])
def home():
    return index()

@application.route('/index', methods=['POST'])
def index():
     return "URL: " + url + "<br/><textarea>" + str(soup) + "</textarea>" + \
             "<br/>Nama: " + nama
    
if __name__ == "__main__":
    application.run()
