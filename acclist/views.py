from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the 'acclist' index.")

def alllist(request, user_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % user_id)

