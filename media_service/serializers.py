from rest_framework import serializers
from media_service.models import Profile, Post, Like, Comment, Follow

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "bio", "first_name", "last_name", "profile_picture", "birth_day", "location", "created_at")


class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "first_name", "last_name")


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
        fields = ("id", "comment", "created_at", "post")


class FollowSerializers(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ("id", "followed_profile", "created_at")
