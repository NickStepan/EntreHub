from django.contrib import admin
from .models import Card
# Register your models here.

from .models import CustomUser

admin.site.register(Card)  


if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser('admin', 'admin@example.com', '1')