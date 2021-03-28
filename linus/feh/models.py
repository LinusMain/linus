from datetime import date

from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.templatetags.static import static
from pygments.lexers.parsers import AntlrJavaLexer


# Create your models here.
class AVAILABILITY(object):
  # Standard pool available
  STANDARD = 'A_STANDARD'
  # Not in standard pool and not any of the other categories
  SPECIAL = 'A_SPECIAL'
  # GHB hero
  GHB = 'A_GHB'
  # TT hero
  TT = 'A_TT'
  # Legendary hero
  LEGENDARY = 'A_LEGENDARY'
  # Mythic hero
  MYTHIC = 'A_MYTHIC'
  # Story
  STORY = 'A_STORY'
  # Duo
  DUO = 'A_DUO'
  # Harmonized
  HARMONIZED = 'A_HARMONIZED'

AVAILABILITY_PAIRS = (
  (AVAILABILITY.STANDARD, 'Standard Pool',),
  (AVAILABILITY.SPECIAL, 'Special',),
  (AVAILABILITY.GHB, 'Grand Hero Battle',),
  (AVAILABILITY.TT, 'Tempest Trials',),
  (AVAILABILITY.LEGENDARY, 'Legendary',),
  (AVAILABILITY.MYTHIC, 'Mythic',),
  (AVAILABILITY.STORY, 'Story',),
  (AVAILABILITY.DUO, 'Duo',),
  (AVAILABILITY.HARMONIZED, 'Harmonized',),
)

AVAILABILITY_HUMAN_READABLE = dict(AVAILABILITY_PAIRS)


class GAME(object):
  ALFONSE = 'G_01_ALFONSE'
  MARTH = 'G_02_MARTH'
  ALM = 'G_03_ALM'
  SELIPH = 'G_04_SELIPH'
  LEIF = 'G_05_LEIF'
  ROY = 'G_06_ROY'
  LYN = 'G_07_LYN'
  EPHRAIM = 'G_08_EPHRAIM'
  IKE = 'G_09_IKE'
  MICAIAH = 'G_10_MICAIAH'
  CHROM = 'G_11_CHROM'
  CORRIN = 'G_12_CORRIN'
  SOTHIS = 'G_13_SOTHIS'
  ITSUKI = 'G_14_ITSUKI'

GAME_PAIRS = (
  (GAME.ALFONSE, 'Fire Emblem Heroes',),
  (GAME.MARTH, 'Mystery of the Emblem / Shadow Dragon',),
  (GAME.ALM, 'Echoes: Shadows of Valentia',),
  (GAME.SELIPH, 'Genealogy of the Holy War',),
  (GAME.LEIF, 'Thracia 776',),
  (GAME.ROY, 'The Binding Blade',),
  (GAME.LYN, 'The Blazing Blade',),
  (GAME.EPHRAIM, 'The Sacred Stones',),
  (GAME.IKE, 'Path of Radiance',),
  (GAME.MICAIAH, 'Radiant Dawn',),
  (GAME.CHROM, 'Awakening',),
  (GAME.CORRIN, 'Fates',),
  (GAME.SOTHIS, 'Three Houses',),
  (GAME.ITSUKI, 'Tokyo Mirage Sessions',),
)

GAME_READABLE = dict(GAME_PAIRS)

TEXT_TO_GAME_MAP = {
    "Awakening": GAME.CHROM,
    "Echoes: Shadows of Valentia": GAME.ALM,
    "Fates": GAME.CORRIN,
    "Genealogy of the Holy War": GAME.SELIPH,
    "Heroes": GAME.ALFONSE,
    "Mystery of the Emblem": GAME.MARTH,
    "New Mystery of the Emblem": GAME.MARTH,
    "Path of Radiance": GAME.IKE,
    "Radiant Dawn": GAME.MICAIAH,
    "Shadow Dragon and the Blade of Light": GAME.MARTH,
    "The Binding Blade": GAME.ROY,
    "The Blazing Blade": GAME.LYN,
    "The Sacred Stones": GAME.EPHRAIM,
    "Thracia 776": GAME.LEIF,
    "Three Houses": GAME.SOTHIS,
    "Tokyo Mirage Sessions ♯FE Encore": GAME.ITSUKI,
}

class MOVEMENT_TYPE(object):
  INFANTRY = 'M_01'
  FLYING = 'M_02'
  CAVALRY = 'M_03'
  ARMOR = 'M_04'

MOVEMENT_TYPE_PAIRS = (
  (MOVEMENT_TYPE.INFANTRY, 'Infantry',),
  (MOVEMENT_TYPE.ARMOR, 'Armor',),
  (MOVEMENT_TYPE.FLYING, 'Flying',),
  (MOVEMENT_TYPE.CAVALRY, 'Cavalry',),
)

MOVEMENT_TYPE_HUMAN_READABLE = dict(MOVEMENT_TYPE_PAIRS)


class F2P_LEVEL(object):
  STORY = 'F_00'
  GRAIL = 'F_01'
  THREE_STAR_STANDARD = 'F_02'
  THREE_STAR_LIMITED = 'F_03'
  FOUR_STAR_STANDARD = 'F_04'
  FOUR_STAR_LIMITED = 'F_05'
  FIVE_STAR_STANDARD = 'F_08'
  FIVE_STAR_LIMITED = 'F_09'


F2P_LEVEL_PAIRS = (
  (F2P_LEVEL.STORY, 'Story',),
  (F2P_LEVEL.THREE_STAR_STANDARD, '3* Standard Pool',),
  (F2P_LEVEL.THREE_STAR_LIMITED, '3* Limited Pool',),
  (F2P_LEVEL.FOUR_STAR_STANDARD, '4* Standard Pool',),
  (F2P_LEVEL.GRAIL, 'Grail',),
  (F2P_LEVEL.FOUR_STAR_LIMITED, '4* Limited Pool',),
  (F2P_LEVEL.FIVE_STAR_STANDARD, '3* Standard Pool',),
  (F2P_LEVEL.FIVE_STAR_LIMITED, '3* Standard Pool',),
)

F2P_LEVEL_HUMAN_READABLE = dict(F2P_LEVEL_PAIRS)

F2P_LEVEL_OVERRIDE = {
    F2P_LEVEL.THREE_STAR_STANDARD: [
        F2P_LEVEL.THREE_STAR_LIMITED,
        F2P_LEVEL.FOUR_STAR_STANDARD,
        F2P_LEVEL.FOUR_STAR_LIMITED,
        F2P_LEVEL.FIVE_STAR_STANDARD,
        F2P_LEVEL.FIVE_STAR_LIMITED,
    ],
    F2P_LEVEL.FOUR_STAR_STANDARD: [
        F2P_LEVEL.FOUR_STAR_LIMITED,
        F2P_LEVEL.FIVE_STAR_STANDARD,
        F2P_LEVEL.FIVE_STAR_LIMITED,
    ],
    F2P_LEVEL.FOUR_STAR_LIMITED: [
        F2P_LEVEL.FIVE_STAR_LIMITED,
    ],
    F2P_LEVEL.FIVE_STAR_STANDARD: [
        F2P_LEVEL.FIVE_STAR_LIMITED,
    ],
}


class WEAPON_TYPE(object):
  R_SWORD = 'W_01'
  B_LANCE = 'W_02'
  G_AXE = 'W_03'
  C_STAFF = 'W_04'
  X_STAFF = 'W_05'

  R_TOME = 'W_11'
  B_TOME = 'W_12'
  G_TOME = 'W_13'
  C_TOME = 'W_14'
  X_TOME = 'W_15'

  R_BOW = 'W_21'
  B_BOW = 'W_22'
  G_BOW = 'W_23'
  C_BOW = 'W_24'
  X_BOW = 'W_25'

  R_DAGGER = 'W_31'
  B_DAGGER = 'W_32'
  G_DAGGER = 'W_33'
  C_DAGGER = 'W_34'
  X_DAGGER = 'W_35'

  R_DRAGON = 'W_41'
  B_DRAGON = 'W_42'
  G_DRAGON = 'W_43'
  C_DRAGON = 'W_44'
  X_DRAGON = 'W_45'

  R_BEAST = 'W_51'
  B_BEAST = 'W_52'
  G_BEAST = 'W_53'
  C_BEAST = 'W_54'
  X_BEAST = 'W_55'


  ASSIST = 'W_71'
  SPECIAL = 'W_81'
  A_SLOT = 'W_91'
  B_SLOT= 'W_92'
  C_SLOT = 'W_93'
  SACRED_SEAL = 'W_94'


WEAPON_TYPE_PAIRS = (
  (WEAPON_TYPE.R_SWORD, 'R Sword',),
  (WEAPON_TYPE.B_LANCE, 'B Lance',),
  (WEAPON_TYPE.G_AXE, 'G Axe',),

  (WEAPON_TYPE.R_TOME, 'R Tome',),
  (WEAPON_TYPE.B_TOME, 'B Tome',),
  (WEAPON_TYPE.G_TOME, 'G Tome',),
  (WEAPON_TYPE.C_TOME, 'C Tome',),
  (WEAPON_TYPE.X_TOME, 'X Tome',),

  (WEAPON_TYPE.R_BOW, 'R Bow',),
  (WEAPON_TYPE.B_BOW, 'B Bow',),
  (WEAPON_TYPE.G_BOW, 'G Bow',),
  (WEAPON_TYPE.C_BOW, 'C Bow',),
  (WEAPON_TYPE.X_BOW, 'X Bow',),

  (WEAPON_TYPE.R_DAGGER, 'R Dagger',),
  (WEAPON_TYPE.B_DAGGER, 'B Dagger',),
  (WEAPON_TYPE.G_DAGGER, 'G Dagger',),
  (WEAPON_TYPE.C_DAGGER, 'C Dagger',),
  (WEAPON_TYPE.X_DAGGER, 'X Dagger',),

  (WEAPON_TYPE.R_DRAGON, 'R Dragon',),
  (WEAPON_TYPE.B_DRAGON, 'B Dragon',),
  (WEAPON_TYPE.G_DRAGON, 'G Dragon',),
  (WEAPON_TYPE.C_DRAGON, 'C Dragon',),
  (WEAPON_TYPE.X_DRAGON, 'X Dragon',),

  (WEAPON_TYPE.R_BEAST, 'R Beast',),
  (WEAPON_TYPE.B_BEAST, 'B Beast',),
  (WEAPON_TYPE.G_BEAST, 'G Beast',),
  (WEAPON_TYPE.C_BEAST, 'C Beast',),
  (WEAPON_TYPE.X_BEAST, 'X Beast',),

  (WEAPON_TYPE.C_STAFF, 'C Staff',),
  (WEAPON_TYPE.X_STAFF, 'X Staff',),

  (WEAPON_TYPE.ASSIST, 'Assist',),
  (WEAPON_TYPE.SPECIAL, 'Special',),
  (WEAPON_TYPE.A_SLOT, 'A',),
  (WEAPON_TYPE.A_SLOT, 'B',),
  (WEAPON_TYPE.A_SLOT, 'C',),
  (WEAPON_TYPE.SACRED_SEAL, 'Sacred Seal'),
)

WEAPON_TYPE_HUMAN_READABLE = dict(WEAPON_TYPE_PAIRS)


class COLOR(object):
  RED = 'C_01'
  BLUE = 'C_02'
  GREEN = 'C_03'
  COLORLESS = 'C_04'

COLOR_PAIRS = (
  (COLOR.RED, 'Red',),
  (COLOR.BLUE, 'Blue',),
  (COLOR.GREEN, 'Green',),
  (COLOR.COLORLESS, 'Colorless',),
)

COLOR_HUMAN_READABLE = dict(COLOR_PAIRS)


BOOK_BEGIN_DATES = [
    [5, date(day=7, month=12, year=2020)],
    [4, date(day=6, month=12, year=2019)],
    [3, date(day=11, month=12, year=2018)],
    [2, date(day=28, month=11, year=2017)],
    [1, date(day=2, month=2, year=2017)],
]


def upload_to_dir(instance, filename):
  return 'heroes_icons/{0}.webp'.format(instance.stripped_name.replace(' ', '-'))


class Hero(models.Model):

  # Linus
  name = models.CharField(max_length=50)

  # Mad Dog
  title = models.CharField(max_length=50)

  # name and title stripped off special characters, for search.
  stripped_name = models.CharField(max_length=100)

  # AVAILABILITY.GHB
  availability = models.CharField(max_length=15, choices=AVAILABILITY_PAIRS)

  # F2Pness: either a 3/4* hero or a grail unit
  f2p_level = models.CharField(max_length=25, choices=F2P_LEVEL_PAIRS)

  # MOVEMENT_TYPE.INFANTRY
  movement_type = models.CharField('move', max_length=15, choices=MOVEMENT_TYPE_PAIRS)

  # WEAPON_TYPE.AXE
  weapon_type = models.CharField('weapon', max_length=15, choices=WEAPON_TYPE_PAIRS)

  # COLOR.GREEN
  color = models.CharField(max_length=15, choices=COLOR_PAIRS)

  origin_game = models.CharField(max_length=50)

  # for leg, mythics
  season = models.CharField(max_length=15, blank=True)

  hp = models.IntegerField()
  attack = models.IntegerField('atk')
  speed = models.IntegerField('spd')
  defense = models.IntegerField('def')
  resistance = models.IntegerField('res')
  bst = models.IntegerField('BST')

  release_date = models.DateField()

  skills = ArrayField(models.CharField(max_length=100))

  gender = models.CharField(max_length=10)

  is_dancer = models.BooleanField()

  has_resplendent = models.BooleanField()

  # All the following are auto generated

  # 2
  book = models.IntegerField()

  # 2
  generation = models.IntegerField('gen')

  harmonized_skill = models.CharField(max_length=2000, blank=True, null=True, default=None)

  rarities = ArrayField(models.IntegerField())

  gamepedia_url = models.URLField()

  # ['+', '', '-', '-', '+']
  boonbanes = ArrayField(models.CharField(max_length=3, blank=True))

  #icon_image = models.ImageField(upload_to=upload_to_dir,
  #                               blank=True,
  #                               null=True,)

  def get_neutral_max_stats(self):
    dragonflowers = 1
    if self.movement_type == MOVEMENT_TYPE.INFANTRY and self.release_date <= date(day=7, month=2, year=2019):
      dragonflowers = 2
    if self.generation < 5:
      dragonflowers += 1
    add_stats = 4 + dragonflowers
    if self.has_resplendent:
      add_stats += 2
    return [
        self.hp + add_stats,
        self.attack + add_stats,
        self.speed + add_stats,
        self.defense + add_stats,
        self.resistance + add_stats,
    ]

  def stats(self):
    return [self.hp, self.attack, self.speed, self.defense, self.resistance]

  @property
  def max_stats(self):
    neutral = self.get_neutral_max_stats()
    res = []
    for (stat, boonbane) in zip(neutral, self.boonbanes):
      addon = 0
      if boonbane == '+':
        addon += 1
      res.append(stat+3+addon)
    return res

  @property
  def max_bst(self):
    base = sum(self.get_neutral_max_stats())
    if '+' in self.boonbanes:
      base += 1
    return base+3

  def get_neutral_adjusted_stats(self):
    dragonflowers = 0
    if self.movement_type == MOVEMENT_TYPE.INFANTRY and self.release_date <= date(day=7, month=2, year=2019):
      dragonflowers = 1
    if self.generation < 5:
      dragonflowers += 1
    add_stats = dragonflowers
    if self.has_resplendent:
      add_stats += 2
    return [
        self.hp + add_stats,
        self.attack + add_stats,
        self.speed + add_stats,
        self.defense + add_stats,
        self.resistance + add_stats,
    ]

  @property
  def adjusted_stats(self):
    return self.get_neutral_adjusted_stats()

  @property
  def adjusted_bst(self):
    base = sum(self.get_neutral_adjusted_stats())
    return base

  @property
  def full_name(self):
    return '{0}: {1}'.format(self.name, self.title)

  @property
  def movement_type_icon(self):
    return static('images/icons/ICON_{0}.png'.format(self.movement_type))

  @property
  def movement_type_human(self):
    return MOVEMENT_TYPE_HUMAN_READABLE.get(self.movement_type)

  @property
  def game_icon(self):
    code = self.game_code
    if code:
      return static('images/icons/ICON_{0}.png'.format(code))
    else:
      return None

  @property
  def game_human(self):
    return GAME_READABLE.get(self.game_code)

  @property
  def f2p_level_icon(self):
    return static('images/icons/ICON_{0}.png'.format(self.f2p_level))

  @property
  def f2p_level_human(self):
    return F2P_LEVEL_HUMAN_READABLE.get(self.f2p_level)

  @property
  def availability_icon(self):
    return static('images/icons/ICON_{0}.png'.format(self.availability))

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
  def game_code(self):
    return TEXT_TO_GAME_MAP.get(self.origin_game)


  @property
  def weapon_type_icon(self):
    return static('images/icons/ICON_{0}.png'.format(self.weapon_type))

  @property
  def weapon_type_human(self):
    return WEAPON_TYPE_HUMAN_READABLE.get(self.weapon_type)

  @property
  def StatArray(self):
    return '{0}/{1}/{2}/{3}/{4}'.format(self.hp, self.attack, self.speed, self.defense, self.resistance)

  @property
  def StandardDeviation(self):
    DEFAULT_HP = 10
    effective_bst = self.bst - DEFAULT_HP
    average = effective_bst * 1.0 / 5
    sumsquare = 0.0
    stats = [self.hp, self.attack, self.speed, self.defense, self.resistance]
    for i in range(5):
      stat = stats[i]
      if i == 0:
        stat -= DEFAULT_HP
      sumsquare += (stat - average)**2.0
    return (sumsquare / 5)**0.5

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

    if self.release_date >= date(day=15, month=8, year=2020):
      return 5
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

    if self.availability == AVAILABILITY.STORY:
      self.f2p_level = F2P_LEVEL.STORY
    elif self.availability in [AVAILABILITY.TT, AVAILABILITY.GHB]:
      self.f2p_level = F2P_LEVEL.GRAIL
    elif 1 in self.rarities or 2 in self.rarities or 3 in self.rarities:
      if self.availability == AVAILABILITY.STANDARD:
        self.f2p_level = F2P_LEVEL.THREE_STAR_STANDARD
      else:
        self.f2p_level = F2P_LEVEL.THREE_STAR_LIMITED
    elif 4 in self.rarities:
      if self.availability == AVAILABILITY.STANDARD:
        self.f2p_level = F2P_LEVEL.FOUR_STAR_STANDARD
      else:
        self.f2p_level = F2P_LEVEL.FOUR_STAR_LIMITED
    else:
      # assert self.rarities == [5] because gamepedia is ebil and sometimes this
      # is left empty at the beginning
      if self.availability == AVAILABILITY.STANDARD:
        self.f2p_level = F2P_LEVEL.FIVE_STAR_STANDARD
      else:
        self.f2p_level = F2P_LEVEL.FIVE_STAR_LIMITED

    return super().save(*args, **kwargs)

  # Hidden
  # stat_details = JSONField()



class Skill(models.Model):

  # Basilikos
  name = models.CharField(max_length=50)

  # name stripped off special characters, for search.
  stripped_name = models.CharField(max_length=100)

  # Accelerate special cooldown
  description = models.CharField(max_length=2000)

  slot = models.CharField(max_length=15, choices=WEAPON_TYPE_PAIRS)

  # Sp cost
  cost = models.IntegerField()

  # is_prf?
  is_prf = models.BooleanField()

  # is_max: is this the final skill on SOME unit. Fury 3 is, even though fury 4 exist.
  is_max = models.BooleanField()

  # GHB, TT, etc
  availabilities = ArrayField(models.CharField(max_length=15, choices=AVAILABILITY_PAIRS))

  # 4: Linus, 5: Leif, etc
  heroes = ArrayField(models.CharField(max_length=200))

  hero_stripped_names = ArrayField(models.CharField(max_length=200))

  f2p_levels = ArrayField(models.CharField(max_length=25, choices=F2P_LEVEL_PAIRS))

  # Smallest rarity where this can be learned
  rarity = models.IntegerField(blank=True, null=True,)

  release_date = models.DateField(blank=True, null=True)

  book = models.IntegerField(blank=True, null=True)

  gamepedia_url = models.URLField()

  f2p_levels = ArrayField(models.CharField(max_length=25, choices=F2P_LEVEL_PAIRS))

  weapon_permissions = ArrayField(models.CharField(max_length=15, choices=WEAPON_TYPE_PAIRS))

  movement_permissions = ArrayField(models.CharField(max_length=15, choices=MOVEMENT_TYPE_PAIRS))

  # Weapon only
  # mt = models.IntegerField(blank=True, null=True)
  # range = models.IntegerField(blank=True, null=True)

  @property
  def display_heroes(self):
    res = []
    for hero in self.heroes:
      f2p_level, availability, icon_url, heroname = hero.split('@', 3)
      res.append([
          static('images/icons/ICON_{0}.png'.format(f2p_level)),
          static('images/icons/ICON_{0}.png'.format(availability)),
          icon_url,
          heroname])
    return res

  @property
  def slot_icon(self):
    return static('images/icons/ICON_{0}.png'.format(self.slot))

  @property
  def f2p_levels_icons(self):
    return [static('images/icons/ICON_{0}.png'.format(f2p_level)) for f2p_level in self.f2p_levels]

  @property
  def weapon_permissions_icons(self):
    return [static('images/icons/ICON_{0}.png'.format(weapon_permission)) for weapon_permission in self.weapon_permissions]

  def movement_permissions_icons(self):
    return [static('images/icons/ICON_{0}.png'.format(movement_permission)) for movement_permission in self.movement_permissions]

  @property
  def book_human(self):
    return 'Book {0}'.format(self.book)

  def __str__(self):
    return '{0}'.format(self.name)



