from django.urls import path
from django.views.decorators.cache import cache_page

from linus.feh.views import lucksack_calculator, HeroesList, RefreshHeroes

from .views import (
    aether_lift_calculator,
)


app_name = "feh"
urlpatterns = [
    path("ar_calculator/", view=aether_lift_calculator, name="arcalc"),
    path("lucksack_calculator/", view=lucksack_calculator, name="lucksackcalc"),
    path("heroes/", view=cache_page(60 * 60 * 24 * 30)(HeroesList.as_view()), name="heroes_list"),
    path("refresh_heroes/", view=cache_page(60)(RefreshHeroes.as_view()), name="heroes_refresh"),
]

