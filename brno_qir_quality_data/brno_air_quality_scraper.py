from bs4 import BeautifulSoup as bs
import requests
from csv import writer

url = 'https://www.brnenskeovzdusi.cz/brno-detska-nemocnice/'
result = requests.get(url).text
doc = bs(result, 'html.parser')

station_name = doc.find('h1').find('strong').text

rows_raw = doc.find_all('tr', id=lambda value: value and value.startswith("radek"))
rows_clean = [current_row.text.strip().split('\n') for current_row in rows_raw]
[row.insert(0, station_name) for row in rows_clean]

header_raw_text = doc.find('table', class_ = "detail stanice-tabulka").findChild().text
header = header_raw_text.strip().split('\r')
header = [column_name.strip().replace('\n', ' ') for column_name in header]
header.insert(0, 'Name of station')

with open(f'{station_name}_info.csv', 'w', encoding='utf-8', newline='') as file:
    thewriter = writer(file)
    thewriter.writerow(header)
    thewriter.writerows(rows_clean)
    