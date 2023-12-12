from django.contrib import admin

from Fitness_center.models import Client, TrainingType, Subscription

admin.site.register(Client)
admin.site.register(TrainingType)
admin.site.register(Subscription)