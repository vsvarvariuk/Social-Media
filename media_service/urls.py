from django.urls import path, include
from rest_framework import routers

from media_service.views import ProfileViewSet, PostViewSet, LikeViewSet, CommentViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)
router.register("comments", CommentViewSet)
router.register("follows", FollowViewSet)
urlpatterns = [
    path("",include(router.urls))
]
app_name = "media-service"
