from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Team, TeamInvitation, XPMap

@login_required
def home_view(request):
    top_20_users = User.objects.all().order_by('-xp')[:20]
    top_3 = top_20_users[:3]
    context = {
        'top_3': top_3,
        'top_20': top_20_users,
    }
    print(context)
    return render(request, 'player/home.html', context)

@login_required
def referral(request):
    reward_xp = XPMap.objects.get(trigger_codename='onboarding').xp_worth
    return render(request, 'player/referral.html', {'reward_xp': reward_xp})

@login_required(login_url='/login/')
def myprofile(request):
    return render(request, 'player/myprofile.html')


@login_required(login_url='/login/')
def save_stats(request):
    if request.method == 'POST':
        fields = ['average_score', 'high_game', 'high_series', 'experience']
        for f in fields:
            setattr(request.user.stats, f, request.POST.get(f, getattr(request.user.stats, f)))
        request.user.stats.save()
        return redirect('user_profile')


@login_required(login_url='/login/')
def public_profile(request, handle: str):
    user = get_object_or_404(User, username=handle)
    return render(request, 'player/public_profile.html', {'user_obj': user})


@login_required
def my_teams(request):
    teams = request.user.teams.all().prefetch_related('members')
    return render(request, 'player/my_teams.html', {'teams': teams})


@login_required
def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('team_name')
        member_ids = request.POST.getlist('members')
        team = Team.objects.create(name=name, created_by=request.user)
        team.members.add(request.user)
        for user_id in member_ids:
            invited_user = User.objects.get(id=user_id)
            TeamInvitation.objects.create(team=team, invited_user=invited_user)
        return redirect('team_detail', team_id=team.id)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'player/create_team.html', {'users': users})


@login_required
def invitations_list(request):
    invites = TeamInvitation.objects.filter(invited_user=request.user, status='pending')
    return render(request, 'player/invitations_list.html', {'invitations': invites})


@login_required
def respond_invitation(request, invite_id):
    invitation = get_object_or_404(TeamInvitation, id=invite_id, invited_user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            invitation.status = 'accepted'
            invitation.save()
            invitation.team.members.add(request.user)
        elif action == 'reject':
            invitation.status = 'rejected'
            invitation.save()
        return redirect('invitations_list')

    return render(request, 'player/respond_invitation.html', {'invite': invitation})


@login_required
def sent_invitations_view(request):
    sent_invitations = TeamInvitation.objects.filter(
        team__created_by=request.user,
        status='pending'
    ).select_related('team', 'invited_user')
    return render(request, 'player/sent_invitations.html', {'sent_invitations': sent_invitations})


@login_required
def withdraw_invitation_view(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, id=invitation_id, team__created_by=request.user)
    if request.method == 'POST':
        invitation.delete()
        return redirect('sent_invitations')
    return redirect('sent_invitations')


@login_required
def team_detail_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.members.all():
        return redirect('my_teams')
    return render(request, 'player/team_detail.html', {'team': team})


@login_required
def add_member_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user != team.created_by:
        messages.error(request, "Only the team owner can add members.")
        return redirect('team_detail', team_id=team.id)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        try:
            user_to_add = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' does not exist.")
            return redirect('team_detail', team_id=team.id)

        if user_to_add in team.members.all():
            messages.warning(request, f"User '{username}' is already a member.")
        else:
            try:
                TeamInvitation.objects.create(team=team, invited_user=user_to_add)
                messages.success(request, f"Invitation sent to user: '{username}'")
            except Exception as e: messages.error(request, str(e))
    return redirect('team_detail', team_id=team.id)


@login_required
def remove_member_view(request, team_id, member_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user != team.created_by:
        messages.error(request, "Only the team owner can remove members.")
        return redirect('team_detail', team_id=team.id)

    member = get_object_or_404(User, id=member_id)
    if request.method == 'POST':
        if member in team.members.all():
            team.members.remove(member)
            messages.success(request, f"User '{member.username}' has been removed from the team.")
        else:
            messages.warning(request, f"User '{member.username}' is not a member of the team.")

    return redirect('team_detail', team_id=team.id)


@login_required
def user_profile(request):
    return render(request, 'player/user_profile.html', {'user_obj': request.user})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@login_required
def upload_profile_picture(request):
    return render(request, 'player/change_profile_pic.html', {'user_obj': request.user})


@csrf_exempt
@login_required
def change_profile_pic(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            image_data = data.get("image_data")
            if image_data:
                request.user.profile_picture_url = image_data
                request.user.save()
                return JsonResponse({"message": "✅ Profile picture updated!"})
            return JsonResponse({"message": "❌ No image data received."}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"❌ Error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Invalid method"}, status=405)
