
from django.db import models
from django.contrib.auth.models import User


# レシピテーブル
class Recipe(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    title = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='recipe_images/',
        blank=True,
        null=True
    )

    reference_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# 材料テーブル
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    sort_order = models.IntegerField()

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.name


# 作り方テーブル
class RecipeStep(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps'
    )

    instruction = models.CharField(max_length=100)
    step_number = models.IntegerField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f'{self.step_number}: {self.instruction}'
