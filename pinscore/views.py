from django.shortcuts import render


def pinscore(request):
    return render(request, 'pinscore.html')
