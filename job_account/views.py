from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.contrib import messages
from .forms import CardCreateForm, EditCardForm#, ScheduleForm, BookingForm

from authorization.models import CustomUser
from .models import Card#, Schedule
from datetime import timedelta, datetime

# Create your views here.

@login_required
def create_card(request):

    if request.method == 'POST':
        card_form = CardCreateForm(request.POST, request.FILES)
        

        if card_form.is_valid():
            card = card_form.save(commit=False)  # Типу чернетка
            card.author = request.user  # Призначаємо поточного користувача як автора
            #Додати інші потрібні поля, теги, тема, текст, так далі
            card.save()
            


            messages.success(request, 'Картку успішно створено!')
            return redirect('index')  # Перенаправлення на список карток
        else:
            messages.error(request, 'Помилка при створенні картки. Перевірте введені дані.')
    else:
        card_form = CardCreateForm()
    return render(request, 'job_account/create_card.html', {'card_form': card_form,})


@login_required
def edit_card(request, card):
    instance = get_object_or_404(Card, card_hash=card)
    if request.method == 'POST':
        edit_card_form = EditCardForm(request.POST, instance=instance)
        
        if edit_card_form.is_valid() :
            edit_card_form.save()
            return redirect('card_detail', hashed=card)
    else:
        edit_card_form = EditCardForm(instance=instance)
       
    
    return render(request, 'job_account/edit_card.html', {
        'edit_card': edit_card_form,
        'card': instance.card_hash,
        'card_name': instance.topic
       
    })

def view_card(request, hashed):
    
    if request.method == "GET":
        #Треба зробити хешування, потім тут перевірку хешу картки
        #  і тільки у разі якщо така є
        #   то виводити із захешованим ідентифікатором картки у посиланні(URL-адресі)
        
        card = get_object_or_404(Card, card_hash=hashed)
        user_card =  CustomUser.objects.filter(username=card.author)
        #card_hash = hash_id(card.id)  # Хешуємо ID для показу в URL

        # Отримати всі поля моделі Card та їх значення
        fields_data = []
        for field in card._meta.get_fields():
            # пропускаємо поля ManyToMany та інші, якщо потрібно
            if hasattr(field, 'name'):
                field_name = field.name
                # отримати значення поля з об'єкта card
                value = getattr(card, field_name)
                fields_data.append({'name': field_name, 'value': value})
    #     schedules = card.schedules.all()
    #     booking_form = BookingForm()

    # if request.method == 'POST':
    #     booking_form = BookingForm(request.POST)
    #     if booking_form.is_valid():
    #         booking = booking_form.save(commit=False)
    #         booking.user = request.user
    #         booking.schedule = get_object_or_404(Schedule, id=request.POST.get('schedule_id'))
    #         booking.save()
    #         messages.success(request, "Booking created successfully!")
    #         return redirect('card_detail', hashed=card.card_hash)    
    
    context = {
        "card":card,
        "user":user_card,
        "fields_data":fields_data,
        
        # 'schedules': schedules,
        # 'booking_form': booking_form

        }
        
    return render(request, 'job_account/card.html', context)
      
@login_required
def delete_card(request, pk):
    card = get_object_or_404(Card, pk=pk)

    if request.method == 'POST':
        card.delete()
        return redirect('profile', profile=request.user)
    return render(request, 'job_account/delete_card.html', {'card': card})




# def add_schedule_to_card(request, card_id):
#     card = get_object_or_404(Card, id=card_id, author=request.user)
#     ScheduleFormSet = formset_factory(ScheduleForm, extra=7)
#     if request.method == 'POST':
#         formset = ScheduleFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data.get('day_of_week'):
#                     schedule = form.save(commit=False)
#                     schedule.author = request.user
#                     schedule.card = card
#                     schedule.save()
#             messages.success(request, "Schedule added successfully!")
#             return redirect('card_detail', card_id=card.id)
#     else:
#         formset = ScheduleFormSet()
#     return render(request, 'schedule.html', {'formset': formset, 'card': card})


