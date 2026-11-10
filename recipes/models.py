
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage

PRIVATE_MEDIA_ROOT = settings.PRIVATE_MEDIA_ROOT

# レシピテーブル
class Recipe(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )

    title = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to="recipes/",
        blank=True,
        null=True,
        storage=FileSystemStorage(
            location=PRIVATE_MEDIA_ROOT
        )
    )

    reference_url = models.URLField(
        blank=True,
        null=True
    )
    memo = models.TextField(
        blank=True,
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
        related_name="ingredients"
    )

    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    sort_order = models.IntegerField()

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.name


# 作り方テーブル
class RecipeStep(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="steps"
    )

    instruction = models.CharField(max_length=100)
    step_number = models.IntegerField()

    class Meta:
        ordering = ["step_number"]

    def __str__(self):
        return f"{self.step_number}：{self.instruction}"
