from bs4 import BeautifulSoup
import requests
import dateutil.parser
import datetime
import pytz

utc=pytz.UTC
nameList = []

header_options = { 'User-Agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_3 rv:4.0) Gecko/20170606 Firefox/36.0' }
def grab_names(min_searches):
  global nameList

  res = requests.get('https://namemc.com/minecraft-names?sort=asc&length_op=&length=3&lang=&searches=100')
  
  if(res.status_code == 200):
    soup = BeautifulSoup(res.text, features='lxml')

    table_parent = soup.find('div', {'class': 'p-0'})
    row_elements = table_parent.findChildren('div', recursive=False)
    
    nameList = [row.get_text().split('\n')[1] for row in row_elements]
  else:
    print('[!] Status code wasnt 200, invalid URL maybe?')
    exit(0)


def grab_change_date():
  for name in nameList:
    res = requests.get(f'https://namemc.com/search?q={name}')
    if(res.status_code == 200):
      soup = BeautifulSoup(res.text, features='lxml')

      name_changes = soup.findAll('div', 'col-md-6 col-lg-7 order-md-1')
      name_change_body = soup.find('div', 'card-body py-1 position-relative')
      change_times = name_change_body.findAll('time')

      change_date = dateutil.parser.parse(change_times[len(change_times) - 1].get_text())
      if (change_date > utc.localize(datetime.datetime(2021, 1, 1, 0, 0))):
        print(f'[+] {name} : Possible Microsoft Account')

if __name__ == '__main__':
  try:
    min_searches = int(input('Minimum Searches > '))
    grab_names(min_searches)
    grab_change_date()
  except ValueError:
    print('[!] Invalid Input, must be type Integer.')
