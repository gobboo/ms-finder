from bs4 import BeautifulSoup
import requests
import dateutil.parser
from datetime import datetime
import pytz

utc=pytz.UTC

def format_time(time):
  return time.replace('-', '').replace(':', '').split('.')[0] + "Z"

nameList = []
header_options = { 'User-Agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_3 rv:4.0) Gecko/20170606 Firefox/36.0' }
time = format_time(datetime.isoformat(datetime.now()))

def grab_names(min_searches, pages):
  global time
  global nameList

  for x in range(pages):
    res = requests.get(f'https://namemc.com/minecraft-names?time={time}&sort=asc&length_op=ge&length=3&lang=en&searches={min_searches}', headers=header_options)
    if(res.status_code == 200):
      soup = BeautifulSoup(res.text, features='lxml')

      table_parent = soup.find('div', {'class': 'p-0'})
      row_elements = table_parent.findChildren('div', recursive=False)
      
      nameList = nameList + [row.get_text().split('\n')[1] for row in row_elements]

      nextTime = row_elements[len(row_elements) - 1].find('time')['datetime']
      time = format_time(nextTime)
    else:
      print('[!] Status code wasnt 200, invalid URL maybe?')
      exit(0)

def grab_change_date():
  for name in nameList:
    res = requests.get(f'https://namemc.com/search?q={name}')
    if(res.status_code == 200):
      soup = BeautifulSoup(res.text, features='lxml')

      name_change_body = soup.find('div', 'card-body py-1 position-relative')
      change_times = name_change_body.findAll('time')

      change_date = dateutil.parser.parse(change_times[len(change_times) - 1].get_text())
      if (change_date > utc.localize(datetime(2021, 1, 1, 0, 0))):
        print(f'[+] {name} : Possible Microsoft Account')

if __name__ == '__main__':
  try:
    min_searches = int(input('Minimum Searches > '))
    pages = int(input('How many Pages > '))
    grab_names(min_searches, pages)
    grab_change_date()
  except ValueError:
    print('[!] Invalid Input, must be type Integer.')
