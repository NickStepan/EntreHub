from django import forms
from django.forms import formset_factory
from .models import Card #Schedule, Booking


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['topic', 'description', 'ico_card']
        
        widgets = {
            'topic': forms.TextInput(attrs={'placeholder': 'Введіть тему картки'}),
            'description': forms.Textarea(attrs={'placeholder': 'Опис картки'}),
            #'ico_card': forms.Input(attrs={'placeholder': 'Оберіть іконку'}),
        }

class EditCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['topic', 'description', 'ico_card']


# class ScheduleForm(forms.ModelForm):
#     class Meta:
#         model = Schedule
#         fields = ['day_of_week', 'start_time', 'end_time', 'is_available']
#         widgets = {
#             'start_time': forms.TimeInput(attrs={'type': 'time'}),
#             'end_time': forms.TimeInput(attrs={'type': 'time'}),
#         }

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['booking_date', 'booking_time']
#         widgets = {
#             'booking_date': forms.DateInput(attrs={'type': 'date'}),
#             'booking_time': forms.TimeInput(attrs={'type': 'time'}),
#         }
#     def clean(self):
#         cleaned_data = super().clean()
#         booking_date = cleaned_data.get('booking_date')
#         booking_time = cleaned_data.get('booking_time')
#         schedule = self.instance.schedule
#         if not schedule.is_available:
#             raise forms.ValidationError(f"{schedule.get_day_of_week_display()} is not available for booking.")
#         if booking_date.weekday() != list(schedule.DAYS_OF_WEEK).index((schedule.day_of_week, schedule.get_day_of_week_display())):
#             raise forms.ValidationError(f"Booking date must match the schedule day ({schedule.get_day_of_week_display()}).")
#         if schedule.start_time and booking_time < schedule.start_time:
#             raise forms.ValidationError(f"Booking time must be after {schedule.start_time}.")
#         if schedule.end_time and booking_time > schedule.end_time:
#             raise forms.ValidationError(f"Booking time must be before {schedule.end_time}.")
#         return cleaned_data