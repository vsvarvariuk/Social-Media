from rest_framework import serializers
from media_service.models import Profile, Post, Like, Comment, Follow

class ProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "profile_picture", "birth_day", "location", "created_at")


class PostSerializers(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "content", "image", "created_at")


class LikeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ("id", "post")


class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "comment", "created_at")


class FollowSerializers(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ("id", "followed_profile", "created_at")