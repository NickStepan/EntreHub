from django.db import models
from authorization.models import CustomUser
import hashlib

# Create your models here.

def hashing(card):
    return hashlib.sha256(str(card).encode()).hexdigest()

def card_path(instance, filename):
        user_id = instance.author.id
        return f'avatars/{user_id % 10}/card_ico/{filename}'

class Card(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="author")
    topic = models.CharField(max_length=150)
    description = models.CharField(max_length=1500, default="Введіть опис картки")
    #tags = models.CharField(max_length=150)
    card_hash = models.CharField(max_length=64, blank=True, editable=False) # Поле для хешу    
    ico_card = models.ImageField(upload_to=card_path, blank=True, null=True, default='images/card.png')
    
    def save(self, *args, **kwargs):
        # Спочатку зберігаємо об'єкт, щоб отримати ID
        super().save(*args, **kwargs)  # Це вже зберігає id

        if not self.card_hash:                      # Тепер генеруємо хеш після того, як об'єкт збережено
            self.card_hash = hashing(self.id)
        super().save(update_fields=['card_hash'])           # Тепер зберігаємо об'єкт з новим значенням card_hash

    def __str__(self):
        return f"Card by {self.author}"
    

# class Schedule(models.Model):
#     DAYS_OF_WEEK = (
#         ('MON', 'Monday'),
#         ('TUE', 'Tuesday'),
#         ('WED', 'Wednesday'),
#         ('THU', 'Thursday'),
#         ('FRI', 'Friday'),
#         ('SAT', 'Saturday'),
#         ('SUN', 'Sunday'),
#     )

#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="client")
#     card = models.ForeignKey(Card, on_delete=models.CASCADE)
#     day = models.DateField()
#     day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
#     start_time = models.TimeField(null=True, blank=True)
#     end_time = models.TimeField(null=True, blank=True)
#     is_available = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Schedule by {self.author} on {self.card}"
    
# class Booking(models.Model):
#     schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="schedules")
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
#     booking_date = models.DateField()
#     booking_time = models.TimeField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Booking by {self.user} on {self.booking_date} at {self.booking_time}"
    
    