from django.conf.urls import url
from rest.views import EventViewSet, Participation

urlpatterns = [
    url(r'^event/$', EventViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^participation/$', Participation.as_view()),
]
