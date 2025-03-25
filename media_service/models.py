import pathlib
import uuid
from django.db import models
from django.utils.text import slugify
from social_media import settings


def upload_to(instance, filename):
    new_file_name = f"{slugify(instance.first_name)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return f"uploads/profile/{new_file_name}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="profiles")

    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)

    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(upload_to=upload_to,
                                        blank=True,
                                        null=True)

    birth_day = models.DateTimeField()
    location = models.CharField(max_length=155, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


def upload_to_post(instance, filename):
    new_file_name = f"{slugify(instance.user.first_name)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return f"uploads/post/{new_file_name}"


class Post(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name="posts")
    content = models.TextField()

    image = models.ImageField(upload_to=upload_to_post,
                              blank=True,
                              null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class Like(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name="liked_posts")

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "post"], name="unique_like")
        ]


class Comment(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class Follow(models.Model):
    profile = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             related_name="follower")
    followed_profile = models.ForeignKey(Profile,
                                         on_delete=models.CASCADE,
                                         related_name="followers")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "followed_profile"], name="unique_follow")
        ]

    def __str__(self):
        return (f"{self.profile.first_name} {self.profile.last_name} "
                f"follow {self.followed_profile.first_name} {self.followed_profile.last_name} "
                f"from {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
