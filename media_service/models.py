import pathlib
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def upload_to(instance, filename):
    new_file_name = (f"{slugify(instance.user.first_name)-(uuid.uuid4())}"
    + pathlib.Path(filename).suffix)
    return f"uploads/profile/{new_file_name}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="profiles")

    profile_picture = models.ImageField(upload_to=upload_to,
                                        blank=True,
                                        null=True)

    birth_day = models.DateTimeField()
    location = models.CharField(max_length=155, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


def upload_to_post(instance, filename):
    new_file_name = (f"{slugify(instance.user.first_name)-(uuid.uuid4())}"
    + pathlib.Path(filename).suffix)
    return f"uploads/post/{new_file_name}"


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="posts")

    image = models.ImageField(upload_to=upload_to_post,
                              blank=True,
                              null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.user.first_name} {self.user.last_name}"
                f" ({self.created_at})")


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="posts")

    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="posts")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name="following")

    followed = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name="followers")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "followed"], name="unique_follow")
        ]

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
