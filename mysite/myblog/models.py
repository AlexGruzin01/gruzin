from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
import re
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
def validate_phone(value):
    """Валидация номера телефона"""
    pattern = r'^\+375 \(\d{2}\) \d{3} \d{2} \d{2}$'
    if not re.match(pattern, value):
        raise ValidationError('Телефон должен быть в формате: +375 (99) 999-99-99')


class Category(MPTTModel):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    description = models.CharField(blank=True, null=True, verbose_name='Описание')
    content = models.TextField(verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменён')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото", blank=True, null=True)
    page_image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото страницы", blank=True, null=True)
    top_img = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Верхнее фото", blank=True, null=True)
    bottom_img = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Нижнее фото", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    # tags = models.ManyToManyField(PostTags, related_name='tags', verbose_name='Теги', blank=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['order', '-created']

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    description = models.TextField(blank=True, null=True,verbose_name='Описание')
    content = models.TextField(verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news', verbose_name='Категория', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменён')
    image = models.ImageField(upload_to='photos/news/%Y/%m/%d', verbose_name="Фото", blank=True, null=True)
    top_img = models.ImageField(upload_to='photos/news/%Y/%m/%d', verbose_name="Верхнее фото", blank=True, null=True)
    bottom_img = models.ImageField(upload_to='photos/news/%Y/%m/%d', verbose_name="Нижнее фото", blank=True, null=True)
    # tags = models.ManyToManyField(PostTags, related_name='tags', verbose_name='Теги', blank=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def get_absolute_url(self):
        return reverse('new', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Site(models.Model):
    phone = models.CharField(verbose_name='Телефон', blank=True, null=True, validators=[validate_phone])
    email = models.EmailField(verbose_name='Email', blank=True)
    logo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)

    class Meta:
        verbose_name = 'Инфо'
        verbose_name_plural = 'Инфо'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        # Разрешаем только одну запись
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Автоматически создаем запись если её нет
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Reviews(models.Model):
    reviewer = models.CharField(max_length=250)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    organization = models.CharField(verbose_name='Организация')
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return 'Отзывы'


class Projects(models.Model):
    title = models.CharField(verbose_name='Название')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание')
    content = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    is_multi = models.BooleanField(default=False, verbose_name='Мульти слайдер')
    year = models.CharField(max_length=10, verbose_name='Год', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', blank=True, null=True, verbose_name='Изображение')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея изображений'

    def __str__(self):
        return 'Картинка'