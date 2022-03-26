#!/usr/bin/python

import os
import csv
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


url = 'https://www.fundsexplorer.com.br/ranking'

# Data Cleansing
# 'R$' => ''
# '%' => ''
# '.0' => ''
# '.' => ''
# ',' => '.'
# 'N/A' => ''

print("Starting...{}".format(datetime.now()))

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

data = []
table = soup.find(id="table-ranking")

table_head = table.find('thead')

rows = table_head.find_all('tr')
for row in rows:
    cols = row.find_all('th')
    colsd = [ele.get_text(separator=" ").strip() for ele in cols]
    data.append([ele for ele in colsd])

table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    colsd = [ele.text.replace('R$','').replace('%','').replace('.0','').replace('.','').replace('N/A','').replace(',','.').strip() for ele in cols]
    data.append([ele for ele in colsd])

out_dir = 'out/'
os.makedirs(out_dir, exist_ok=False)
file = open(out_dir+"fii.csv", "w")

wtr = csv.writer(file, delimiter=';', lineterminator='\n')
for x in data : wtr.writerow(x)

file.close()

print("Finish...{}".format(datetime.now()))

time.sleep(1)
