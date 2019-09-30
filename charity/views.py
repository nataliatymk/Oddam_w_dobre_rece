from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import datetime
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

class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html")



class EditProfileView(View):
    def get(self, request):
        return render(request, "edit_profile.html")
    def post(self, request):
        user_id = request.user
        user = User.objects.get(id = user_id.id)
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        form_password = request.POST.get("form_password")
        if user.check_password(form_password) == True:
            user.username =email
            user.first_name = name
            user.last_name = surname
            user.email= email
            user.save()
            message = "Zmiany w profilu zostały zapisane"
            return render (request, "edit_profile.html", context={"message": message})

        old_password = request.POST.get("old_password")

        if user.check_password(old_password) == True:
            new_password = request.POST.get("password")
            new_check = request.POST.get("password2")
            if new_check == new_password:
                user.set_password(new_password)
                user.save()
                message = "Hasło zostało poprawnie zmienione"
            else:
                message = "Niepoprawne hasło"
        else:
            message = "Niepoprawne hasło"

        return render(request, "edit_profile.html", context={"message":message})

class DonationProfileView(View):
    def get(self, request):
        user = request.user
        donation_list = Donation.objects.all().filter(user_id = user).order_by('is_taken')
        return render(request, "profile_donation.html", context={"donation_list":donation_list})
    def post(self, request):
        user = request.user
        donation_list = Donation.objects.all().filter(user_id = user).order_by('is_taken')
        is_taken = request.POST.get("is_taken")
        taken = request.POST.get("taken")

        if is_taken:
            change=Donation.objects.get(id=is_taken)
            change.is_taken = True
            date=datetime.datetime.today().date()
            time = datetime.datetime.today().time()
            change.pick_up_date = date
            change.pick_up_time = time
            change.save()

        if taken:
            change = Donation.objects.get(id=taken)
            change.is_taken = False
            change.pick_up_date = None
            change.pick_up_time = None
            change.save ()


        return render(request, "profile_donation.html", context={"donation_list":donation_list})


