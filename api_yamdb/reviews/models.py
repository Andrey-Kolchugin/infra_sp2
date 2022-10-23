from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validation

User = get_user_model()


class Category(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=256, db_index=True,
                            help_text='Название категории')
    slug = models.SlugField(max_length=256, unique=True,
                            help_text='Уникальный URL категории.')

    class Meta:
        verbose_name = 'Категория'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название жанра произведения',
                            help_text='Введите название жанра')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название произведения',
                            help_text='Введите название произведения')
    year = models.PositiveSmallIntegerField(validators=[year_validation],
                                            verbose_name='Дата выпуска',
                                            help_text='Введите дату выпуска')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание произведения',
                                   help_text='Введите описание произведения')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name='titles', blank=True, null=True,
                                 verbose_name='Категория')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles', blank=True,
                                   verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Отзыв',
        help_text='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews',

    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1, message='Значение должно быть от 1 до 10'),
            MaxValueValidator(10, message='Значение должно быть от 1 до 10')
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments',
    )
    text = models.CharField(
        'Текст комментария',
        max_length=300,
        help_text='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
