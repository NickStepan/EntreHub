from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

def user_avatar_path(instance, filename):
        user_id = instance.user.id
        # Зберігаємо аватар у папці, названій за username або id користувача
        return f'avatars/{user_id % 10}/{user_id}/{filename}'
        # Або за id: return f'avatars/{instance.user.id}/{filename}'

class CustomUser(AbstractUser):    
    profession = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.username


# Створення аккаунту(профілю) для користувача,
#    для того щоб додати нові поля(місто, картинка),
#        яких немає у вбудованого User

class UserProfile(models.Model):
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True, default='images/avatar.png')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    pass
