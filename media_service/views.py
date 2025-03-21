from django.shortcuts import render
from rest_framework import viewsets
from media_service.models import (Profile,
                                  Post,
                                  Comment,
                                  Like,
                                  Follow)

from media_service.serializers import (ProfileSerializers,
                                       PostSerializers,
                                       CommentSerializers,
                                       LikeSerializers,
                                       FollowSerializers)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers
