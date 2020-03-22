'''
Created on Sep 7, 2017

@author: dolphinigle
'''
from datetime import date
from time import strptime
import time

from django.core.management.base import BaseCommand

from linus.feh.models import AVAILABILITY, MOVEMENT_TYPE, WEAPON_TYPE, COLOR
from linus.feh.poro.poropicklechecker import LoadPoro

from ... import models


class Command(BaseCommand):
  help = 'Import Heroes from porocode.'

  def handle(self, *args, **options):
    all_data = LoadPoro()

    heroes = all_data['heroes']

    models.Hero.objects.all().delete()
    for hero in heroes:

      AV_MAP = dict(
          Normal=AVAILABILITY.STANDARD,
          Mythic=AVAILABILITY.MYTHIC,
          GHB=AVAILABILITY.GHB,
          Special=AVAILABILITY.SPECIAL,
          Story=AVAILABILITY.STORY,
          TT=AVAILABILITY.TT,
          Legendary=AVAILABILITY.LEGENDARY,
          Duo=AVAILABILITY.DUO,
      )

      MV_MAP = dict(
          Infantry=MOVEMENT_TYPE.INFANTRY,
          Armor=MOVEMENT_TYPE.ARMOR,
          Cavalry=MOVEMENT_TYPE.CAVALRY,
          Flying=MOVEMENT_TYPE.FLYING,
      )

      WP_MAP = {
          'Sword': WEAPON_TYPE.R_SWORD,
          'Lance': WEAPON_TYPE.B_LANCE,
          'Axe': WEAPON_TYPE.G_AXE,

          'Red Tome': WEAPON_TYPE.R_TOME,
          'Blue Tome': WEAPON_TYPE.B_TOME,
          'Green Tome': WEAPON_TYPE.G_TOME,
          'Colorless Tome': WEAPON_TYPE.C_TOME,

          'Red Dagger': WEAPON_TYPE.R_DAGGER,
          'Blue Dagger': WEAPON_TYPE.B_DAGGER,
          'Green Dagger': WEAPON_TYPE.G_DAGGER,
          'Colorless Dagger': WEAPON_TYPE.C_DAGGER,

          'Red Bow': WEAPON_TYPE.R_BOW,
          'Blue Bow': WEAPON_TYPE.B_BOW,
          'Green Bow': WEAPON_TYPE.G_BOW,
          'Colorless Bow': WEAPON_TYPE.C_BOW,

          'Red Beast': WEAPON_TYPE.R_BEAST,
          'Blue Beast': WEAPON_TYPE.B_BEAST,
          'Green Beast': WEAPON_TYPE.G_BEAST,
          'Colorless Beast': WEAPON_TYPE.C_BEAST,

          'Red Dragonstone': WEAPON_TYPE.R_DRAGON,
          'Blue Dragonstone': WEAPON_TYPE.B_DRAGON,
          'Green Dragonstone': WEAPON_TYPE.G_DRAGON,
          'Colorless Dragonstone': WEAPON_TYPE.C_DRAGON,

          'Colorless Stave': WEAPON_TYPE.C_STAFF,
      }

      COLOR_MAP = dict(
          Red=COLOR.RED,
          Blue=COLOR.BLUE,
          Green=COLOR.GREEN,
          Colorless=COLOR.COLORLESS,
      )

      finalstat = hero.statArray
      release_date = strptime(hero.releaseDate, '%Y-%m-%d')

      models.Hero.objects.create(
          name=hero.name,
          title=hero.mod,
          availability=AV_MAP[hero.heroSrc],
          is_f2p=hero.isF2P(),
          movement_type=MV_MAP[hero.move],
          weapon_type=WP_MAP[hero.getWeaponType()],
          color=COLOR_MAP[hero.getColor()],
          hp = finalstat[0],
          attack = finalstat[1],
          speed = finalstat[2],
          defense = finalstat[3],
          resistance = finalstat[4],
          bst=hero.getBST(),
          categories=hero.categories,
          rarities=hero.getPullableRarities(),
          release_date=date.fromtimestamp(time.mktime(release_date)),
          gamepedia_url=hero.url,
      )


