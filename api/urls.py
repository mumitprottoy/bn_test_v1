from django.urls import path
from . import views

urlpatterns = [
    path('pro-login', views.ProLoginAPI.as_view(), name='pro-login'),

    # feed
    path('feed', views.PostFeedAPI.as_view()),

    # posts
    path('user/posts', views.UserPostAPI.as_view()),
    path('user/post/click-like/<int:metadata_id>', views.PostClickLikeAPI.as_view()),
    path('user/post/add-comment/<int:metadata_id>', views.PostAddCommentAPI.as_view()),
    path('user/post/add-reply/<int:comment_id>', views.PostAddReplyAPI.as_view()),

    # stats
    path('user/stats/game-stats', views.GameStatsAPI.as_view()),
    path('user/stats/engagement-stats', views.EngagementStatsAPI.as_view()),

    # pro dashboard
    path('user/pro-dashboard-data', views.ProDashboardAPI.as_view()),


    # profile
    path('user/profile', views.PlayerProfileAPI.as_view()),
]