from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest.models import Event, Participant
from rest.serializer import EventSerializer, ParticipantSerializer
import requests
import json
from datetime import datetime, timedelta


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects
    serializer_class = EventSerializer

    @staticmethod
    def to_dict_with_participant(event: Event):
        participants = Participant.objects.filter(event__id=event.id).all()
        event_dict = event.to_dict()
        participants_list = [p.to_dict() for p in participants]
        event_dict.update(participants=participants_list)
        return event_dict

    def list(self, request, *args, **kwargs):
        events = self.queryset.all()
        events_dict = [self.to_dict_with_participant(e) for e in events]
        return Response(data=events_dict, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        event_dict = {
            'title': data.get('title'),
            'date': data.get('date'),
            'place': data.get('place'),
            'max_people': data.get('max_people'),
            'remark': data.get('remark'),
        }
        event = Event(**event_dict)
        event.save()
        return Response(data=event.id, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        eid = data.get('id')
        event = self.queryset.filter(id=eid).get()
        event_dict = {
            'title': data.get('title'),
            'date': data.get('date'),
            'place': data.get('place'),
            'max_people': data.get('max_people'),
            'remark': data.get('remark'),
        }
        event.update(event_dict)
        event.save()
        return Response(data=event.id, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        eid = self.kwargs['eid']
        event = self.queryset.filter(id=eid)
        event.delete()
        return Response(data={}, status=status.HTTP_200_OK)


class Participation(generics.CreateAPIView):
    queryset = Participant.objects
    serializer_class = ParticipantSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        event_id = data.get('event')
        event = Event.objects.filter(id=event_id).get()
        name = data.get('name')
        participant = Participant(event=event, name=name)
        participant.save()
        return Response(data=participant.id, status=status.HTTP_201_CREATED)


class Discord(generics.RetrieveAPIView):
    queryset = Event.objects
    serializer_class = EventSerializer

    @staticmethod
    def create_query(event: Event):
        return {
            'title': event.title,
            'fields': [
                {
                    'name': '日時',
                    'value': event.date.strftime('%Y年%m月%d日 %H:%M')
                },
                {
                    'name': '場所',
                    'value': event.place
                },
                {
                    'name': '備考',
                    'value': event.remark
                },
            ]
        }

    def get(self, request, *args, **kwargs):
        today = datetime.now() + timedelta(hours=9)
        all_events = self.queryset.all()
        events = list(filter(lambda e: today.date() == e.date.date(), all_events))
        url = "https://discordapp.com/api/webhooks/736767432076689471/bI2PyBoHm02ur00VU1vtXri5Fk_daEGc2yBR0-0QkUO65Xnukmf7UMHEutt-xAFhXswl"
        headers = {'content-type': 'application/json'}

        if len(events) == 0:
            query = {
                'content': '本日のイベントはありません。'
            }
            payload = json.dumps(query)
            requests.post(url, data=payload, headers=headers)
        else:
            query = {
                'content': '本日のイベントです。',
                'embeds': [self.create_query(e) for e in events],
            }
            payload = json.dumps(query)
            requests.post(url, data=payload, headers=headers)

        return Response(data=query, status=status.HTTP_200_OK)
