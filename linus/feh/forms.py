'''
Created on 21 Dec 2018

@author: irvan
'''

from django import forms
from django.core import validators


class AetherLiftForm(forms.Form):
  aether = forms.IntegerField(validators=[validators.MinValueValidator(0),
                                          validators.MaxValueValidator(200)], initial=200)
  lift = forms.IntegerField(validators=[validators.MinValueValidator(0),
                                        validators.MaxValueValidator(100000)])
  reset_left = forms.IntegerField(validators=[validators.MinValueValidator(0),
                                              validators.MaxValueValidator(7)],
                                  initial=6)

  has_free_run = forms.BooleanField(required=False, initial=True)
  lift_gain = forms.IntegerField(initial=100, validators=[validators.MinValueValidator(0),
                                                          validators.MaxValueValidator(1000)])

  aether_storage_max = forms.IntegerField(initial=200, validators=[validators.MinValueValidator(100),
                                                                   validators.MaxValueValidator(1000)])

  aether_regen = forms.IntegerField(initial=50, validators=[validators.MinValueValidator(0),
                                                          validators.MaxValueValidator(1000)])

