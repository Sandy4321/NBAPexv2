import sys
from sys import argv
import urllib.request
from bs4 import BeautifulSoup as bs

script, command = argv

if command == "teams":
    url = "http://www.basketball-reference.com/teams/?lid=front_qi_teams"
    response = urllib.request.urlopen(url)
    soup = bs(response.read().decode('utf-8','ignore'),'html.parser')
    #print(soup.prettify().encode(sys.stdout.encoding, errors='replace'))
    table = soup.find("table", {"id": "active"})
    rows = table.find_all("tr")
    for r in rows:
    	cells = r.find_all("td")
    	if cells:
    		if cells[0].a:
    			print(cells[0].a.get('href'))

elif command == "refs":
    url = "http://www.basketball-reference.com/referees"
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    soup = bs(''.join(str_response))
    table = soup.find('table', attrs = {'id':'referees'})
    t_body = table.find('tbody')
    rows = soup.find_all('tr')

    for row in rows:
        link = row.find('a')
        if(link):
            href = link.get('href')
            if href and "referees" in href:
                print(href)
        #    link = row.find('a')
        #    r_id = link['href'][10:-5]
            #print(r_id)
            #attributes = row.find_all('td')