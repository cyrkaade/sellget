from django.contrib import admin
from .models import myUser, Room, Message, Topic, Buy

admin.site.register(myUser)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Buy)
