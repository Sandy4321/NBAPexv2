from django.db import models

# Create your models here.
class Team(models.Model):
    team_id = models.IntegerField()
    team_city = models.CharField(max_length=50)
    team_name = models.CharField(max_length=50)
    team_abbreviation = models.CharField(max_length=5)
    team_conference = models.CharField(max_length=4)
    team_division = models.CharField(max_length=25)
    team_code = models.CharField(max_length=25)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    w_pct = models.DecimalField(max_digits=4,decimal_places=3)
    conf_rank = models.IntegerField()
    div_rank = models.IntegerField()
    min_year = models.IntegerField()
    max_year = models.IntegerField()

    def __str__(self):
        return "%s %s" %(self.team_city, self.team_name)

    class Meta:
    	db_table = 'team'


class Player(models.Model):
    player_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_first_last = models.CharField(max_length=201)
    display_last_comma_first = models.CharField(max_length=202)
    display_fi_last = models.CharField(max_length=102)
    birthdate = models.DateField()
    school = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200,null=True)
    last_affiliation = models.CharField(max_length=200,null=True)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    season_exp = models.IntegerField(default=0)
    jersey = models.IntegerField(default=0)
    position = models.CharField(max_length=40,null=True)
    roster_status = models.CharField(max_length=20,null=True)
    team = models.ForeignKey(Team)
    #These fields are include because they can change after a player retires.
    #For instance, if a player retired as a Buffalo Brave, simply referencing the fields in the Teams table would list
    #Him as a Los Angeles Clipper which we don't really want
    team_name = models.CharField(max_length=200,null=True)
    team_abbreviation = models.CharField(max_length=3,null=True)
    team_code = models.CharField(max_length=50,null=True)
    team_city = models.CharField(max_length=100,null=True)
    playercode = models.CharField(max_length=100,null=True)
    from_year = models.IntegerField(default=2015)
    to_year = models.IntegerField(default = 2015)

    def __str__(self):
        return self.display_first_last

    class Meta:
    	db_table = 'player'

class Coach(models.Model):
    coach_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    coach_name = models.CharField(max_length=201)
    from_year = models.IntegerField(default=2015)
    to_year = models.IntegerField(default=2015)
    years = models.IntegerField(default=0)
    reg_season_games = models.IntegerField(default=0)
    reg_season_wins = models.IntegerField(default=0)
    reg_season_losses = models.IntegerField(default=0)
    reg_season_w_pct = models.DecimalField(max_digits=4,decimal_places=3)
    above_500 = models.DecimalField(max_digits=5,decimal_places=1,null=True)
    post_season_games = models.IntegerField(default=0,null=True)
    post_season_wins = models.IntegerField(default=0,null=True)
    post_season_losses = models.IntegerField(default=0,null=True)
    post_season_w_pct = models.DecimalField(max_digits=4,decimal_places=3,null=True)
    conference_champs = models.IntegerField(default=0,null=True)
    league_champs = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.coach_name

    class Meta:
    	db_table = 'coach'

class Referee(models.Model):
    ref_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ref_name = models.CharField(max_length=201)
    birthdate = models.DateField()
    school = models.CharField(max_length=100)
    jersey = models.IntegerField()

    def __str__(self):
        return self.ref_name

    class Meta:
    	db_table = 'referees'

class PlayerSeason(models.Model):
    player = models.ForeignKey(Player)
    #Value of 0 indicates Career Totals
    season_id = models.IntegerField()
    #regular, post, all star
    season_type = models.CharField(max_length=100)
    career_flag = models.BooleanField()
    player_name = models.CharField(max_length=200)
    team = models.ForeignKey(Team)
    team_abbreviation = models.CharField(max_length=5)
    player_age = models.IntegerField()
    gp = models.IntegerField(default=0)
    gs = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    l = models.IntegerField(default=0)
    w_pct = models.DecimalField(max_digits=4,decimal_places=3)

    class Meta:
        abstract = True

class PlayerPerGameSeason(PlayerSeason):
    min = models.DecimalField(max_digits=3,decimal_places=1)
    fgm = models.DecimalField(max_digits=3,decimal_places=1)
    fga = models.DecimalField(max_digits=3,decimal_places=1)
    fg_pct = models.DecimalField(max_digits=4,decimal_places=3)
    fg3m = models.DecimalField(max_digits=3,decimal_places=1)
    fg3a = models.DecimalField(max_digits=3,decimal_places=1)
    fg3_pct = models.DecimalField(max_digits=4,decimal_places=3)
    ftm = models.DecimalField(max_digits=3,decimal_places=1)
    fta = models.DecimalField(max_digits=3,decimal_places=1)
    ft_pct = models.DecimalField(max_digits=4,decimal_places=3)
    oreb = models.DecimalField(max_digits=3,decimal_places=1)
    dreb = models.DecimalField(max_digits=3,decimal_places=1)
    reb = models.DecimalField(max_digits=3,decimal_places=1)
    ast = models.DecimalField(max_digits=3,decimal_places=1)
    stl = models.DecimalField(max_digits=3,decimal_places=1)
    blk = models.DecimalField(max_digits=3,decimal_places=1)
    blka = models.DecimalField(max_digits=3,decimal_places=1)
    tov = models.DecimalField(max_digits=3,decimal_places=1)
    pf = models.DecimalField(max_digits=3,decimal_places=1)
    pfd = models.DecimalField(max_digits=3,decimal_places=1)
    pts = models.DecimalField(max_digits=3,decimal_places=1)
    plus_minus = models.DecimalField(max_digits=3,decimal_places=1)
    dd2 = models.IntegerField(default=0)
    td3 = models.IntegerField(default=0)

    class Meta:
    	db_table = 'player_per_game_season'

class PlayerTotalSeason(PlayerSeason):
    min = models.IntegerField()
    fgm = models.IntegerField()
    fga = models.IntegerField()
    fg_pct = models.DecimalField(max_digits=4,decimal_places=3)
    fg3m = models.IntegerField()
    fg3a = models.IntegerField()
    fg3_pct = models.DecimalField(max_digits=4,decimal_places=3)
    ftm = models.IntegerField()
    fta = models.IntegerField()
    ft_pct = models.DecimalField(max_digits=4,decimal_places=3)
    oreb = models.IntegerField()
    dreb = models.IntegerField()
    reb = models.IntegerField()
    ast = models.IntegerField()
    stl = models.IntegerField()
    blk = models.IntegerField()
    blka = models.IntegerField()
    tov = models.IntegerField()
    pf = models.IntegerField()
    pfd = models.IntegerField()
    pts = models.IntegerField()
    plus_minus = models.IntegerField()
    dd2 = models.IntegerField(default=0)
    td3 = models.IntegerField(default=0)

    class Meta:
    	db_table = 'player_total_season'

class PlayerAdvancedSeason(PlayerSeason):
    min = models.IntegerField()
    u_per = models.DecimalField(max_digits=3,decimal_places=1)
    per = models.DecimalField(max_digits=3,decimal_places=1)
    ts_pct = models.DecimalField(max_digits=4,decimal_places=3)
    fg3_ar = models.DecimalField(max_digits=3,decimal_places=3)
    ft_ar = models.DecimalField(max_digits=3,decimal_places=3)
    oreb_pct = models.DecimalField(max_digits=3,decimal_places=1)
    dreb_pct = models.DecimalField(max_digits=3,decimal_places=1)
    reb_pct = models.DecimalField(max_digits=3,decimal_places=1)
    ast_pct = models.DecimalField(max_digits=3,decimal_places=1)
    stl_pct = models.DecimalField(max_digits=3,decimal_places=1)
    blk_pct = models.DecimalField(max_digits=3,decimal_places=1)
    tov_pct = models.DecimalField(max_digits=3,decimal_places=1)
    usg_pct = models.DecimalField(max_digits=3,decimal_places=1)
    ows = models.DecimalField(max_digits=3,decimal_places=1)
    dws = models.DecimalField(max_digits=3,decimal_places=1)
    ws = models.DecimalField(max_digits=3,decimal_places=1)
    ws_48 = models.DecimalField(max_digits=3,decimal_places=3)
    obpm = models.DecimalField(max_digits=3,decimal_places=1)
    dbpm = models.DecimalField(max_digits=3,decimal_places=1)
    bpm = models.DecimalField(max_digits=3,decimal_places=1)
    vorp = models.DecimalField(max_digits=3,decimal_places=1)

    class Meta:
    	db_table = 'player_advanced_season'

class TeamSeason(models.Model):
    team = models.ForeignKey(Team)
    season_type = models.CharField(max_length=100)
    season_id = models.IntegerField()
    team_name = models.CharField(max_length=100)
    gp = models.IntegerField()
    w = models.IntegerField()
    l = models.IntegerField()
    w_pct = models.DecimalField(max_digits = 4, decimal_places=3)

    class Meta:
        abstract = True

class TeamPerGameSeason(TeamSeason):
    min = models.DecimalField(max_digits=3,decimal_places=1)
    fgm = models.DecimalField(max_digits=3,decimal_places=1)
    fga = models.DecimalField(max_digits=3,decimal_places=1)
    fg_pct = models.DecimalField(max_digits=4,decimal_places=3)
    fg3m = models.DecimalField(max_digits=3,decimal_places=1)
    fg3a = models.DecimalField(max_digits=3,decimal_places=1)
    fg3_pct = models.DecimalField(max_digits=4,decimal_places=3)
    ftm = models.DecimalField(max_digits=3,decimal_places=1)
    fta = models.DecimalField(max_digits=3,decimal_places=1)
    ft_pct = models.DecimalField(max_digits=4,decimal_places=3)
    oreb = models.DecimalField(max_digits=3,decimal_places=1)
    dreb = models.DecimalField(max_digits=3,decimal_places=1)
    reb = models.DecimalField(max_digits=3,decimal_places=1)
    ast = models.DecimalField(max_digits=3,decimal_places=1)
    stl = models.DecimalField(max_digits=3,decimal_places=1)
    blk = models.DecimalField(max_digits=3,decimal_places=1)
    blka = models.DecimalField(max_digits=3,decimal_places=1)
    tov = models.DecimalField(max_digits=3,decimal_places=1)
    pf = models.DecimalField(max_digits=3,decimal_places=1)
    pfd = models.DecimalField(max_digits=3,decimal_places=1)
    pts = models.DecimalField(max_digits=3,decimal_places=1)
    plus_minus = models.DecimalField(max_digits=3,decimal_places=1)

    class Meta:
    	db_table = 'team_per_game_season'

class TeamTotalSeason(TeamSeason):
    min = models.IntegerField()
    fgm = models.IntegerField()
    fga = models.IntegerField()
    fg_pct = models.DecimalField(max_digits=4,decimal_places=3)
    fg3m = models.IntegerField()
    fg3a = models.IntegerField()
    fg3_pct = models.DecimalField(max_digits=4,decimal_places=3)
    ftm = models.IntegerField()
    fta = models.IntegerField()
    ft_pct = models.IntegerField()
    oreb = models.IntegerField()
    dreb = models.IntegerField()
    reb = models.IntegerField()
    ast = models.IntegerField()
    stl = models.IntegerField()
    blk = models.IntegerField()
    blka = models.IntegerField()
    tov = models.IntegerField()
    pf = models.IntegerField()
    pfd = models.IntegerField()
    pts = models.IntegerField()
    plus_minus = models.IntegerField()

    class Meta:
    	db_table = 'team_total_season'

class TeamAdvancedSeason(TeamSeason):
    min = models.IntegerField()
    off_rating = models.DecimalField(max_digits=4,decimal_places=1)
    def_rating = models.DecimalField(max_digits=4,decimal_places=1)
    net_rating = models.DecimalField(max_digits=3,decimal_places=1)
    ast_pct = models.DecimalField(max_digits=3,decimal_places=1)
    ast_to = models.DecimalField(max_digits=3,decimal_places=2)
    ast_ratio = models.DecimalField(max_digits=3,decimal_places=1)
    oreb_pct = models.DecimalField(max_digits=3,decimal_places=1)
    dreb_pct = models.DecimalField(max_digits=3,decimal_places=1)
    reb_pct = models.DecimalField(max_digits=3,decimal_places=1)
    tm_tov_pct = models.DecimalField(max_digits=3,decimal_places=1)
    efg_pct = models.DecimalField(max_digits=3,decimal_places=1)
    ts_pct = models.DecimalField(max_digits=3,decimal_places=1)
    pace = models.DecimalField(max_digits=5,decimal_places=2)
    pie = models.DecimalField(max_digits=3,decimal_places=1)

    class Meta:
    	db_table = 'team_advanced_season'