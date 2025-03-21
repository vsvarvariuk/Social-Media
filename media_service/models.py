import pathlib
import uuid
from django.db import models
from django.utils.text import slugify


def upload_to(instance, filename):
    new_file_name = (f"{slugify(instance.first_name)-(uuid.uuid4())}"
    + pathlib.Path(filename).suffix)
    return f"uploads/profile/{new_file_name}"


class Profile(models.Model):
    first_name = models.CharField(max_length=155)

    last_name = models.CharField(max_length=155)

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

    image = models.ImageField(upload_to=upload_to_post,
                              blank=True,
                              null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at


class Like(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at


class Follow(models.Model):
    followed_profile = models.ForeignKey(Profile,
                                         on_delete=models.CASCADE,
                                         related_name="followers")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Follow {self.u} "
                f"{self.followed_profile.last_name} from {self.created_at}")
