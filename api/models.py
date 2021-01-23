from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='images')
    name = models.CharField(max_length=128)
    image_url = models.URLField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='likes')
    image = models.ForeignKey(Image, on_delete=models.CASCADE,
                              related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'image'],
                name='unique like'
            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.image.name}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')
    image = models.ForeignKey(Image, on_delete=models.CASCADE,
                              related_name='comments')
    text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user.username} -> {self.image.name} -> {self.text}'
