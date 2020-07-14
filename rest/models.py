from django.db import models
from datetime import datetime


class Event(models.Model):
    id: int = models.AutoField(primary_key=True)
    title: str = models.CharField(max_length=31)
    date: datetime = models.DateTimeField()
    place: str = models.CharField(max_length=31)
    max_people: int = models.IntegerField(null=True)
    remark: str = models.CharField(max_length=255)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'place': self.place,
            'maxPeople': self.max_people,
            'remark': self.remark,
        }


class Participant(models.Model):
    id: int = models.AutoField(primary_key=True)
    event: Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=15)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
