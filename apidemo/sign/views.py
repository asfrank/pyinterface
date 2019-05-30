from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")

def login_action(request):
    login_username = request.POST.get("username")
    login_password = request.POST.get("password")
    if login_username == "" or login_password == "":
        return render(request, "index.html", {"error": "username or password is null"})

    return HttpResponse("login ok")