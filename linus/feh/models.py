from datetime import date

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


BOOK_BEGIN_DATES = [
    [4, date(day=6, month=12, year=2019)],
    [3, date(day=11, month=12, year=2018)],
    [2, date(day=28, month=11, year=2017)],
    [1, date(day=2, month=2, year=2017)],
]


class Hero(models.Model):

  # Linus
  name = models.CharField(max_length=50)

  # Mad Dog
  title = models.CharField(max_length=50)

  # AVAILABILITY.GHB
  availability = models.CharField(max_length=15, choices=AVAILABILITY_PAIRS)

  # F2Pness: either a 3/4* hero or a grail unit
  is_f2p = models.BooleanField('f2p')

  # MOVEMENT_TYPE.INFANTRY
  movement_type = models.CharField(max_length=15, choices=MOVEMENT_TYPE_PAIRS)

  # WEAPON_TYPE.AXE
  weapon_type = models.CharField(max_length=15, choices=WEAPON_TYPE_PAIRS)

  # COLOR.GREEN
  color = models.CharField(max_length=15, choices=COLOR_PAIRS)

  hp = models.IntegerField()
  attack = models.IntegerField('atk')
  speed = models.IntegerField('spd')
  defense = models.IntegerField('def')
  resistance = models.IntegerField('res')
  bst = models.IntegerField('BST')

  pullable_3star = models.BooleanField()
  pullable_4star = models.BooleanField()
  pullable_5star = models.BooleanField()

  release_date = models.DateField()

  # All the following are auto generated

  # 2
  book = models.IntegerField()

  # 2
  generation = models.IntegerField('gen')

  @property
  def StatArray(self):
    return '{0}/{1}/{2}/{3}/{4}'.format(self.hp, self.attack, self.speed, self.defense, self.resistance)

  def __str__(self):
    return '{0}: {1}'.format(self.name, self.title)

  def ComputeGeneration(self):
    if (self.name, self.title) in [
        ('Bantu', "Tiki's Guardian"),
        ('Chad', 'Lycian Wildcat'),
        ('Tanya', "Dagdar's Kid"),
        ('Ross', "His Father's Son"),
        ('Valbar', 'Open and Honest'),]:
      return 3

    if self.release_date >= date(day=16, month=8, year=2019):
      return 4
    if self.release_date >= date(day=27, month=2, year=2019):
      return 3
    if self.release_date >= date(day=15, month=11, year=2017):
      return 2

    if (self.name, self.title) in [
        ('Ayra', "Astra's Wielder"),
        ('Henry', 'Happy Vampire'),
        ('Jakob', 'Devoted Monster'),
        ('Sigurd', 'Holy Knight'),]:
      return 2

    return 1

  def save(self, *args, **kwargs):
    found = False
    for book, book_begin_date in BOOK_BEGIN_DATES:
      if self.release_date >= book_begin_date:
        self.book = book
        found = True
        break
    assert found, self

    self.generation = self.ComputeGeneration()

    return super().save(*args, **kwargs)

  # Hidden
  # stat_details = JSONField()

