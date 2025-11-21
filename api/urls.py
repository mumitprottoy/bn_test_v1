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
    path('user/post/vote/<int:option_id>', views.PollVoteAPI.as_view()),
    path('reports/post', views.ReportPostAPI.as_view()),

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

    # profiles
    path('user/profile', views.PlayerProfileAPI.as_view()),
    path('user/pro-player-public-profile', views.ProPlayersPublicProfileAPI.as_view()),
    path('user/profile/upload-profile-picture/', views.UploadProfilePictureAPI.as_view()),
    path('user/profile/upload-cover-photo/', views.UploadCoverPhotoAPI.as_view()),
    path('user/profile/upload-intro-video/', views.UploadIntroVideoAPI.as_view()),
    path('cities', views.CountriesAPI.as_view()),
    path('secret-delete', views.SecretDeleteUserAPI.as_view()),
    path('user/info', views.UserInfoAPI.as_view()),
    path('user/profile-status', views.ProfileStatusAPI.as_view()),
    path('user/media', views.UserMediaAPI.as_view()),

    # teams
    path('user/teams', views.TeamsAPI.as_view()),
    path('user/teams/<int:team_id>/delete', views.TeamDeletionAPI.as_view()),
    path('user/teams/<int:team_id>/members', views.TeamMembersAPI.as_view()),
    path('user/teams/<str:team_id>/upload-logo', views.UploadTeamLogoAPI.as_view()),
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

    # entrance
    path('send-invite-with-csv-file', views.SendInvitesWithCSVFileAPI.as_view()),
    path('send-verification-code', views.SendEmailVerificationCode.as_view()),
    path('verify-email', views.VerifyEmailAPI.as_view()),
    path('pre-register', views.PreRegistrationAPI.as_view()),
    path('validate-signup-data', views.SignupDataValidationAPI.as_view()),
    path('validate-username', views.UsernameValidationAPI.as_view()),
    path('send-otp', views.OTPSendingAPI.as_view()),
    path('reset-password', views.PasswordResetAPI.as_view()),

    # centers
    path('center', views.CentersAPI.as_view()),
    path('all-centers', views.AllCentersAPI.as_view()),
    path('center-by-id/<int:center_id>', views.CenterByIDAPI.as_view()),
    path('get-center-by-current-user', views.GetCenterDataByCurrentUserAPI.as_view()),

    # tournaments
    path('tournaments', views.TournamentsAPI.as_view()),
    path('all-tournaments', views.AllTournamentsAPI.as_view()),
    path('tournament/<int:tournament_id>/add-singles-member/<int:user_id>', views.AddSinglesMemberAPI.as_view()),
    path('tournament/<int:tournament_id>/add-teams-member/<int:team_id>', views.AddTeamsMemberAPI.as_view()),
    path('tournament/<int:tournament_id>/teams', views.TournamentAllTeamsAPI.as_view()),
    path('tournaments/v0', views.TournamentsV0API.as_view()),
    path('tournaments/v0/delete/<int:tournament_id>', views.TournamentsV0DeleteAPI.as_view()),
    path('tournaments/v0/upload-flyer/<int:tournament_id>', views.TournamentV0FlyerUploadAPI.as_view()),
    path('tournaments/v0/publish/<int:tournament_id>', views.PublishTournamentV0API.as_view()),

    # Deletion
    path('delete-account', views.DeleteAccountAPI.as_view()),

    # Test
    path('test-address', views.TestAdressAPI.as_view()),
    path('test-payload', views.TestPayloadAPI.as_view()),

    # habijabi
    path('add-question', views.AddQuestionAPI.as_view()),
    path('all-questions', views.AllQuestionsAPI.as_view()),
    path('edit-question/<int:ques_id>', views.EditQuestionAPI.as_view()),
    path('delete-question/<int:ques_id>', views.DeleteQuestionAPI.as_view()),
    path('serialize-questions', views.SerializeQuestionsAPI.as_view()),
    path('validate-security-code', views.ValidateSecurityCodeAPI.as_view()), 
    path('send-private-url/<int:pro_onb_id>', views.PrivateURLEmailAPI.as_view()),
    path('pro-info', views.ProInfoAPI.as_view()),
    path('pros-private-signup', views.ProsPrivateOnboardingAPI.as_view()),
    path('pros-private-auth', views.ProsPrivateAuthAPI.as_view()),
    path('submit-answer-by-ques-id/<int:ques_id>', views.SubmitAnswerByQuesIDAPI.as_view()),
    path('submit-survey', views.SubmitSurveyAPI.as_view()),
    path('pro-survey', views.ProSurveyAPI.as_view()),

    # Games
    path('games', views.GamesAPI.as_view()),
    path('games/delete/<int:game_id>', views.DeleteGameAPI.as_view()),

    # beta
    path('private-login', views.BetaPrivateAccessAPI.as_view()),

    # lanes
    path('lanes/discussions', views.DiscussionAPI.as_view()),
    path('lanes/discussions/topics', views.DiscussionTopicAPI.as_view()),
    path('lanes/discussions/feed', views.DiscussionFeedAPI.as_view()),
    path('lanes/discussions/vote', views.DiscussionVoteAPI.as_view())
]