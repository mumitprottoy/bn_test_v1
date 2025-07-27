from django.urls import path
from . import views

urlpatterns = [
    path('pro-login', views.ProLoginAPI.as_view(), name='pro-login'),
    path('amateur-login', views.AmateurLoginAPI.as_view(), name='amateur-login'),
    path('create-user', views.UserRegisterAPI.as_view(), name='create-user'),

    # feed
    path('feed', views.PostFeedAPI.as_view()),

    # posts
    path('post/<int:post_id>', views.PostsByID.as_view()),
    path('post-by-uid/<str:uid>', views.PostsByUID.as_view()),
    path('user/posts', views.UserPostAPI.as_view()),
    path('user/post/click-like/<int:metadata_id>', views.PostClickLikeAPI.as_view()),
    path('user/post/add-comment/<int:metadata_id>', views.PostAddCommentAPI.as_view()),
    path('user/post/add-reply/<int:comment_id>', views.PostAddReplyAPI.as_view()),

    # stats
    path('user/stats/game-stats', views.GameStatsAPI.as_view()),
    path('user/stats/engagement-stats', views.EngagementStatsAPI.as_view()),
    path('user/follow', views.FollowAPI.as_view()),
    path('user/follow-count', views.FollowerCountAPI.as_view()),
    path('user/followers', views.FollowersAPI.as_view()),

    # pros
    path('user/pro-dashboard-data', views.ProDashboardAPI.as_view()),
    path('pro/profile/<str:username>', views.ProPlayerProfileByUsername.as_view()),

    # by user id
    path('user/profile/<str:username>', views.UserProfileByUsername.as_view()),
    path('user/<int:user_id>/posts', views.UserPostsByID.as_view()),

    # profile
    path('user/profile', views.PlayerProfileAPI.as_view()),
    path('user/pro-player-public-profile', views.ProPlayersPublicProfileAPI.as_view()),
    path('user/profile/upload-profile-picture', views.UploadProfilePictureAPI.as_view()),
    path('user/profile/upload-cover-photo', views.UploadCoverPhotoAPI.as_view()),

    # teams
    path('user/teams', views.TeamsAPI.as_view()),
    path('user/teams/<int:team_id>/delete', views.TeamDeletionAPI.as_view()),
    path('user/teams/<int:team_id>/members', views.TeamMembersAPI.as_view()),
    path('user/teams/invite', views.TeamInviteSendingAPI.as_view()),
    path('user/teams/invitations', views.UserTeamInvitationsAPI.as_view()),

    # users
    path('user-data', views.UserDataAPI.as_view()),

    # feedbacks
    path('feedback-types', views.FeedbackTypesAPI.as_view()),
    path('feedbacks', views.FeedbacksAPI.as_view()),

    # brands
    path('brands', views.BrandsAPI.as_view()),
    path('user/brands/favorites', views.FavoriteBrandAPI.as_view()),

    # tests
    path('test-image-upload', views.TestImageUploadAPI.as_view()),

    # chat
    path('chat/rooms', views.RoomsAPI.as_view()),
    path('chat/room/<int:room_id>/messages', views.ChatMessagesAPI.as_view()),
]