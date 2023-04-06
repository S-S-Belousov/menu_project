from django.shortcuts import render
from menu.models import MenuItem


def home_view(request):
    context = {
        'main_menu': MenuItem.objects.filter(named_url__isnull=True)
    }
    return render(request, "home.html", context)
