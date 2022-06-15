from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.TextField()
    description = models.TextField()
    slug = models.SlugField(max_length=20, db_index=True, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст сообщения')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="posts",
        blank=True,
        null=True,
        verbose_name='Группа',
    )

    def __str__(self):
        return self.text

