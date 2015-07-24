import logging
from django.shortcuts import render_to_response
from datetime import date
import urllib.request
import json
from bs4 import BeautifulSoup as bs
from stats.models import *
from stats.stats_utils import *
# Create your views here.

log = logging.getLogger(__name__)

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
    i=1047
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
            create_coach_from_web(c_id=c_id,attr=attributes)

def seed_player_advanced(player):
    all_seasons = []
    for yr in range(player.from_year,player.to_year+1):
        if yr >= 1996:
            for season_type in ["Regular+Season","Playoffs"]:
                season = make_season_str(yr)
                url = "http://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=%s&PlusMinus=N&Rank=N&Season=%s&SeasonSegment=&SeasonType=%s&VsConference=&VsDivision=" %(player.player_id,season,season_type)
                response = urllib.request.urlopen(url)
                str_response = response.readall().decode('utf-8')
                data = json.loads(str_response)
                stats = standardize_player_data(data['resultSets'][0],adv_flag=True,player=player)
                stats['season_type'] = season_type

    return all_seasons

def seed_player_seasons_data(player, split):
    if split == "Advanced":
        all_seasons = seed_player_advanced(player_id)
    else:
        url = "http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=%s&PlayerID=%s" %(split,player.player_id)
        response = urllib.request.urlopen(url)
        str_response = response.readall().decode('utf-8')
        data = json.loads(str_response)
        
        reg_seasons = standardize_player_data(data['resultSets'][0],player=player)
        career_reg_season = standardize_player_data(data['resultSets'][1],player=player)
        post_seasons = standardize_player_data(data['resultSets'][2],player=player)
        career_post_season = standardize_player_data(data['resultSets'][3],player=player)
        all_star_seasons = standardize_player_data(data['resultSets'][4],player=player)
        career_as_season = standardize_player_data(data['resultSets'][5],player=player)
        all_seasons = reg_seasons + career_reg_season + post_seasons + career_post_season + all_star_seasons + career_as_season
        
        for s in all_seasons:
            log.debug(s)
            create_player_season(split, s)

def seed_team_seasons_data(split):
    for year in range(1996,2015):
        print(year)
        for season_type in ["Regular+Season","Playoffs"]:
            season = make_season_str(year)
            url = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=%s&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=%s&SeasonSegment=&SeasonType=%s&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=" %(split, season,season_type)
            response = urllib.request.urlopen(url)
            str_response = response.readall().decode('utf-8')
            data = json.loads(str_response)
            data = data['resultSets'][0]
            seasons = standardize_team_data(data,season_type,year)
            for s in seasons:
                create_team_season(split,s)

def seed_individuals(request):
    #seed_teams()
    #seed_players()
    #seed_coaches()
    return render_to_response('seed_individuals.html')

def seed_player_seasons(request):
    players = Player.objects.all()
    for p in players:
        log.debug("Creating seasons for %s" %p.display_first_last)
        seed_player_seasons_data(p,"PerGame")
        seed_player_seasons_data(p,"Totals")
        seed_player_seasons_data(p,"Advanced")
    return render_to_response('seed_player_seasons.html')

def seed_team_seasons(request):
    seed_team_seasons_data("PerGame")
    seed_team_seasons_data("Totals")
    seed_team_seasons_data("Advanced")
    return render_to_response('seed_team_seasons.html')