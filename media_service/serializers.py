from rest_framework import serializers
from media_service.models import Profile, Post, Like, Comment, Follow


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            "id",
            "bio",
            "first_name",
            "last_name",
            "profile_picture",
            "birth_day",
            "location",
            "created_at",
        )


class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "first_name", "last_name")


class LikeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ("id", "post")


class LikePostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="profile.full_name")

    class Meta:
        model = Like
        fields = ("user",)


class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "comment", "created_at", "post")


class CommentPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="profile.full_name")

    class Meta:
        model = Comment
        fields = ("user", "comment")


class PostSerializers(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "content", "image", "comments", "likes", "created_at")

    def get_comments(self, obj):
        return obj.posts_comments.count()

    def get_likes(self, obj):
        return obj.likes.count()


class PostDetailSerializer(serializers.ModelSerializer):
    posts_comments = CommentPostSerializer(many=True, read_only=True)
    user = serializers.CharField(source="profile.full_name")
    likes = LikePostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "content",
            "image",
            "likes",
            "posts_comments",
            "created_at",
        )


class FollowSerializers(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ("id", "followed_profile", "created_at")


class FollowListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="followed_profile.full_name")

    class Meta:
        model = Follow
        fields = ("id", "full_name")


class FollowersSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="profile.full_name")

    class Meta:
        model = Follow
        fields = ("id", "full_name")


class FollowDetailSerializer(serializers.ModelSerializer):
    followed_profile = ProfileSerializer()

    class Meta:
        model = Follow
        fields = ("id", "followed_profile")
