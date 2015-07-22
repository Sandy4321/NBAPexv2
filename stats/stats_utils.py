#Utility methods primarily used for seed the database

def get_team_info_from_web(team_id):
    url = "http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular+Season&TeamID=1610612"+str(team_id)+"&season=2014-15"
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    #This goofy thing returns a list containing the relevant team information
    return data['resultSets'][0]['rowSet'][0]

def create_team_from_web(t_id):
    info = self.get_team_info_from_web(team_id=t_id)
    team = Team(team_id=info[0], team_city=info[2], team_name=info[3],
    			 team_abbreviation = info[4], team_conference=info[5], 
    			 team_division=info[6], team_code=info[7],wins=info[8],
    			 losses=info[9],w_pct=info[10],conf_rank=info[11],
    			 div_rank=info[12],min_year=int(info[13]),max_year=int(info[14]))
    team.save()

def convert_height_to_int(height_string):
    if len(height_string) > 0:
        vals = height_string.split('-')
        return 12 * int(vals[0]) + int(vals[1])
    return 0

def convert_datetime_string_to_date_instance(date_string):
    #Chomps off the end of the string which is universally 'T00:00:00'
    vals = date_string[:10].split('-')
    return date(int(vals[0]),int(vals[1]),int(vals[2]))

def sanitize_player_data(to_fix):
    to_fix[6] = self.convert_datetime_string_to_date_instance(to_fix[6])
    to_fix[10] = self.convert_height_to_int(to_fix[10])
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
    info = self.sanitize_player_data(self.get_player_info_from_web(player_id=p_id))
    for i in info:
        print("Type: %s Val: %s" %(type(i), i))
    team = Team.objects.get(team_id=info[16])

    player = Player(player_id=info[0],first_name=info[1],last_name=info[2], display_first_last=info[3],display_last_comma_first=info[4],display_fi_last=info[5],birthdate=info[6],
                    school=info[7],country=info[8],last_affiliation=info[9], height=info[10],weight=info[11],season_exp=info[12],jersey=info[13],
                    position=info[14],roster_status=info[15],team_id=team,team_name=info[17],team_abbreviation=info[18],team_code=info[19],team_city=info[20],playercode=info[21],from_year=info[22],
                    to_year=info[23])
    player.save()