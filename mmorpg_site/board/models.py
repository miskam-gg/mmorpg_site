from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Advertisement(models.Model):
    CATEGORY_CHOICES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DPS', 'ДД'),
        ('Merchants', 'Торговцы'),
        ('GuildMasters', 'Гилдмастеры'),
        ('QuestGivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Alchemists', 'Зельевары'),
        ('Spellcasters', 'Мастера заклинаний'),
    ]
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)

    def get_absolute_url(self):
        return reverse('advertisement_detail', args=[str(self.pk)])


class Response(models.Model):
    text = models.TextField()
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True, blank=True)
    responder = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    is_accepted = models.BooleanField(default=False)
