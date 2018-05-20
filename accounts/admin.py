from django.contrib import admin

# Register your models here.
from accounts.models import User, PlayerInfo, SportCategory, City

admin.site.register(User)
admin.site.register(PlayerInfo)
admin.site.register(SportCategory)
admin.site.register(City)
