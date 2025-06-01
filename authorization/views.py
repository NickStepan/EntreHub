from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, UserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

#from .forms import UserCreationForm

from job_account.models import Card
from .utils import hash_data
# Create your views here.

def index(request):
    profiles = CustomUser.objects.all()
    cards = Card.objects.all()
    
    #cards = [
    #        {"text": "Це перший профіль"},
    #        {"text": "Це другий профіль"},
    #        {"text": "Це третій профіль"},
    #        {"text": "Це четвертий профіль"},
    #        {"text": "Це п'ятий профіль"},
    #    ]
    
    context = {
        'cards': cards,
        'profiles': profiles
        }

    return render(request, 'main/index.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            if request.POST.get('remember_me'):
                request.session.set_expiry(1209600)  # 2 тижні
            else:
                request.session.set_expiry(0)  # Сесія до закриття браузера

            redirect_to = request.POST.get('next', request.GET.get('next', reverse('index')))
            messages.success(request, 'Ви успішно увійшли!')
            return redirect(redirect_to)  # перенаправити на сторінку входу, або куди потрібно
        else:
            messages.error(request, 'Помилка при реєстрації. Перевірте введені дані.')
    else:
        form = UserCreationForm()
    return render(request, 'authorization/register.html', {'form': form})


def login_view(request):
    # Якщо користувач уже авторизований, перенаправляємо на головну сторінку
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.POST.get('remember_me'):
                    request.session.set_expiry(1209600)  # 2 тижні
                else:
                    request.session.set_expiry(0)  # Сесія до закриття браузера
                
                # Обробка параметра 'next' для редіректу, для повернення на сторінку з якої було перенаправлено на авторизацію
                redirect_to = request.POST.get('next', request.GET.get('next', reverse('index')))
                messages.success(request, 'Ви успішно увійшли!')
                return redirect(redirect_to)
            else:
                messages.error(request, "Невірне ім'я користувача або пароль.")
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'authorization/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('index')



#@login_required
def profile_view(request, profile):
    if request.method == "GET":
        #if not request.profile
        user = get_object_or_404(CustomUser, username=profile)
        #card = get_object_or_404(Card, pk=request.card.id)
        user_cards = Card.objects.filter(author=user)

        context = {
            'user': user,
            "user_cards":user_cards,

        }
    return render(request, 'authorization/my_profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        #profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() :
            user_form.save()
            #profile_form.save()
            return redirect('profile', profile=str(request.user))
    else:
        user_form = UserForm(instance=request.user)
        #profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'authorization/edit_profile.html', {
        'user_form': user_form,
        #'profile_form': profile_form
    })