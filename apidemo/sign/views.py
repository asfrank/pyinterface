from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == "POST":
        login_username = request.POST.get("username")
        login_password = request.POST.get("password")
        if login_username == "" or login_password == "":
            return render(request, "index.html", {"error": "username or password is null"})
        else:
            user = auth.authenticate(username = login_username, password = login_password)
            if user is not None:
                auth.login(request, user)
                response = HttpResponseRedirect('/event_manage')
                # response.set_cookie("user", login_username, 10)
                # request.session["user"] = login_username
                return response
            return render(request, "index.html", {"error": "username or password error"})
    else:
        return render(request, "index.html")

@login_required
def event_manage(request):
    # username = request.session.get("user", "")
    username = request.user.username
    return render(request, "event_manage.html", {"user": username})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect("/index")
    return response