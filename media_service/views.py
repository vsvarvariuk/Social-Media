from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from media_service.models import (Profile,
                                  Post,
                                  Comment,
                                  Like,
                                  Follow)

from media_service.serializers import (ProfileSerializer,
                                       PostSerializers,
                                       CommentSerializers,
                                       LikeSerializers,
                                       FollowSerializers, ProfileListSerializer)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.all()
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        return ProfileSerializer



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


class UserFollowersPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def get_queryset(self):
        follow_profile = Follow.objects.filter(profile=self.request.user.profiles).values_list("followed_profile", flat=True)
        queryset = Post.objects.filter(profile__in=follow_profile)
        return queryset



class PostLikeUser(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def get_queryset(self):
        return Post.objects.filter(likes__profile__user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profiles)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profiles)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers

    def get_queryset(self):
        queryset = Follow.objects.filter(profile=self.request.user.profiles)
        return queryset


    def perform_create(self, serializer):
        return serializer.save(profile=self.request.user.profiles)


class UserFollowersView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers

    def get_queryset(self):
        queryset = Follow.objects.filter(followed_profile__user=self.request.user)
        return queryset