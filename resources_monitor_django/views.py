from django.shortcuts import render


def resources_view(request):
    return render(request, "index.html")