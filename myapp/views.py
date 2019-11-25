from django.shortcuts import render


def home_page(request):
    return render(request, 'homepage.html')


def get_tour(request):
    return render(request, 'tour_agregator.html')


def info(request):
    return render(request, 'info.html')


def tours(request):
    return render(request, 'tours.html')


def login(request):
    return render(request, 'login_page.html')
