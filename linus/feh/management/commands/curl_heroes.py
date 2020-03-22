'''
Created on Sep 7, 2017

@author: dolphinigle
'''

from django.core.management.base import BaseCommand

from linus.feh.poro.porocurler import CurlAll


class Command(BaseCommand):
  help = 'Curl heroes from gamepedia.'

  def handle(self, *args, **options):
    CurlAll()


