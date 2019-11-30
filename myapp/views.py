from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm

from .models import Country, UserData

from .tour_manager import TourManager
from .helpers.parser import loop
from .helpers.configs.tours import TOURS

manager = TourManager()


def home_page(request):
    # # DATA
    # #########################################################################
    # limit = 3
    # lang = 'ru'  # OR lang = 'ru'
    # country_name = 'Spain'
    # # OR
    # # city_name = 'Barcelona'
    # flights_params = {'origin': 'MSQ',
    #                   'destination': 'BCN',
    #                   'depart_date': '2020-01-01',  # Enter by user or constant
    #                   'return_date': '2020-12-31',  # Enter by user or constant
    #                   'limit': limit
    #                   }
    # #########################################################################
    # excursions, flights, hotels = loop.run_until_complete(
    #     manager.get_country_tour(country_name=country_name,
    #                              limit=limit,
    #                              flights_params=flights_params,
    #                              lang=lang))
    # user_info = []
    # for index in range(limit):
    #     data = {'excursion': excursions[index],
    #             'flight': flights[index],
    #             'hotel': hotels[index],
    #             'index': index+1}
    #     user_info.append(data)
    # context = {'user_info': user_info}
    # return render(request, 'homepage.html', context)
    return render(request, 'homepage.html')


def info(request):
    return render(request, 'info.html')


def tours(request):
    return render(request, 'tours.html')


def index(request):
    if request.user.is_authenticated:
        user_info = []
        username = request.user.username
        users = UserData.objects.all()
        for user in users:
            if username == user.username:
                user_data = user.data.split('|')
                data = {
                    'q1': user_data[0].replace("'", ""),
                    'q2': user_data[1],
                    'q3': user_data[2],
                    'q4': user_data[3],
                    'q5': user_data[4],
                    'q6': user_data[5],
                    'q7': user_data[6],
                    'q8': user_data[7],
                    'q9': user_data[8],
                    'q10': user_data[9],
                    'q11': user_data[10].replace("'", ""),
                }
                context = {'data': data}
                user_info.append(context)

        country_name = 'Испания'

        tour_info = []
        for country in Country.objects.all():
            if country.rus_country_name == country_name:
                name = country.country_name
                info = TOURS
                country_data = info.get(name)
                excursions = country_data.get('Excursions')
                flights = country_data.get('Flights')
                hotels = country_data.get('Hotels')
                for index in range(3):
                    tour_data = {
                        'excursion': excursions[index],
                        'flight': flights[index],
                        'hotel': hotels[index],
                    }

                    tour_info.append(tour_data)

        context = {'user_info': user_info, 'tour_info': tour_info}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


app_url = "/index/"


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = app_url + "login/"
    template_name = "reg/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "reg/login.html"
    success_url = app_url

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(app_url)


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    success_url = app_url + 'login/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)
