from django.urls import path, include
from rest_framework import routers

from media_service.views import ProfileViewSet, PostViewSet, LikeViewSet, CommentViewSet, FollowViewSet, \
    UserFollowersView, UserFollowersPost, PostLikeUser

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)
router.register("comments", CommentViewSet)
router.register("follows", FollowViewSet)
urlpatterns = [
    path("",include(router.urls)),
    path("myfollowers/", UserFollowersView.as_view(), name="followers"),
    path("myfollowers-posts/", UserFollowersPost.as_view(), name="myfollowers_post"),
    path("posts-like-me/", PostLikeUser.as_view(), name="like-post")
]
app_name = "media-service"
