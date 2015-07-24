import urllib.request
import json
from datetime import date
from stats.models import *
#Utility methods primarily used for seed the database

def get_team_info_from_web(team_id):
    url = "http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular+Season&TeamID=1610612"+str(team_id)+"&season=2014-15"
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    #This goofy thing returns a list containing the relevant team information
    return data['resultSets'][0]['rowSet'][0]

def create_team_from_web(t_id):
    info = get_team_info_from_web(team_id=t_id)
    team = Team(team_id=info[0], team_city=info[2], team_name=info[3],
    			 team_abbreviation = info[4], team_conference=info[5], 
    			 team_division=info[6], team_code=info[7],wins=info[8],
    			 losses=info[9],w_pct=info[10],conf_rank=info[11],
    			 div_rank=info[12],min_year=int(info[13]),max_year=int(info[14]))
    team.save()

def extract_values(attrib):
    values = []
    for a in attrib:
        values.append(a.get_text())
    return values

def create_coach_from_web(c_id, attr):
    vals = extract_values(attrib=attr)
    names = vals[1].split(' ')
    print(vals)
    if(vals[10] == ''):
        print("No playoff games")
        coach = Coach(coach_id = c_id,first_name=names[0],last_name=names[1],display_first_last=vals[1],from_year=vals[2],to_year=vals[3],
        years = vals[4], reg_season_games=vals[5],reg_season_wins=vals[6],reg_season_losses=vals[7],reg_season_w_pct=vals[8],above_500=vals[9])
    else:
        if vals[14]=='' or vals[15] == '':
            if vals[13] =='':
                coach = Coach(coach_id = c_id,first_name=names[0],last_name=names[1],display_first_last=vals[1],from_year=vals[2],to_year=vals[3],
                    years = vals[4], reg_season_games=vals[5],reg_season_wins=vals[6],reg_season_losses=vals[7],reg_season_w_pct=vals[8],above_500=vals[9])
            else:
                coach = Coach(coach_id = c_id,first_name=names[0],last_name=names[1],display_first_last=vals[1],from_year=vals[2],to_year=vals[3],
                    years = vals[4], reg_season_games=vals[5],reg_season_wins=vals[6],reg_season_losses=vals[7],reg_season_w_pct=vals[8],above_500=vals[9],
                    post_season_games=vals[10],post_season_wins=vals[11],post_season_losses=vals[12],post_season_w_pct=vals[13])
        else:
            if vals[13] =='':
                coach = Coach(coach_id = c_id,first_name=names[0],last_name=names[1],display_first_last=vals[1],from_year=vals[2],to_year=vals[3],
                    years = vals[4], reg_season_games=vals[5],reg_season_wins=vals[6],reg_season_losses=vals[7],reg_season_w_pct=vals[8],above_500=vals[9],
                    post_season_games=vals[10],post_season_wins=vals[11],post_season_losses=vals[12],conference_champs=vals[14],league_champs=vals[15])
            else:
                coach = Coach(coach_id = c_id,first_name=names[0],last_name=names[1],display_first_last=vals[1],from_year=vals[2],to_year=vals[3],
                years = vals[4], reg_season_games=vals[5],reg_season_wins=vals[6],reg_season_losses=vals[7],reg_season_w_pct=vals[8],above_500=vals[9],
                post_season_games=vals[10],post_season_wins=vals[11],post_season_losses=vals[12],post_season_w_pct=vals[13],conference_champs=vals[14],league_champs=vals[15])
    coach.save()

def convert_height_to_int(height_string):
    if len(height_string) > 0:
        vals = height_string.split('-')
        return 12 * int(vals[0]) + int(vals[1])
    return 0

def convert_datetime_string_to_date_instance(date_string):
    #Chomps off the end of the string which is universally 'T00:00:00'
    if date_string:
        vals = date_string[:10].split('-')
        return date(int(vals[0]),int(vals[1]),int(vals[2]))

def sanitize_player_data(to_fix):
    to_fix[6] =convert_datetime_string_to_date_instance(to_fix[6])
    to_fix[10] = convert_height_to_int(to_fix[10])
    print("Player id = %s" %to_fix[0])
    print("Player name: %s" %to_fix[3])
    if not to_fix[7]:
        to_fix[7] = "N/A"
    print("to_fix[13] = %s" %to_fix[13])
    #weight
    if not(to_fix[11] =='' or to_fix[11] == ' '):
        to_fix[11] = int(to_fix[11])
    else:
        to_fix[11] = 0
    #jersey
    if not(to_fix[13] =='' or to_fix[13] == ' '):
        vals = to_fix[13].split('-')
        print("vals[0] = %s" %vals[0])
        to_fix[13] = int(vals[0][:2])
    else:
        to_fix[13] = 0
    #from_year
    if (to_fix[22] =='' or to_fix[22] == ' '):
        to_fix[22] = 0
    #to_year
    if (to_fix[23] =='' or to_fix[23] == ' '):
        to_fix[13] = 0
    return to_fix

def get_player_info_from_web(player_id):
    url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID="+str(player_id)+"&SeasonType=Regular+Season"
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    #This goofy thing returns a list containing the relevant player information
    return data['resultSets'][0]['rowSet'][0]

def create_player_from_web(p_id):
    info = sanitize_player_data(get_player_info_from_web(player_id=p_id))
    for i in info:
        print("Type: %s Val: %s" %(type(i), i))
    p = Player.objects.filter(player_id = info[0]).first()
    if not p:
        team = Team.objects.get(team_id=info[16])

        player = Player(player_id=info[0],first_name=info[1],last_name=info[2], display_first_last=info[3],display_last_comma_first=info[4],display_fi_last=info[5],birthdate=info[6],
                        school=info[7],country=info[8],last_affiliation=info[9], height=info[10],weight=info[11],season_exp=info[12],jersey=info[13],
                        position=info[14],roster_status=info[15],team=team,team_name=info[17],team_abbreviation=info[18],team_code=info[19],team_city=info[20],playercode=info[21],from_year=info[22],
                        to_year=info[23])
        player.save()

#Start season methods
def make_season_int(season):
 if type(season) == str:
      return int(season.split("-")[0])
 else:
      return season

def make_season_str(year):
    if year == 1999:
        return "1999-00"
    suf = int(str(year)[2:])
    suf += 1
    if 2000 <= year <= 2008:
        return "%s-%s" %(str(year),str(suf).rjust(2,'0'))
    return "%s-%s" %(str(year),str(suf))

def get_player_age(player,year):
     return year - player.birthdate.year

def convert_dict_keys_to_lowercase(data):
    ret_dict = {}
    for k,v in data.items():
        if (not k == "GROUP_SET") and (not k== "GROUP_VALUE") and (not k== "CFID") and (not k== "CFPARAMS"): 
            ret_dict[k.lower()] = v
    return ret_dict

def standardize_player_data(data,player,adv_flag=False):
    seasons_list = []
    hdrs = data['headers']
    plr_name = Player.objects.get(player_id = player.player_id).display_first_last
    if adv_flag:
        #It turns out that the row set is a list that contains a single list
        d = dict(zip(hdrs,data['rowSet'][0]))
        #Here is where we need to set missing fields
        d['PLAYER_ID'] = player.player_id
        d['PLAYER_NAME'] = plr_name
        d['SEASON_ID'] = make_season_int(d['GROUP_VALUE'])
        d['PLAYER_AGE'] = get_player_age(player=player, year = d['SEASON_ID'])
        d['CAREER_FLAG'] = False
        seasons_list.append(convert_dict_keys_to_lowercase(d))
    if data['rowSet']:
        for s in data['rowSet']:
            d = dict(zip(hdrs,s))
            d['PLAYER_NAME'] = plr_name
            if "Career" in data['name']:
                d['SEASON_ID'] = 0
                d['TEAM_ABBREVIATION'] = Team.objects.get(team_id = d['TEAM_ID']).team_abbreviation
                d['CAREER_FLAG'] = True
            else:
                d['CAREER_FLAG'] = False
                d['SEASON_ID'] = make_season_int(d['SEASON_ID'])
            if "Regular" in data['name']:
                d['SEASON_TYPE'] = "regular"
            elif "Post" in data['name']:
                d['SEASON_TYPE'] = "post"
            elif "AllStar" in data['name']:
                d['SEASON_TYPE'] = "all_star"
            seasons_list.append(convert_dict_keys_to_lowercase(d))
     #We now have a list of dicts that each specify a season
    return seasons_list

def standardize_team_data(data, season_type,year):
    seasons_list = []
    hdrs = data['headers']
    if data['rowSet']:
        for s in data['rowSet']:
            d = dict(zip(hdrs,s))
            d['SEASON_TYPE'] = season_type
            d['SEASON_ID'] = year
            seasons_list.append(convert_dict_keys_to_lowercase(d))
    return seasons_list

def create_player_season(split, data):
    if split == "PerGame":
        s = PlayerPerGameSeason(**data)
    elif split == "Totals":
        s = PlayerTotalSeason(**data)
    elif split == "Advanced":
        s = PlayerAdvancedSeason(**data)
    s.save()

def create_team_season(split, data):
    if split == "PerGame":
        s = TeamPerGameSeason(**data)
    elif split == "Totals":
        s = TeamTotalSeason(**data)
    elif split == "Advanced":
        s = TeamAdvancedSeason(**data)
    print(data)
    s.save()