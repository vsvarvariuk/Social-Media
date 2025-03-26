from django.urls import path, include
from rest_framework import routers

from media_service.views import (
    ProfileViewSet,
    PostViewSet,
    LikeViewSet,
    CommentViewSet,
    FollowViewSet,
    UserFollowersView,
    UserFollowersPost,
    PostLikeUser,
    UserFollowerPostDetail,
    PostLikeUserDetail
)

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
    path("myfollowers-posts/<int:pk>/", UserFollowerPostDetail.as_view(), name="myfollowers_post_detail"),
    path("posts-like-me/", PostLikeUser.as_view(), name="like-post"),
    path("posts-like-me/<int:pk>/", PostLikeUserDetail.as_view(), name="like-post-detail")
]
app_name = "media-service"
