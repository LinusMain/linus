from django.contrib import admin

from . import models
from advanced_filters.admin import AdminAdvancedFiltersMixin

# Register your models here.
@admin.register(models.Hero)

class HeroAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
  list_display  = ('name',
                   'title',
                   'is_f2p',
                   'movement_type',
                   'weapon_type',
                   'color',
                   'hp',
                   'attack',
                   'speed',
                   'defense',
                   'resistance',
                   'bst',
                   'generation',
                   )

  search_fields = ('name',
                   'title',
                   'movement_type',
                   'weapon_type',
                   'color',
                   'availability',)

  list_filter = ('is_f2p',
                 'movement_type',
                 'weapon_type',
                 'color',
                 'availability',
                 'book',
                 'generation',
                 )
  # simple list filters

  # specify which fields can be selected in the advanced filter
  # creation form
  advanced_filter_fields = ('name',
                            'title',
                            'is_f2p',
                            'availability',
                            'movement_type',
                            'weapon_type',
                            'color',
                            'hp',
                            'attack',
                            'speed',
                            'defense',
                            'resistance',
                            'bst',
                            'book',
                            'generation',
                            'release_date',)



