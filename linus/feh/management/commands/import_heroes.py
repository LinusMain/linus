'''
Created on Sep 7, 2017

@author: dolphinigle
'''
from django.core.management.base import BaseCommand

from linus.feh import porocode
from linus.feh.models import AVAILABILITY, MOVEMENT_TYPE, WEAPON_TYPE, COLOR

from ... import models


class Command(BaseCommand):
  help = 'Import Heroes from porocode.'

  def add_arguments(self, parser):
    parser.add_argument('filename', type=str)

  def handle(self, *args, **options):
    filename = options['filename']
    heroes = porocode.readHeroFile(filename)

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

          'Red Breath': WEAPON_TYPE.R_DRAGON,
          'Blue Breath': WEAPON_TYPE.B_DRAGON,
          'Green Breath': WEAPON_TYPE.G_DRAGON,
          'Colorless Breath': WEAPON_TYPE.C_DRAGON,

          'Colorless Staff': WEAPON_TYPE.C_STAFF,
      }

      COLOR_MAP = dict(
          Red=COLOR.RED,
          Blue=COLOR.BLUE,
          Green=COLOR.GREEN,
          Colorless=COLOR.COLORLESS,
      )

      finalstat = hero.statArray

      models.Hero.objects.create(
          name=hero.heroName,
          title=hero.heroMod,
          availability=AV_MAP[hero.heroSrc],
          is_f2p=hero.isF2P(),
          movement_type=MV_MAP[hero.move],
          weapon_type=WP_MAP[hero.getWeaponString()],
          color=COLOR_MAP[hero.getColor()],
          hp = finalstat[-5][1],
          attack = finalstat[-4][1],
          speed = finalstat[-3][1],
          defense = finalstat[-2][1],
          resistance = finalstat[-1][1],
          bst=hero.getBST(),
          pullable_3star=hero.hero3Star,
          pullable_4star=hero.hero4Star,
          pullable_5star=hero.hero5Star,
      )


