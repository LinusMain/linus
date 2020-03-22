from django.urls import path

from .views import (
    aether_lift_calculator,
)
from linus.feh.views import lucksack_calculator, HeroesList

app_name = "feh"
urlpatterns = [
    path("ar_calculator/", view=aether_lift_calculator, name="arcalc"),
    path("lucksack_calculator/", view=lucksack_calculator, name="lucksackcalc"),
    path("heroes/", view=HeroesList.as_view(), name="heroes_list"),
]

