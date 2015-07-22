from django.shortcuts import render_to_response
from datetime import date
import urllib.request
import json
from bs4 import BeautifulSoup as bs
from stats.models import *
from stats.status_utils import *
# Create your views here.

def seed_teams():
	#Need to check this range
	for t in range(737,767):
		create_team_from_web(t)

def seed_players():
    url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2014-15"
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    info = data['resultSets'][0]['rowSet']
    i=0
    for index in range(i,len(info)):
        create_player_from_web(p_id = info[index][0])
        print(i)
        i += 1
        
def seed_coaches():
    url = "http://www.basketball-reference.com/coaches/NBA_stats.html"
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    soup = bs(''.join(str_response))
    table = soup.find('table', attrs = {'id':'coaches'})
    t_body = table.find('tbody')
    rows = t_body.find_all('tr')

    for row in rows:
        if(row.find('a')):
            link = row.find('a')
            c_id = link['href'][9:-5]
            attributes = row.find_all('td')
            Coach().create_coach_from_web(c_id=c_id,attr=attributes)

def seed_refs():
    url = "http://www.basketball-reference.com/referees"
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    soup = bs(''.join(str_response))
    table = soup.find('table', attrs = {'id':'referees'})
    t_body = table.find('tbody')
    rows = t_body.find_all('tr')

    for row in rows:
        if(row.find('a')):
            link = row.find('a')
            r_id = link['href'][10:-5]
            print(r_id)
            #attributes = row.find_all('td')

def seed_individuals(request):
	seed_teams()
	seed_players()
	seed_coaches()
	seed_referees()
	return render_to_response('seed_individuals.html')
