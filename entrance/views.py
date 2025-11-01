from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as _login, logout as _logout, get_user_model
from .models import OnBoarding, PreRegistration
from django.http import JsonResponse

User = get_user_model()

def login(request):
    context = dict()
    if request.user.is_authenticated:
        return redirect('/')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if authenticate(
            request, username=username, password=password):
            user = get_user_model().objects.get(username=username)
            _login(request, user)
            return redirect('/')
        context['error_message'] = 'Invalid credentials'
    return render(request, 'entrance/login.html', context)


def signup(request, channel: str):
    context = dict()
    
    if request.POST:
        kwargs = dict(first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        username = request.POST['username'],
        email = request.POST['email'])
        password = request.POST['password']
        user = None
        try:
            user = User.objects.create(**kwargs)
        except Exception as e:
            context['error_message'] = str(e)
        if user is not None:
            user.set_password(password)
            user.save()
            sender = User.objects.filter(username=channel).first()
            OnBoarding.objects.create(user=user, channel=sender)
            return redirect('/login/')
    return render(request, 'entrance/signup.html', context)
        

def base_(request):
    return render(request, 'base.html')

def logout(request):
    _logout(request)
    return redirect('login')

def random_shift(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'random_shift.html')
    return redirect('home')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def random_shift_api(request, cycle: int):
    from django.http import JsonResponse
    import random
    print('In random,', f'{cycle} rounds')
    for _ in range(int(cycle)):
        print('round', _+1)
        for user in User.objects.all():
            shift = random.randint(-2, 20)
            user.xp += shift
            user.save()
        try:
            haha = User.objects.get(email='mumitprottoy@gmail.com')
            max_xp = User.objects.all().order_by('-xp').first().xp
            haha.xp = max_xp + random.randint(1,10)
            haha.save()
        except Exception as e:
            print(str(e))
    return JsonResponse({'message': 'OK'})


def splash(request):
    return render(request, 'splash/splash_demo.html')


def pre_registrations(request):
    total = PreRegistration.objects.count()
    pre_regs = PreRegistration.objects.all().order_by('-id')
    return render(request, 'pre_reg.html', context={'pre_regs': pre_regs, 'total': total})


def pre_registration_json(request):
    pre_regs = [pr.details for pr in PreRegistration.objects.filter(
        is_activated=True).order_by('id')]
    return JsonResponse(dict(pre_registers=pre_regs))