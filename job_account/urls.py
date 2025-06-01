from django.urls import path
from .views import view_card, create_card, edit_card, delete_card#, add_schedule_to_card

urlpatterns = [
    path('card/<str:hashed>/', view_card, name="card_detail"),
    path('edit-card/<str:card>/', edit_card, name="edit_card"),
    path('new-card/', create_card, name="create_card"),
    path('delete-card/<int:pk>', delete_card, name="delete_card"),
    #path('card/<str:hashed>/add-schedule/', add_schedule_to_card, name='add_schedule_to_card'),    
]