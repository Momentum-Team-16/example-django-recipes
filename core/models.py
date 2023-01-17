from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from ordered_model.models import OrderedModel
from django.db.models.constraints import UniqueConstraint
from django_toggle_m2m.toggle import ToggleManyToMany


class User(AbstractUser):
    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"


# https://docs.djangoproject.com/en/4.0/topics/db/managers/#adding-extra-manager-methods
class RecipeManager(models.Manager):
    def for_user(self, user):
        if user.is_authenticated:
            recipes = self.filter(Q(public=True) | Q(author=user))
        else:
            recipes = self.filter(public=True)
        return recipes


class Recipe(models.Model):
    objects = RecipeManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=255)
    prep_time_in_minutes = models.PositiveIntegerField(null=True, blank=True)
    cook_time_in_minutes = models.PositiveIntegerField(null=True, blank=True)
    original_recipe = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, null=True, blank=True
    )
    public = models.BooleanField(default=True)
    favorited_by = models.ManyToManyField(
        User, related_name="favorite_recipes", blank=True
    )

    def total_time_in_minutes(self):
        if self.cook_time_in_minutes is None or self.prep_time_in_minutes is None:
            return None
        return self.cook_time_in_minutes + self.prep_time_in_minutes

    def __str__(self):
        return self.title


# https://github.com/django-ordered-model/django-ordered-model
class RecipeStep(OrderedModel):
    recipe = models.ForeignKey(
        to=Recipe, on_delete=models.CASCADE, related_name="steps"
    )
    text = models.TextField()
    order_with_respect_to = "recipe"

    def __str__(self):
        return f"{self.order} {self.text}"


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    amount = models.CharField(max_length=20)
    item = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.amount} {self.item}"


class MealPlan(models.Model, ToggleManyToMany):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plans")
    date = models.DateField(verbose_name="Date for plan")
    recipes = models.ManyToManyField(Recipe, related_name="meal_plans")

    TOGGLEABLE_FIELDS = ("recipes",)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "date"], name="unique_user_date")
        ]

    def add_or_remove_recipe(self, recipe):
        self.toggle_recipes(instance=recipe)
