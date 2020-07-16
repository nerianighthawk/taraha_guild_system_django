from django.contrib import admin

from rest.models import Event, Participant


@admin.register(Event)
class Event(admin.ModelAdmin):
    pass


@admin.register(Participant)
class Participant(admin.ModelAdmin):
    pass
