from django.contrib import admin
from django.urls import path, include
from entrance import views as entrance_views
from player import views as player_views
from pinscore.views import pinscore


urlpatterns = [
    path('api/', include('api.urls')),
    # path('', player_views.myprofile, name='my-profile'),
    path('', player_views.home_view, name='home'),
    path('referral/', player_views.referral, name='referral'),
    path('public-profile/<str:handle>', player_views.public_profile, name='public-profile'),
    path('save-stats/', player_views.save_stats, name='save-stats'),
    # path('my-teams/', player_views.my_teams, name='my_teams'),
    # path('create-team/', player_views.create_team, name='create_team'),
    # path('team-invitations/', player_views.invitations_list, name='invitations_list'),
    # path('respond-to-invitation/<int:invite_id>', player_views.respond_invitation, name='respond_invitation'),
    # path('team/<int:team_id>/', player_views.team_detail_view, name='team_detail'),
    path('my-profile/', player_views.user_profile, name='user_profile'),
    path("change-profile-pic/", player_views.change_profile_pic, name="change_profile_pic"),
    path("upload-profile-pic/", player_views.upload_profile_picture, name="upload_profile_pic"),
    # path('sent-invitations/', player_views.sent_invitations_view, name='sent_invitations'),
    # path('sent-invitations/withdraw/<int:invitation_id>/', player_views.withdraw_invitation_view, name='withdraw_invitation'),
    # path('team/<int:team_id>/add-member/', player_views.add_member_view, name='add_member'),
    # path('team/<int:team_id>/remove-member/<int:member_id>/', player_views.remove_member_view, name='remove_member'),
    path('random/', entrance_views.random_shift, name='random_shift'),
    path('random-shift-api/<int:cycle>', entrance_views.random_shift_api),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', entrance_views.login, name='login'),
    path('i/<str:channel>', entrance_views.signup, name='signup'),
    path('base/', entrance_views.base_, name='base'),
    path('logout/', entrance_views.logout, name='logout'),
    path('pinscore', pinscore, name='pinscore'),
]
