'''
Created on 21 Dec 2018

@author: irvan
'''

from datetime import datetime, date, time

from django import forms
from django.core import validators
from django.utils import timezone
import pytz


def GetResetDate():
  d = date(2019, 1, 15)
  t = time(15, 0, 0, tzinfo=pytz.timezone('Asia/Singapore'))
  return datetime.combine(d, t)

ARENA_RESET_EPOCH = GetResetDate()


class AetherLiftForm(forms.Form):
  aether = forms.IntegerField(validators=[validators.MinValueValidator(0),
                                          validators.MaxValueValidator(1000)])
  lift = forms.IntegerField(validators=[validators.MinValueValidator(0),
                                        validators.MaxValueValidator(100000)])
  reset_left = forms.IntegerField(validators=[validators.MinValueValidator(0),
                                              validators.MaxValueValidator(15)],
                                  initial=6)

  has_free_run = forms.BooleanField(required=False, initial=True)
  lift_gain = forms.IntegerField(initial=100, validators=[validators.MinValueValidator(0),
                                                          validators.MaxValueValidator(1000)])

  aether_storage_max = forms.IntegerField(initial=200, validators=[validators.MinValueValidator(100),
                                                                   validators.MaxValueValidator(1000)])

  aether_regen = forms.IntegerField(initial=70, validators=[validators.MinValueValidator(0),
                                                          validators.MaxValueValidator(1000)])


  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    current_time = timezone.now()
    epoch_distance = current_time - ARENA_RESET_EPOCH
    so_far = (epoch_distance.days % 7)
    remain = 6 - so_far
    self.fields['reset_left'].initial = remain
    self.fields['aether'].widget.attrs.update({'autofocus': 'autofocus'})

