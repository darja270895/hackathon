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
from .NN.predict import Predict
from .helpers.configs.tours import TOURS

manager = TourManager()


def get_user_ans(request):
    if request.GET.get('q1'):
        ans_1 = request.GET['q1']
    else:
        ans_1 = 'None'
    if request.GET.get('q2'):
        ans_2 = request.GET['q2']
    else:
        ans_2 = 'None'
    if request.GET.get('q3'):
        ans_3 = request.GET['q3']
    else:
        ans_3 = 'None'
    if request.GET.get('q4'):
        ans_4 = request.GET['q4']
    else:
        ans_4 = 'None'
    if request.GET.get('q5'):
        ans_5 = request.GET['q5']
    else:
        ans_5 = 'None'
    if request.GET.get('q6'):
        ans_6 = request.GET['q6']
    else:
        ans_6 = 'None'
    if request.GET.get('q7'):
        ans_7 = request.GET['q7']
    else:
        ans_7 = 'None'
    if request.GET.get('q8'):
        ans_8 = request.GET['q8']
    else:
        ans_8 = 'None'
    if request.GET.get('q9'):
        ans_9 = request.GET['q9']
    else:
        ans_9 = 'None'
    if request.GET.get('q10'):
        ans_10 = request.GET['q10']
    else:
        ans_10 = 'None'
    if request.GET.get('q11'):
        ans_11 = request.GET['q11']
    else:
        ans_11 = 'None'
    data = f"'{ans_1}|" \
        f"{ans_2}|" \
        f"{ans_3}|" \
        f"{ans_4}|" \
        f"{ans_5}|" \
        f"{ans_6}|" \
        f"{ans_7}|" \
        f"{ans_8}|" \
        f"{ans_9}|" \
        f"{ans_10}|" \
        f"{ans_11}|" \
        f"'"
    return data


def home_page(request):
    message = get_user_ans(request)

    # print(f"Fuck Yea{message}")
    # # DATA
    # #########################################################################
    # limit = 5
    # lang = 'ru'  # OR lang = 'ru'
    # country_name = 'Germany'
    # # OR
    # city_name = 'Barcelona'
    # flights_params = {'origin': 'MSQ',
    #                   'destination': 'BER',
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
    #             'index': index + 1}
    #     user_info.append(data)
    # context = {'all_info': user_info}
    # return render(request, 'homepage.html', context)
    # return render(request, 'homepage.html')
    country_name = 'Испания'
    if request.GET.get('q1'):
        ans = request.GET['q1']
        if ans == 'нейтральные комфортные дни':
            country_name = 'Франция'
        elif ans == 'буйство стихии':
            country_name = 'Финляндия'
        else:
            country_name = 'Греция'



    tour_info = []
    for country in Country.objects.all():
        if country.rus_country_name == country_name:
            name = country.country_name
            info = TOURS
            country_data = info.get(name)
            excursions = country_data.get('Excursions')
            flights = country_data.get('Flights')
            hotels = country_data.get('Hotels')
            for index in range(5):
                tour_data = {
                    'excursion': excursions[index],
                    'flight': flights[index],
                    'hotel': hotels[index],
                }
                tour_info.append(tour_data)
    context = {'tour_info': tour_info}
    return render(request, 'homepage.html', context)


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
                user_data[0] = user_data[0].replace("'", "")
                user_data[10] = user_data[10].replace("'", "")
                # predict_instance = Predict([user_data])
                # country_name = predict_instance.predict_data()

        # country_name = 'Германия'
        from .NN.predict import get_data
        country_name = get_data(user_data)

        tour_info = []
        for country in Country.objects.all():
            if country.rus_country_name == country_name:
                name = country.country_name
                info = TOURS
                country_data = info.get(name)
                excursions = country_data.get('Excursions')
                flights = country_data.get('Flights')
                hotels = country_data.get('Hotels')
                for index in range(5):
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
