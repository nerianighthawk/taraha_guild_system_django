from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest.models import Event, Participant
from rest.serializer import EventSerializer, ParticipantSerializer


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
        data = request.POST
        max_people = data.get('max_people') if data.get('max_people') else None
        event_dict = {
            'title': data.get('title'),
            'date': data.get('date'),
            'max_people': max_people,
            'remark': data.get('remark'),
        }
        event = Event(**event_dict)
        event.save()
        return Response(data=event.id, status=status.HTTP_201_CREATED)


class Participation(generics.CreateAPIView):
    queryset = Participant.objects
    serializer_class = ParticipantSerializer

    def post(self, request, *args, **kwargs):
        data = request.POST
        event_id = data.get('event')
        event = Event.objects.filter(id=event_id).get()
        name = data.get('name')
        participant = Participant(event=event, name=name)
        participant.save()
        return Response(data=participant.id, status=status.HTTP_201_CREATED)
