from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Url
from django.contrib.sites.shortcuts import get_current_site
import random, string


def getAlias():
    return "".join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(8)])


def dashboard(request):
    if request.method == "POST":
        site = get_current_site(request)
        URL = request.POST["URL"]
        alias = request.POST.get("alias", None)
        if not alias:
            alias = getAlias()

        try:
            Url.objects.create(user=request.user, target_url=URL, alias=alias).save()
            messages.success(request, "shorted successfully.")
            return redirect("dashboard")
        except IndexError:
            messages.error(request, "Alias already in used")
            return render(request, "dashboard.html", {"url": URL, "alias": alias})
        except IntegrityError:
            messages.error(request, "Alias already in used")
            return render(request, "dashboard.html", {"url": URL, "alias": alias})
    site = get_current_site(request)
    return render(request, "dashboard.html",{"domain": site})
