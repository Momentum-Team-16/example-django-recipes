from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ordered_model.admin import OrderedModelAdmin

from .models import RecipeStep, User, Recipe, Ingredient

admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Ingredient)


class RecipeStepAdmin(OrderedModelAdmin):
    list_display = ('order', 'recipe_id', 'text', 'move_up_down_links')


admin.site.register(RecipeStep, RecipeStepAdmin)
