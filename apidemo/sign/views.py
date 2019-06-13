from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
from sign.models import Event, Guest


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
    events = Event.objects.all()
    # for event in events:
    #     print(event.name)
    #     print(event.address)
    return render(request, "event_manage.html", {"user": username, "events": events})

@login_required
def search_name(request):
    search_name = request.GET.get("name")
    events = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"events": events})

@login_required
def guest_manage(request):
    username = request.user.username
    guests = Guest.objects.all()
    return render(request, "guest_manage.html", {"guests": guests})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect("/index")
    return response