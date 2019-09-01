import sys

from django.shortcuts import render
from django.views.generic.edit import FormView

from linus.feh.lucksack_calc import FehSnipeProbability

from . import forms


def AetherCost(lift):
  return min(50, (lift + 99) // 100 + 9)

def Pot(lift):
  return min(10, ((lift // 100) + 10) // 5)

def Calc(aether, lift, resets, lift_gain=100, aether_max=200, aether_regen=50):
  res = []
  current_aether = aether
  current_lift = lift
  res.append('Aether: {0}, Lift: {1}'.format(current_aether, current_lift))

  pot_gains = []
  for x in range(resets+1):
    res.append('')
    res.append('Start of day {0}/{1}'.format(x, resets))
    if x:
      res.append('Aether regen daily.')
      current_aether += aether_regen
      res.append('Aether: {0}, Lift: {1}'.format(current_aether, current_lift))
      current_aether = min(current_aether, aether_max)

    # Do Free Run
    #if has_free_run or x:
    #  pot_q = Pot(current_lift)
    #  res.append('>>>Free run. Pay 0. Get {0} from pots'.format(pot_q))
    #  current_aether += pot_q
    #  current_aether = min(current_aether, aether_max)
    #  current_lift += lift_gain
    #  pot_gains.append(pot_q)
    #  res.append('Aether: {0}, Lift: {1}'.format(current_aether, current_lift))

    # Do as many runs as you can
    while current_aether >= AetherCost(current_lift):
      cost = AetherCost(current_lift)
      pot = Pot(current_lift)
      res.append('>>>Normal run. Pay {0}. Get {1} from pots'.format(cost, pot))
      current_aether -= cost
      current_aether += pot
      pot_gains.append(pot)
      current_aether = min(current_aether, aether_max)
      current_lift += lift_gain
      res.append('Aether: {0}, Lift: {1}'.format(current_aether, current_lift))

  # How many pots can I miss?
  can_miss = 0
  if len(pot_gains) >= 2:
    spare = current_aether - pot_gains[-1]
    i = len(pot_gains)-2
    while i >= 0:
      if spare - pot_gains[i] >= 0:
        spare -= pot_gains[i]
        can_miss += 2
        i -= 1
      elif spare - (pot_gains[i] - pot_gains[i] / 2) >= 0:
        spare -= (pot_gains[i] - pot_gains[i] / 2)
        can_miss += 1
        break
      else:
        break

  return res, current_aether, current_lift, can_miss, len(pot_gains)



class AetherLiftCalculator(FormView):
  template_name = 'feh/calculator.html'
  form_class = forms.AetherLiftForm
  res = ''

  def get_context_data(self, *args, **kwargs):
    context = FormView.get_context_data(self, *args, **kwargs)
    context['res'] = self.res
    return context

  def form_valid(self, form):
    log, aether, lift, can_miss, matches = Calc(form.cleaned_data['aether'],
                                                form.cleaned_data['lift'],
                                                form.cleaned_data['reset_left'],
                                                form.cleaned_data['lift_gain'],
                                                form.cleaned_data['aether_storage_max'],
                                                form.cleaned_data['aether_regen'],)
    self.res = dict(
      log='\n'.join(log),
      aether=aether,
      lift=lift,
      can_miss=can_miss,
      matches=matches)
    return self.get(form)

aether_lift_calculator = AetherLiftCalculator.as_view()


class LucksackCalculator(FormView):
  template_name = 'feh/lucksack.html'
  form_class = forms.LucksackForm
  res = ''

  def get_context_data(self, *args, **kwargs):
    context = FormView.get_context_data(self, *args, **kwargs)
    context['res'] = self.res
    return context

  def form_valid(self, form):

    orbs = form.cleaned_data.get('orbs')

    ssr_focus = form.cleaned_data.get('five_star_focus_chance_total')
    ssr_pity = form.cleaned_data.get('five_star_pitybreaker_chance_total')

    ssr_f_sc = form.cleaned_data.get('number_of_other_focus_units_with_the_same_color_as_target')
    ssr_f_wc = form.cleaned_data.get('number_of_other_focus_units_with_different_color_than_target')

    ssr_n_sc = form.cleaned_data.get('number_of_five_star_units_with_the_same_color_as_target')
    ssr_n_wc = form.cleaned_data.get('number_of_five_star_units_with_different_color_than_target')

    com_n_sc = form.cleaned_data.get('number_of_four_star_or_lower_units_with_the_same_color_as_target')
    com_n_wc = form.cleaned_data.get('number_of_four_star_or_lower_units_with_different_color_than_target')

    already_in_pool = form.cleaned_data.get('is_target_unit_already_in_summonable_pool')

    total_focus_units = 1 + ssr_f_sc + ssr_f_wc
    total_ssr_units = ssr_n_sc + ssr_n_wc
    total_com_units = com_n_sc + com_n_wc

    units = [
      (1, 'red', 1, ssr_focus / total_focus_units),
      (2, 'red', 1, ssr_f_sc * ssr_focus / total_focus_units),
      (3, 'blue', 1, ssr_f_wc * ssr_focus / total_focus_units),
      #(4, 'red', 1, ssr_n_sc * ssr_pity / total_ssr_units),
      (5, 'blue', 1, ssr_n_wc * ssr_pity / total_ssr_units),
      (6, 'red', 0, com_n_sc * (1.0 - ssr_focus - ssr_pity) / total_com_units),
      (7, 'blue', 0, com_n_wc * (1.0 - ssr_focus - ssr_pity) / total_com_units),
    ]
    if already_in_pool:
      units.append((1, 'red', 1, ssr_pity / total_ssr_units))
      units.append((4, 'red', 1, (ssr_n_sc - 1) * ssr_pity / total_ssr_units))
    else:
      units.append((4, 'red', 1, ssr_n_sc * ssr_pity / total_ssr_units))

    sys.setrecursionlimit(10000)
    sackchance = FehSnipeProbability(orbs, units, 1)
    self.res = list(enumerate(sackchance))

    return self.get(form)

lucksack_calculator = LucksackCalculator.as_view()





