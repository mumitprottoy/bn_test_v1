from django.shortcuts import render


def add_questionnaire(request):
    return render(request, 'habijabi/add_questionnaire.html')
