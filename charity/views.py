from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from charity.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        quantity = list(Donation.objects.aggregate(Sum('quantity')).values())[0]
        institutions = Institution.objects.count()
        # institutions = list(Donation.objects.aggregate(Count('institution')).values())[0]
        foundations = Institution.objects.filter(type=0)
        organisations = Institution.objects.filter(type=1)
        locals = Institution.objects.filter(type=2)

        return render (request, "index.html", context={"quantity":quantity, "institutions":institutions, "foundations":foundations,
                                                       "organisations":organisations, "locals":locals})


class AddDonation (View):
    def get (self, request):
        category =Category.objects.all()
        return render (request, "form.html", context={"category":category})


class Login (View):
    def get (self, request):
        return render (request, "login.html")

    def post (self, request):
        users_list = User.objects.all()
        if request.method == "POST":
            username = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate (username=username, password=password)
            try:
                if user == User.objects.get_by_natural_key(username=username):
                    login (request, user)
                    return redirect (reverse ("landing"))
                else:
                    message = "Podano niepoprawny login i hasło"
                    return render (request, "login.html", context={"message": message})
            except Exception:
                return redirect (reverse ("register"))

class LogoutView (View):
    def get (self, request):
        logout (request)
        return redirect (reverse ("landing"))



class Register (View):
    def get (self, request):
        return render (request, "register.html")
    def post(self, request):
        if request.method == "POST":
            name = request.POST.get("name")
            surname = request.POST.get("surname")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            if password == password2:
                User.objects.create_user(username=email,email=email,password=password, first_name=name, last_name=surname)
                return render (request, "login.html")
            else:
                message="Podano niepoprawne dane"
                return render (request, "register.html", context={"message":message})


