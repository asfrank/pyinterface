from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == "POST":
        login_username = request.POST.get("username")
        login_password = request.POST.get("password")
        if login_username == "" or login_password == "":
            return render(request, "index.html", {"error": "username or password is null"})
        elif login_username == "admin" and login_password == "123":
            response = HttpResponseRedirect('/event_manage')
            # response.set_cookie("user", login_username, 10)
            request.session["user"] = login_username
            return response
        return render(request, "index.html", {"error": "username or password error"})
    else:
        return render(request, "index.html")


def event_manage(request):
    username = request.session.get("user", "")
    return render(request, "event_manage.html", {"user": username})