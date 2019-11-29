from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=20)
    city_name = models.CharField(max_length=20)
    rus_city_name = models.CharField(max_length=20)
    rus_country_name = models.CharField(max_length=20)
    iata_code = models.CharField(max_length=4)
    country_id = models.IntegerField()
    city_id = models.IntegerField()


class UserData(models.Model):
    username = models.CharField(max_length=20)
    data = models.CharField(max_length=20)
