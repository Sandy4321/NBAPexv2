from django.test import TestCase

from .models import *
from stats.stats_utils import *
# Create your tests here.

class PlayerSeasonMethodTests(TestCase):
	def setup(self)
	
	def test_make_season_int(self):
		self.assertEqual(make_season_int("1999-00"),1999)

	def test_make_season_str(self):
		self.assertEqual(make_season_str(1978),"1978-79")
		self.assertEqual(make_season_str(1999),"1999-00")
		self.assertEqual(make_season_str(2001),"2001-02")
		self.assertEqual(make_season_str(2012),"2012-13")

	def test_get_player_age(self):

