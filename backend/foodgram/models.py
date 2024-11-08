from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_time, validate_color, validate_name
from .constants import LENGTH_NAME_OBJ, LENGTH_COLOR


User = get_user_model()


class NameObject(models.Model):
    """Абстрактный класс"""

    name = models.CharField(
        'Название',
        help_text='Укажите название',
        validators=(validate_name,),
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )

    class Meta:
        abstract = True


class Tag(NameObject):
    """Модель Тега"""

    color = models.CharField(
        'Цвет',
        help_text='Укажите цвет',
        max_length=LENGTH_COLOR,
        validators=(validate_color,),
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        help_text='Укажите слаг, поле должно быть уникальным',
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingridient(NameObject):
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=LENGTH_NAME_OBJ,
        help_text='Укажите единицу измерения',
    )

    class Meta:
        verbose_name_plural = 'Ingridients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_unit',
            )
        ]

    def __str__(self):
        return self.name


class Recipe(NameObject):
    """Модель рецепта"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        'Фотография',
        help_text='Добавьте фотографию рецепта',
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Опишите рецепт',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Укажите время приготовления',
        validators=(validate_time,),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Recipes'
        default_related_name = 'recipes'

    def __str__(self):
        return self.name


class RecipeIngridients(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients'
    )
    ingredients = models.ForeignKey(
        Ingridient,
        verbose_name='Ингредиенты',
        on_delete=models.CASCADE,
        related_name='+',
    )
    amount = models.SmallIntegerField(
        'количество',
        help_text='Укажите количество ингредиента',
        validators=(validate_time,),
    )

    class Meta:
        verbose_name_plural = 'RecipeIngridients'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='unique_recipe_ingredients',
            ),
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )

    class Meta:
        verbose_name_plural = 'FavoriteRecipes'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favourite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_purchase'
            )
        ]


class ImportFile(models.Model):
    file = models.FileField(upload_to='uploads/')
