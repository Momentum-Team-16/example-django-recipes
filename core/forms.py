from django import forms
from .models import Ingredient, Recipe, RecipeStep


TEXT_INPUT_CLASSES = "pa2 f4 w-100"


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "prep_time_in_minutes",
            "cook_time_in_minutes",
            "public",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": TEXT_INPUT_CLASSES}),
            "prep_time_in_minutes": forms.NumberInput(
                attrs={"class": TEXT_INPUT_CLASSES}
            ),
            "cook_time_in_minutes": forms.NumberInput(
                attrs={"class": TEXT_INPUT_CLASSES}
            ),
            "public": forms.CheckboxInput(attrs={"class": "ml2 mt2"}),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "amount",
            "item",
        ]


class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ["text"]

    widgets = {
        "text": forms.TextInput(attrs={"class": TEXT_INPUT_CLASSES}),
    }


class MealPlanForm(forms.Form):
    recipe = forms.ChoiceField(choices=[])
