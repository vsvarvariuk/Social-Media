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
    PostLikeUserDetail,
    AllProfileView,
    AllProfileDetailView,
    AllPostView,
)

router = routers.DefaultRouter()
router.register("my-profile", ProfileViewSet)
router.register("my-posts", PostViewSet)
router.register("my-likes", LikeViewSet)
router.register("my-comments", CommentViewSet)
router.register("my-subscriptions", FollowViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("profiles/", AllProfileView.as_view(), name="all_profiles"),
    path("profiles/<int:pk>/", AllProfileDetailView.as_view(), name="profile-detail"),
    path("my-followers/", UserFollowersView.as_view(), name="followers"),
    path("my-followers-posts/", UserFollowersPost.as_view(), name="my_followers_post"),
    path(
        "my-followers-posts/<int:pk>/",
        UserFollowerPostDetail.as_view(),
        name="my_followers_post_detail",
    ),
    path("all-posts/", AllPostView.as_view(), name="all_posts"),
    path("posts-like-me/", PostLikeUser.as_view(), name="like-post"),
    path(
        "posts-like-me/<int:pk>/", PostLikeUserDetail.as_view(), name="like-post-detail"
    ),
]
app_name = "media-service"
