from django.urls import path
from . import views

urlpatterns = [
    path('pro-login', views.ProLoginAPI.as_view(), name='pro-login'),

    # posts
    path('user/posts', views.UserPostAPI.as_view()),
    path('user/post/click-like/<int:metadata_id>', views.PostClickLikeAPI.as_view()),
    path('user/post/add-comment/<int:metadata_id>', views.PostAddCommentAPI.as_view()),
    path('user/post/add-reply/<int:comment_id>', views.PostAddReplyAPI.as_view()),

    # stats
    path('users/stats', views.StatsAPI.as_view()),

    # profile
    path('user/profile', views.PlayerProfileAPI.as_view()),

    # weighted index
    path('weighted-index', views.WeightedIndexAPI.as_view()),
]