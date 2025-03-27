from django.db.models import Count
from rest_framework import viewsets, generics
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from media_service.models import Profile, Post, Comment, Like, Follow

from media_service.serializers import (
    ProfileSerializer,
    PostSerializers,
    CommentSerializers,
    LikeSerializers,
    FollowSerializers,
    ProfileListSerializer,
    PostDetailSerializer,
    FollowListSerializer,
    FollowDetailSerializer,
    FollowersSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.exclude(user=self.request.user)
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="first_name",
                type=str,
                description="Filter by first_name",
            ),
            OpenApiParameter(
                name="last_name",
                type=str,
                description="Filter bu last_name",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """Search profile for first_name or last_name"""
        return super().get(request, *args, **kwargs)


class AllProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(profile=self.request.user.profiles)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(profile=self.request.user.profiles)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializers


class AllPostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            Post.objects.exclude(profile__user=self.request.user)
            .select_related("profile", "profile__user")
            .prefetch_related("posts_comments", "likes")
            .annotate(comment_count=Count("posts_comments"), like_count=Count("likes"))
        )
        search_field = self.request.query_params.get("search", "").strip()
        if search_field:
            queryset = queryset.filter(content__icontains=search_field)

        return queryset.order_by("-created_at")

    @extend_schema(
        parameters=[
            OpenApiParameter(name="search", type=str, description="Search by word"),
        ]
    )
    def get(self, request, *args, **kwargs):
        """Search post by word"""
        return super().get(request, *args, **kwargs)


class UserFollowersPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        follow_profile = Follow.objects.filter(
            profile=self.request.user.profiles
        ).values_list("followed_profile", flat=True)
        queryset = Post.objects.filter(profile__in=follow_profile)
        search_field = self.request.query_params.get("search")
        if search_field:
            queryset = queryset.filter(content__icontains=search_field)
        return queryset


class UserFollowerPostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class PostLikeUser(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(likes__profile__user=self.request.user)


class PostLikeUserDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            Post.objects.all()
            .select_related("profile", "profile__user")
            .prefetch_related("posts_comments", "likes__profile")
        )
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(profile=self.request.user.profiles)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profiles)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers

    def get_queryset(self):
        return Like.objects.filter(profile=self.request.user.profiles)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profiles)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers

    def get_queryset(self):
        return Follow.objects.select_related("profile", "followed_profile").filter(
            profile=self.request.user.profiles
        )

    def perform_create(self, serializer):
        return serializer.save(profile=self.request.user.profiles)

    def get_serializer_class(self):
        if self.action == "list":
            return FollowListSerializer
        if self.action == "retrieve":
            return FollowDetailSerializer
        return FollowSerializers


class UserFollowersView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowersSerializer

    def get_queryset(self):
        queryset = Follow.objects.filter(followed_profile__user=self.request.user)
        return queryset
