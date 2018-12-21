from django.urls import path

from .views import (
    aether_lift_calculator,
)

app_name = "feh"
urlpatterns = [
    path("~ar_calculator/", view=aether_lift_calculator, name="arcalc"),
]

