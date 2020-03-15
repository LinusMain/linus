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


