# resume/models.py
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    """Модель профиля с личной информацией"""
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    position = models.CharField(max_length=200, verbose_name="Позиция")
    bio = models.TextField(verbose_name="О себе")
    photo = models.ImageField(upload_to='profile/', verbose_name="Фото")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    github_url = models.URLField(verbose_name="GitHub", blank=True)
    linkedin_url = models.URLField(verbose_name="LinkedIn", blank=True)
    telegram_url = models.URLField(verbose_name="Telegram", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активный профиль")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('profile_detail')

class Skill(models.Model):
    """Модель навыков"""
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'База данных'),
        ('devops', 'DevOps'),
        ('tools', 'Инструменты'),
        ('other', 'Другое'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, verbose_name="Название")
    level = models.IntegerField(
        default=50, 
        verbose_name="Уровень (1-100)",
        help_text="От 1 до 100"
    )
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='other',
        verbose_name="Категория"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.level}%)"

class Certificate(models.Model):
    """Модель сертификатов"""
    title = models.CharField(max_length=200, verbose_name="Название сертификата")
    organization = models.CharField(max_length=200, verbose_name="Организация")
    description = models.TextField(verbose_name="Описание")
    certificate_image = models.ImageField(upload_to='certificates/', verbose_name="Изображение сертификата")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    credential_id = models.CharField(max_length=100, blank=True, verbose_name="ID сертификата")
    credential_url = models.URLField(blank=True, verbose_name="Ссылка на верификацию")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"
        ordering = ['-issue_date', 'order']

    def __str__(self):
        return self.title

class Project(models.Model):
    """Модель проектов"""
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    short_description = models.CharField(max_length=300, verbose_name="Краткое описание")
    technologies = models.CharField(
        max_length=500, 
        verbose_name="Технологии",
        help_text="Перечислите технологии через запятую"
    )
    github_url = models.URLField(verbose_name="GitHub", blank=True)
    demo_url = models.URLField(verbose_name="Демо", blank=True)
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['-created_at', 'order']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]

class ProjectImage(models.Model):
    """Модель изображений проектов"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/', verbose_name="Изображение")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Изображение проекта"
        verbose_name_plural = "Изображения проектов"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Без подписи'}"