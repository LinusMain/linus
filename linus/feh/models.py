from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


# Create your models here.
class AVAILABILITY(object):
  # Standard pool available
  STANDARD = 'STANDARD'
  # Not in standard pool and not any of the other categories
  SPECIAL = 'SPECIAL'
  # GHB hero
  GHB = 'GHB'
  # TT hero
  TT = 'TT'
  # Legendary hero
  LEGENDARY = 'LEGENDARY'
  # Mythic hero
  MYTHIC = 'MYTHIC'
  # Story
  STORY = 'STORY'

AVAILABILITY_PAIRS = (
  (AVAILABILITY.STANDARD, 'Standard Pool',),
  (AVAILABILITY.SPECIAL, 'Limited Hero',),
  (AVAILABILITY.GHB, 'Grand Hero Battle',),
  (AVAILABILITY.TT, 'Tempest Trials',),
  (AVAILABILITY.LEGENDARY, 'Legendary Hero',),
  (AVAILABILITY.MYTHIC, 'Mythic Hero',),
  (AVAILABILITY.STORY, 'Story Hero',),
)

AVAILABILITY_HUMAN_READABLE = dict(AVAILABILITY_PAIRS)


class MOVEMENT_TYPE(object):
  INFANTRY = 'INFANTRY'
  ARMOR = 'ARMOR'
  FLYING = 'FLYING'
  CAVALRY = 'CAVALRY'

MOVEMENT_TYPE_PAIRS = (
  (MOVEMENT_TYPE.INFANTRY, 'Infantry',),
  (MOVEMENT_TYPE.ARMOR, 'Armor',),
  (MOVEMENT_TYPE.FLYING, 'Flying',),
  (MOVEMENT_TYPE.CAVALRY, 'Cavalry',),
)

MOVEMENT_TYPE_HUMAN_READABLE = dict(MOVEMENT_TYPE_PAIRS)


class WEAPON_TYPE(object):
  R_SWORD = 'SWORD'
  B_LANCE = 'LANCE'
  G_AXE = 'AXE'

  R_TOME = 'R_TOME'
  B_TOME = 'B_TOME'
  G_TOME = 'G_TOME'
  C_TOME = 'C_TOME'

  R_BOW = 'R_BOW'
  B_BOW = 'B_BOW'
  G_BOW = 'G_BOW'
  C_BOW = 'C_BOW'

  R_DAGGER = 'R_DAGGER'
  B_DAGGER = 'B_DAGGER'
  G_DAGGER = 'G_DAGGER'
  C_DAGGER = 'C_DAGGER'

  R_DRAGON = 'R_DRAGON'
  B_DRAGON = 'B_DRAGON'
  G_DRAGON = 'G_DRAGON'
  C_DRAGON = 'C_DRAGON'

  R_BEAST = 'R_BEAST'
  B_BEAST = 'B_BEAST'
  G_BEAST = 'G_BEAST'
  C_BEAST = 'C_BEAST'

  C_STAFF = 'C_STAFF'


WEAPON_TYPE_PAIRS = (
  (WEAPON_TYPE.R_SWORD, 'R Sword',),
  (WEAPON_TYPE.B_LANCE, 'B Lance',),
  (WEAPON_TYPE.G_AXE, 'G Axe',),

  (WEAPON_TYPE.R_TOME, 'R Tome',),
  (WEAPON_TYPE.B_TOME, 'B Tome',),
  (WEAPON_TYPE.G_TOME, 'G Tome',),
  (WEAPON_TYPE.C_TOME, 'C Tome',),

  (WEAPON_TYPE.R_BOW, 'R Bow',),
  (WEAPON_TYPE.B_BOW, 'B Bow',),
  (WEAPON_TYPE.G_BOW, 'G Bow',),
  (WEAPON_TYPE.C_BOW, 'C Bow',),

  (WEAPON_TYPE.R_DAGGER, 'R Dagger',),
  (WEAPON_TYPE.B_DAGGER, 'B Dagger',),
  (WEAPON_TYPE.G_DAGGER, 'G Dagger',),
  (WEAPON_TYPE.C_DAGGER, 'C Dagger',),

  (WEAPON_TYPE.R_DRAGON, 'R Dragon',),
  (WEAPON_TYPE.B_DRAGON, 'B Dragon',),
  (WEAPON_TYPE.G_DRAGON, 'G Dragon',),
  (WEAPON_TYPE.C_DRAGON, 'C Dragon',),

  (WEAPON_TYPE.R_BEAST, 'R Beast',),
  (WEAPON_TYPE.B_BEAST, 'B Beast',),
  (WEAPON_TYPE.G_BEAST, 'G Beast',),
  (WEAPON_TYPE.C_BEAST, 'C Beast',),

  (WEAPON_TYPE.C_STAFF, 'C Staff',),
)


WEAPON_TYPE_HUMAN_READABLE = dict(WEAPON_TYPE_PAIRS)


class COLOR(object):
  RED = 'RED'
  BLUE = 'BLUE'
  GREEN = 'GREEN'
  COLORLESS = 'COLORLESS'

COLOR_PAIRS = (
  (COLOR.RED, 'Red',),
  (COLOR.BLUE, 'Blue',),
  (COLOR.GREEN, 'Green',),
  (COLOR.COLORLESS, 'Colorless',),
)

COLOR_HUMAN_READABLE = dict(COLOR_PAIRS)


class Hero(models.Model):

  # Linus
  name = models.CharField(max_length=50)

  # Mad Dog
  title = models.CharField(max_length=50)

  # AVAILABILITY.GHB
  availability = models.CharField(max_length=15, choices=AVAILABILITY_PAIRS)

  # F2Pness: either a 3/4* hero or a grail unit
  is_f2p = models.BooleanField()

  # MOVEMENT_TYPE.INFANTRY
  movement_type = models.CharField(max_length=15, choices=MOVEMENT_TYPE_PAIRS)

  # WEAPON_TYPE.AXE
  weapon_type = models.CharField(max_length=15, choices=WEAPON_TYPE_PAIRS)

  # COLOR.GREEN
  color = models.CharField(max_length=15, choices=COLOR_PAIRS)

  hp = models.IntegerField()
  attack = models.IntegerField()
  speed = models.IntegerField()
  defense = models.IntegerField()
  resistance = models.IntegerField()
  bst = models.IntegerField()

  pullable_3star = models.BooleanField()
  pullable_4star = models.BooleanField()
  pullable_5star = models.BooleanField()

  @property
  def StatArray(self):
    return '{0}/{1}/{2}/{3}/{4}'.format(self.hp, self.attack, self.speed, self.defense, self.resistance)

  # Hidden
  # stat_details = JSONField()

