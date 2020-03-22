from datetime import date

from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.templatetags.static import static


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
  # Duo
  DUO = 'DUO'

AVAILABILITY_PAIRS = (
  (AVAILABILITY.STANDARD, 'Standard Pool',),
  (AVAILABILITY.SPECIAL, 'Special Hero',),
  (AVAILABILITY.GHB, 'Grand Hero Battle',),
  (AVAILABILITY.TT, 'Tempest Trials',),
  (AVAILABILITY.LEGENDARY, 'Legendary Hero',),
  (AVAILABILITY.MYTHIC, 'Mythic Hero',),
  (AVAILABILITY.STORY, 'Story Hero',),
  (AVAILABILITY.DUO, 'Duo Hero',),
)

AVAILABILITY_HUMAN_READABLE = dict(AVAILABILITY_PAIRS)


class MOVEMENT_TYPE(object):
  INFANTRY = 'M_01_INFANTRY'
  FLYING = 'M_02_FLYING'
  CAVALRY = 'M_03_CAVALRY'
  ARMOR = 'M_04_ARMOR'

MOVEMENT_TYPE_PAIRS = (
  (MOVEMENT_TYPE.INFANTRY, 'Infantry',),
  (MOVEMENT_TYPE.ARMOR, 'Armor',),
  (MOVEMENT_TYPE.FLYING, 'Flying',),
  (MOVEMENT_TYPE.CAVALRY, 'Cavalry',),
)

MOVEMENT_TYPE_HUMAN_READABLE = dict(MOVEMENT_TYPE_PAIRS)


class WEAPON_TYPE(object):
  R_SWORD = 'W_01_SWORD'
  B_LANCE = 'W_02_LANCE'
  G_AXE = 'W_03_AXE'

  R_TOME = 'W_11_R_TOME'
  B_TOME = 'W_12_B_TOME'
  G_TOME = 'W_13_G_TOME'
  C_TOME = 'W_14_C_TOME'

  R_BOW = 'W_21_R_BOW'
  B_BOW = 'W_22_B_BOW'
  G_BOW = 'W_23_G_BOW'
  C_BOW = 'W_24_C_BOW'

  R_DAGGER = 'W_31_R_DAGGER'
  B_DAGGER = 'W_32_B_DAGGER'
  G_DAGGER = 'W_33_G_DAGGER'
  C_DAGGER = 'W_34_C_DAGGER'

  R_DRAGON = 'W_41_R_DRAGON'
  B_DRAGON = 'W_42_B_DRAGON'
  G_DRAGON = 'W_43_G_DRAGON'
  C_DRAGON = 'W_44_C_DRAGON'

  R_BEAST = 'W_51_R_BEAST'
  B_BEAST = 'W_52_B_BEAST'
  G_BEAST = 'W_53_G_BEAST'
  C_BEAST = 'W_54_C_BEAST'

  C_STAFF = 'W_64_C_STAFF'


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
  movement_type = models.CharField('move', max_length=15, choices=MOVEMENT_TYPE_PAIRS)

  # WEAPON_TYPE.AXE
  weapon_type = models.CharField('weapon', max_length=15, choices=WEAPON_TYPE_PAIRS)

  # COLOR.GREEN
  color = models.CharField(max_length=15, choices=COLOR_PAIRS)

  hp = models.IntegerField()
  attack = models.IntegerField('atk')
  speed = models.IntegerField('spd')
  defense = models.IntegerField('def')
  resistance = models.IntegerField('res')
  bst = models.IntegerField('BST')

  release_date = models.DateField()

  # All the following are auto generated

  # 2
  book = models.IntegerField()

  # 2
  generation = models.IntegerField('gen')

  categories = ArrayField(models.CharField(max_length=100))
  rarities = ArrayField(models.IntegerField())

  gamepedia_url = models.URLField()

  @property
  def max_stats(self):
    dragonflowers = 1
    if self.movement_type == MOVEMENT_TYPE.INFANTRY and self.release_date <= date(day=7, month=2, year=2019):
      dragonflowers = 2
    add_stats = 4 + dragonflowers
    return [
        self.hp + add_stats,
        self.attack + add_stats,
        self.speed + add_stats,
        self.defense + add_stats,
        self.resistance + add_stats,
    ]

  @property
  def max_bst(self):
    return sum(self.max_stats)

  @property
  def full_name(self):
    return '{0}: {1}'.format(self.name, self.title)

  @property
  def movement_type_icon(self):
    return static('images/icons/ICON_{0}.png'.format(self.movement_type))

  @property
  def book_human(self):
    return 'Book {0}'.format(self.book)

  @property
  def generation_human(self):
    return 'Gen {0}'.format(self.generation)

  @property
  def availability_human(self):
    return AVAILABILITY_HUMAN_READABLE[self.availability]

  @property
  def weapon_type_icon(self):
    return static('images/icons/ICON_{0}.png'.format(self.weapon_type))

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




